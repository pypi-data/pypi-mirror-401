# detect.py
import sys, threading, time, platform, queue, json, cv2
from pathlib import Path
from datetime import timedelta
import numpy as np
from ultralytics import YOLO

# ----------- UTILITIES ---------------
from .utils.paths import get_runs_dir, get_output_folder, WEIGHTS_DIR
from .utils.detect.arguments import parse_arguments
from .utils.console import Console, fmt_bold
from .utils.detect.measurements import (
    MeasurementConfig,
    Counter,
    Interactions,
    Aggregator,
    Motion,
    compute_counts_from_boxes,
)
from .utils.detect.class_config import load_or_create_classes, ClassConfig
from .utils.detect.video_util import (
    VideoSourceInfo,
    extract_video_metadata,
    extract_camera_metadata,
    VideoReader,
    create_video_writer,
    write_annotated_frame,
    extract_boxes_from_results,
)
from .utils.detect.inference_util import InferenceWorker
from .utils.train.io import ensure_weights

# ---- SYSTEM ----
stop_event = threading.Event()
IS_MAC = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"
IS_PI = IS_LINUX and ("arm" in platform.machine() or "aarch64" in platform.machine())


# ---- THREADING MANAGER ----
class VideoProcessor:
    def __init__(
        self,
        weights_path,
        source,
        source_type,
        idx,
        total_sources,
        printer,
        test=False,
        model_name=None,
        class_config: "ClassConfig" = None,
    ):
        self.weights_path = Path(weights_path)
        self.model_name = str(model_name) if model_name is not None else self.weights_path.stem
        self.class_config = class_config

        self.source = source
        self.source_type = source_type
        self.idx = idx
        self.total_sources = total_sources
        self.printer = printer
        self.test = test

        self.is_camera = source_type == "usb"
        base_src_name = Path(str(source)).stem if not self.is_camera else f"usb{source}"
        self.source_display_name = f"{self.model_name} | {base_src_name}"

        # ---------- THREADING QUEUES ----------
        self.frame_queue = queue.Queue(maxsize=50)
        self.infer_queue = queue.Queue(maxsize=20)

        # Components
        self.reader = None
        self.infer_worker = None

        # Model / IO
        self.model = None
        self.is_obb_model = False
        self.cap = None
        self.out_writer = None

        # Measurement objects
        self.config = MeasurementConfig()
        self.counter = None
        self.aggregator = None
        self.interactions = None
        self.motion = None

        # Timing / metadata
        self.start_time = None
        self.fps_video = None
        self.total_frames = None
        self.frame_width = None
        self.frame_height = None

        self.paths = None
        self.out_file = None
        self.metadata_file = None

    # ----------- Initialization -----------
    def initialize(self):
        # Load model
        try:
            self.model = YOLO(str(self.weights_path))
            self.model.weights_path = self.weights_path
        except Exception as e:
            self.printer.model_fail(e)
            return False

        # Detect OBB capability
        try:
            test_frame = np.zeros((640, 640, 3), dtype=np.uint8)
            res = self.model.predict(test_frame, verbose=False, show=False)
            self.is_obb_model = hasattr(res[0], "obb") and res[0].obb is not None
        except Exception:
            self.is_obb_model = False

        # ---------- Capture init FIRST ----------
        try:
            if self.is_camera:
                backend = cv2.CAP_AVFOUNDATION if IS_MAC else cv2.CAP_V4L2
                self.cap = cv2.VideoCapture(int(self.source), backend)
            else:
                self.cap = cv2.VideoCapture(str(self.source))

            if not self.cap.isOpened():
                self.printer.open_capture_fail(self.source_display_name)
                return False
        except Exception:
            self.printer.open_capture_fail(self.source_display_name)
            return False

        # ---------- Unified VideoSourceInfo handling ----------
        if not self.is_camera:
            meta_dict = extract_video_metadata(self.source)
            src_info = VideoSourceInfo(meta_dict, is_camera=False, display_name=self.source_display_name)
        else:
            try:
                source_id = int(self.source)
            except ValueError:
                source_id = 0
            meta_dict = extract_camera_metadata(self.cap, source_id)
            src_info = VideoSourceInfo(meta_dict, is_camera=True, display_name=self.source_display_name)

        # Parse creation time (returns datetime)
        self.start_time = src_info.parse_creation_time()
        metadata = src_info.metadata
        metadata["creation_time_str"] = self.start_time.strftime("%H:%M:%S")

        # ---------- Output paths ----------
        self.paths = get_output_folder(
            self.weights_path,
            self.source_type,
            self.source if not self.is_camera else f"usb{self.source}",
            test_detect=self.test,
            base_time=self.start_time,
        )

        self.out_file = self.paths["video_folder"] / f"{self.paths['safe_name']}.mp4"
        self.metadata_file = self.paths["metadata"]

        with open(self.metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

        # ---------- Dimensions & FPS ----------
        if not self.is_camera:
            ret, frame0 = self.cap.read()
            if not ret or frame0 is None:
                self.printer.read_frame_fail(self.source_display_name)
                return False

            self.frame_height, self.frame_width = frame0.shape[:2]
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        else:
            self.frame_width = src_info.width or int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
            self.frame_height = src_info.height or int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)

        # FPS
        if src_info.fps:
            self.fps_video = src_info.fps
        else:
            src_fps = self.cap.get(cv2.CAP_PROP_FPS)
            if not src_fps or src_fps <= 0 or np.isnan(src_fps):
                src_fps = 30.0
            self.fps_video = src_fps

        # ---------- TOTAL FRAMES FOR VIDEO SOURCES ----------
        if not self.is_camera:
            total = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            if total is None or total < 2:
                duration = getattr(src_info, "duration", None)
                if duration:
                    self.total_frames = int(duration * self.fps_video)
                else:
                    self.total_frames = None
            else:
                self.total_frames = int(total)
        else:
            self.total_frames = None

        # ---- VIDEO WRITER ----
        self.out_writer = create_video_writer(
            self.out_file,
            self.fps_video,
            self.frame_width,
            self.frame_height,
            self.source_display_name,
            self.printer,
            self.cap,
            self.source_type,
        )
        if self.out_writer is None:
            return False

        # --- Measurement objects ---
        self.counter = Counter(out_folder=self.paths["counts"], class_config=self.class_config, config=self.config, start_time=self.start_time)
        self.aggregator = Aggregator(out_folder=self.paths["counts"], class_config=self.class_config, config=self.config, start_time=self.start_time)
        self.interactions = Interactions(
            out_folder=self.paths["interactions"],
            class_config=self.class_config,
            config=self.config,
            start_time=self.start_time,
            is_obb=self.is_obb_model,
        )
        self.motion = Motion(
            paths=self.paths,
            class_config=self.class_config,
            frame_width=self.frame_width,
            frame_height=self.frame_height,
            config=self.config,
            start_time=self.start_time,
        )

        # --- Reader + Inference worker ---
        self.reader = VideoReader(
            cap=self.cap,
            frame_queue=self.frame_queue,
            infer_queue=self.infer_queue,
            is_camera=self.is_camera,
            source_display_name=self.source_display_name,
            global_stop_event=stop_event,
            printer=self.printer,
        )

        self.infer_worker = InferenceWorker(
            model=self.model,
            frame_queue=self.frame_queue,
            infer_queue=self.infer_queue,
            is_camera=self.is_camera,
            frame_width=self.frame_width,
            frame_height=self.frame_height,
            source_display_name=self.source_display_name,
            global_stop_event=stop_event,
            printer=self.printer,
        )
        return True

    # ---------- Writer / Processing Loop ----------
    def run(self):
        frame_count = 0
        prev_time = time.time()
        loop_start = time.time()

        self.reader.start()
        self.infer_worker.start()

        try:
            while not stop_event.is_set():
                try:
                    item = self.infer_queue.get(timeout=0.1)
                except queue.Empty:
                    if stop_event.is_set():
                        break
                    continue

                # EOF marker
                if (
                    isinstance(item, tuple)
                    and len(item) == 2
                    and isinstance(item[0], str)
                    and item[0] == "EOF"
                ):
                    break

                frame_resized, results = item

                # ---------- Annotation ----------
                try:
                    annotated_tmp = results[0].plot() if results else frame_resized
                    h, w = annotated_tmp.shape[:2]
                    if (w, h) != (self.frame_width, self.frame_height):
                        annotated = cv2.resize(annotated_tmp, (self.frame_width, self.frame_height), interpolation=cv2.INTER_LINEAR)
                    else:
                        annotated = annotated_tmp
                except Exception:
                    annotated = frame_resized

                # ---------- Extract boxes ----------
                names, boxes_list = extract_boxes_from_results(results, self.is_obb_model)

                # ---------- Timestamp ----------
                video_ts = self.start_time + timedelta(seconds=frame_count / self.fps_video)

                # ---------- Measurements ----------
                counts = compute_counts_from_boxes(
                    boxes_list, names,
                    focus_classes=self.class_config.focus,
                    context_classes=self.class_config.context,
                )
                self.counter.update_counts(boxes_list, names, video_ts)
                self.aggregator.push_frame_data(video_ts, counts_dict=counts)
                self.interactions.process_frame(boxes_list, names, video_ts)
                self.motion.process_frame(boxes_list, names, video_ts)

                # ---------- Terminal status ----------
                fps_smooth, tstr, prev_time, eta = self.printer.format_time_fps(
                    frame_count,
                    prev_time,
                    loop_start,
                    fps_video=self.fps_video,
                    total_frames=self.total_frames,
                    source_type=self.source_type,
                    source_idx=self.idx,  # keep smoothing separated per processor
                )

                frame_count += 1
                if frame_count % 5 == 0:
                    self.printer.update_frame_status(
                        self.idx,
                        self.source_display_name,
                        frame_count,
                        fps_smooth,
                        counts,
                        tstr,
                        eta,
                    )

                # ---------- Write annotated frame ----------
                write_annotated_frame(self.out_writer, annotated)

        finally:
            if self.reader:
                self.reader.stop()
            if self.infer_worker:
                self.infer_worker.stop()

            if self.reader:
                self.reader.join(timeout=1.0)

            while True:
                try:
                    self.frame_queue.get_nowait()
                except queue.Empty:
                    break

            if self.infer_worker:
                self.infer_worker.join(timeout=2.0)

            saved = [self.out_file, self.metadata_file]

            # ---------- Save measurement results ----------
            f1 = self.counter.save_results()
            if f1:
                saved.extend(f1)
            self.aggregator.finalize()
            f2 = self.aggregator.save_interval_results()
            if f2:
                saved.append(f2)
            f3 = self.aggregator.save_session_summary()
            if f3:
                saved.append(f3)
            f4 = self.interactions.save_results()
            if f4:
                saved.extend(f4) if isinstance(f4, list) else saved.append(f4)
            f5 = self.motion.save_results()
            if f5:
                saved.extend(f5)

            self.printer.mark_source_complete(self.idx)
            self.interactions.finalize()
            self.printer.save_measurements(self.paths["scores_folder"], saved)


# ---------------------- MODEL RESOLUTION HELPERS ----------------------
def _resolve_one_model(model_arg: str, runs_dir: Path, printer: Console):
    """
    Resolve a single model identifier into:
      (model_name: str, weights_path: Path)
    Supports:
      - runs/<model_run> directory name
      - explicit .pt path
      - official model name via ensure_weights
    """
    model_arg = str(model_arg).strip()
    if not model_arg:
        return None

    candidate_dir = runs_dir / model_arg
    if candidate_dir.is_dir():
        model_name = candidate_dir.name
        best = candidate_dir / "weights" / "best.pt"
        if best.exists():
            return model_name, best

        pts = sorted(candidate_dir.rglob("*.pt"), key=lambda p: p.stat().st_mtime, reverse=True)
        if pts:
            printer.warn(f"No best.pt found for {candidate_dir.name} — using: {pts[0].name}")
            return model_name, pts[0]

        printer.missing_weights(candidate_dir)
        return None

    model_path = Path(model_arg)

    # explicit .pt
    if model_path.suffix == ".pt":
        if not model_path.exists():
            printer.error(f"Model file does not exist: {fmt_bold(model_path)}")
            return None
        return model_path.stem, model_path

    # official YOLO name via ensure_weights
    placeholder = WEIGHTS_DIR / f"{model_arg}.pt"
    resolved = ensure_weights(placeholder, model_arg)
    if resolved is None or not resolved.exists():
        printer.error(f"Could NOT resolve or download model '{model_arg}'.")
        return None
    return resolved.stem, resolved


def _default_single_model_selection(runs_dir: Path, args, printer: Console):
    """
    Preserve existing single-model default behavior:
      - if runs/ has models -> pick newest or prompt selection
      - else fallback to yolo11n
    Returns (model_name, weights_path)
    """
    model_dirs = sorted(
        [d for d in runs_dir.iterdir() if d.is_dir() and (args.test or d.name.lower() != "test")],
        reverse=True,
    )

    if not model_dirs:
        placeholder = WEIGHTS_DIR / "yolo11n.pt"
        resolved = ensure_weights(placeholder, "yolo11n")
        if resolved is None or not resolved.exists():
            printer.error("Failed to download or resolve YOLO11n fallback model.")
            printer.exit("Detection aborted due to missing fallback model.")
            return None
        return resolved.stem, resolved

    if len(model_dirs) == 1:
        selected = model_dirs[0]
    else:
        selected = printer.prompt_model_selection(runs_dir, exclude_test=not args.test)
        if not selected:
            return None

    selected = Path(selected)
    model_name = selected.name
    best = selected / "weights" / "best.pt"
    if best.exists():
        return model_name, best

    pts = sorted(selected.rglob("*.pt"), key=lambda p: p.stat().st_mtime, reverse=True)
    if pts:
        printer.warn(f"No best.pt found — using: {pts[0].name}")
        return model_name, pts[0]

    printer.missing_weights(selected)
    return None


# ---- Main Entry ----
def main():
    args = parse_arguments()

    # We'll size Console based on #models × #sources once models are resolved.
    runs_dir = get_runs_dir(test=args.test)

    # Temporary printer for early resolution logs
    tmp_printer = Console(total_sources=0)

    # ---------------------- RESOLVE MODELS ----------------------
    model_specs = []  # list of dicts: {model_name, weights_path, class_config}
    if getattr(args, "model", None) and len(args.model) > 0:
        for m in args.model:
            resolved = _resolve_one_model(m, runs_dir, tmp_printer)
            if resolved is None:
                tmp_printer.exit("Detection aborted due to invalid model selection.")
                sys.exit(1)
            model_name, weights_path = resolved

            if not weights_path.exists() or weights_path.stat().st_size == 0:
                tmp_printer.error(f"Invalid weights file: {fmt_bold(weights_path)}")
                tmp_printer.exit("Detection aborted due to missing weights file.")
                sys.exit(1)

            class_config = load_or_create_classes(
                model_name=model_name,
                weights_path=weights_path,
                force_reload=False,
                printer=tmp_printer,
            )

            model_specs.append(
                {
                    "model_name": model_name,
                    "weights_path": weights_path,
                    "class_config": class_config,
                }
            )
    else:
        # default: single model selection behavior (unchanged)
        resolved = _default_single_model_selection(runs_dir, args, tmp_printer)
        if resolved is None:
            sys.exit(1)
        model_name, weights_path = resolved

        class_config = load_or_create_classes(
            model_name=model_name,
            weights_path=weights_path,
            force_reload=False,
            printer=tmp_printer,
        )
        model_specs.append(
            {
                "model_name": model_name,
                "weights_path": weights_path,
                "class_config": class_config,
            }
        )

    # ---------------------- REAL PRINTER (correct total_sources) ----------------------
    total_processors = len(model_specs) * len(args.sources)
    printer = Console(total_sources=total_processors)

    # Show model banner
    if len(model_specs) == 1:
        printer.set_model_name(model_specs[0]["model_name"])
    else:
        joined = ", ".join([m["model_name"] for m in model_specs])
        printer.set_model_name(f"{len(model_specs)} models: {joined}")

    # Union classes for UI placeholder usage (Console now uses self.all_classes after our patch below)
    union_classes = []
    seen = set()
    for ms in model_specs:
        for c in ms["class_config"].display_classes:
            if c not in seen:
                seen.add(c)
                union_classes.append(c)
    printer.classes_loaded(union_classes)

    # ---------------------- BUILD PROCESSORS (model × source) ----------------------
    processors = []
    idx = 1  # global processor index for Console UI rows

    for ms in model_specs:
        model_name = ms["model_name"]
        weights_path = ms["weights_path"]
        class_config = ms["class_config"]

        for src in args.sources:
            s = str(src)

            # determine source_type
            if s.lower().startswith("usb"):
                source_type = "usb"
                try:
                    source_id = int(s[3:])
                except ValueError:
                    printer.warn(f"Invalid USB source '{s}' — must be like usb0, usb1")
                    continue
            else:
                source_type = "video"
                source_id = s

            printer.sources[idx - 1]["source_type"] = source_type

            vp = VideoProcessor(
                weights_path=weights_path,
                source=source_id,
                source_type=source_type,
                idx=idx,
                total_sources=total_processors,
                printer=printer,
                test=args.test,
                model_name=model_name,
                class_config=class_config,
            )
            if vp.initialize():
                printer.register_source_classes(idx, class_config.display_classes)
                processors.append(vp)
                idx += 1
            else:
                # If a processor fails to init, still increment the UI slot so indexing stays consistent.
                printer.warn(f"Processor failed to initialize: {model_name} | {s}")
                idx += 1

    # ---------------------- START THREADS ----------------------
    threads = []
    for vp in processors:
        t = threading.Thread(target=vp.run, daemon=True)
        t.start()
        threads.append(t)

    try:
        while any(t.is_alive() for t in threads):
            time.sleep(0.1)
    except KeyboardInterrupt:
        printer.stop_signal_received(single_thread=(len(threads) == 1))
        stop_event.set()

        for t in threads:
            while t.is_alive():
                try:
                    t.join(timeout=0.5)
                except KeyboardInterrupt:
                    continue

    printer.release_all_writers()
    printer.all_threads_terminated()


if __name__ == "__main__":
    main()
