# utils/console.py
import os
import re
import time
import logging
import threading
from pathlib import Path
from datetime import datetime
from ultralytics.utils import LOGGER

# ------------- COLORS -------------
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"

RED = "\033[31m"
BRIGHT_RED = "\033[91m"

GREEN = "\033[32m"
BRIGHT_GREEN = "\033[92m"

YELLOW = "\033[33m"
BRIGHT_YELLOW = "\033[93m"

BLUE = "\033[34m"
BRIGHT_BLUE = "\033[94m"
BLUE_006B = "\033[38;5;33m"

MAGENTA = "\033[35m"
BRIGHT_MAGENTA = "\033[95m"

CYAN = "\033[36m"
BRIGHT_CYAN = "\033[96m"

WHITE = "\033[37m"

# ------------- FORMATTING HELPERS -------------
def fmt_info(msg):   return f"{BRIGHT_CYAN}{BOLD}info{RESET}: {WHITE}{msg}{RESET}"
def fmt_model(msg):  return f"{BRIGHT_YELLOW}{BOLD}model{RESET}: {WHITE}{msg}{RESET}"
def fmt_dataset(msg):return f"{BLUE}{BOLD}dataset{RESET}: {WHITE}{msg}{RESET}"
def fmt_train(msg):  return f"{GREEN}{BOLD}train{RESET}: {WHITE}{msg}{RESET}"
def fmt_exit(msg):   return f"{BRIGHT_RED}{BOLD}exit{RESET}: {WHITE}{msg}{RESET}"
def fmt_warn(msg):   return f"{YELLOW}{BOLD}warn{RESET}: {WHITE}{msg}{RESET}"
def fmt_error(msg):  return f"{RED}{BOLD}error{RESET}: {WHITE}{msg}{RESET}"
def fmt_save(msg):   return f"{BRIGHT_GREEN}{BOLD}save{RESET}: {WHITE}{msg}{RESET}"
def fmt_source(txt): return f"{BLUE_006B}{BOLD}{txt}{RESET}"
def fmt_label(txt):  return f"{WHITE}{BOLD}{txt}{RESET}"
def fmt_header(txt): return f"{WHITE}{BOLD}{txt}{RESET}"
def fmt_num(n):      return f"{WHITE}{BOLD}{n}{RESET}"
def fmt_path(path: str | Path) -> str: return f"{BRIGHT_MAGENTA}{BOLD}{path}{RESET}"
def fmt_bold(txt: str | Path) -> str: return f"{WHITE}{BOLD}{txt}{RESET}"

# ------------- TERMINAL HELPERS -------------
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def print_divider(width=120):
    print("-" * width)

def print_training_header_static():
    print("\n" + "-" * 120 + "\n")

# ------------- ULTRALYTICS TRAINING LOG FILTERING / PATCHING -------------
class UltralyticsFilter(logging.Filter):
    noise_patterns = [
        r"Ultralytics.*Python",
        r"New .* available",
        r"engine/trainer",
        r"Transferred .* items",
        r"optimizer:",
        r"anchors:",
        r"Scanning .*labels",
        r"duplicate labels removed",
        r"ignoring corrupt",
        r"Freezing layer",
        r"summary:",
        r"Layers:",
        r"Model.*parameters",
        r"Using 0 dataloader workers",
        r"Image sizes",
        r"Creating cache",
        r"YOLO.*layers",
    ]

    def filter(self, record):
        msg = record.getMessage()
        return not any(re.search(p, msg) for p in self.noise_patterns)

def quiet_ultralytics_logs():
    ul = logging.getLogger("ultralytics")
    ul.setLevel(logging.INFO)
    ul.addFilter(UltralyticsFilter())

def quiet_wandb_logs():
    logging.getLogger("wandb").setLevel(logging.ERROR)

_original_info = LOGGER.info

def _is_epoch_line(msg: str) -> bool:
    return ("Epoch" in msg and "|" in msg) or ("%|" in msg)

def patched_info(msg, *a, **k):
    if getattr(patched_info, "interrupted", False):
        return

    lower = msg.lower()
    if "exit" in lower or "interrupt" in lower or "error" in lower:
        return _original_info(msg, *a, **k)

    if _is_epoch_line(msg):
        print_training_header()
        return _original_info(msg, *a, **k)

    if msg.strip() == "-" * 120:
        return

    suppress = (
        msg.startswith("train:")
        or msg.startswith("val:")
        or "Overriding model.yaml" in msg
        or "Fast image access" in msg
        or "ultralytics.nn" in msg
        or "Conv " in msg
        or "C2" in msg
        or "C3" in msg
        or "SPPF" in msg
        or "Concat" in msg
        or "Upsample" in msg
        or "parameters" in msg
        or msg.strip().startswith("from")
    )
    if suppress:
        return

    return _original_info(msg, *a, **k)

def apply_ultralytics_patch():
    LOGGER.info = patched_info

def remove_ultralytics_patch():
    LOGGER.info = _original_info

# ------------- TRAINING HEADER + FOOTER -------------
def print_training_header():
    clear_terminal()
    print(fmt_bold("YOLO4r Training"))
    print("----------------\n")

def print_training_footer(model_source, dataset_name, batch_size, workers, epochs):
    print(fmt_model(f"Model initializing: {fmt_path(model_source)}"))
    print(fmt_dataset(fmt_bold(dataset_name)))
    print(fmt_train(
        f"{WHITE}{BOLD}Epochs -{RESET} {epochs}    "
        f"{WHITE}{BOLD}Batch -{RESET} {batch_size}    "
        f"{WHITE}{BOLD}Workers -{RESET} {workers}"
    ))
    print()
    print_divider()
    print()

# -------------------------- UNIFIED CONSOLE UI CLASS --------------------------
class Console:
    """
    Unified UI for training + detection.

    Detection UI (multi-model):
      - UI is grouped by model (each model gets its own section + divider)
      - sources are shown WITHOUT model prefix (e.g. "skylight", not "model | skylight")
      - per-model classes are logged in the info region ("Loaded N classes: [...]")
      - final save blocks are grouped by model
    """
    def __init__(self, total_sources: int = 0):
        self.total_sources = total_sources
        self.lock = threading.Lock()

        self.sources = []
        for _ in range(total_sources):
            self.sources.append(
                {
                    "name": None,              # full display name e.g. "model | skylight"
                    "short_name": None,        # e.g. "skylight"
                    "model_name": None,        # e.g. "yolo11n"
                    "frame_count": 0,
                    "fps": 0.0,
                    "time_str": "--:--",
                    "counts": {},
                    "completed": False,
                    "source_type": None,       # "usb" or "video"
                    "eta": "--",
                    "classes": None,           # list[str] or None
                }
            )

        self.log_lines = []
        cols, rows = self._get_term_size()
        self.max_logs = max(15, rows // 2)

        self._fps_smooth = {}
        self.last_redraw_time = 0.0
        self.redraw_interval = 0.15

        self.freeze_ui = False
        self.final_exit_events = []
        self.in_shutdown = False

        # Final save blocks grouped by model: dict[str, list[list[str]]]
        self.final_save_blocks_by_model = {}

        # Optional fallback union (not preferred anymore, but kept for safety)
        self._recording_initialized_once = False
        self.all_classes = []

        # Per-model "Loaded classes" logging guard
        self._classes_logged_for_model = set()

        # Active video writers
        self.active_writers = {}

    # ------------- INTERNAL HELPERS -------------
    def _get_term_size(self):
        try:
            size = os.get_terminal_size()
            return size.columns, size.lines
        except OSError:
            return 120, 40

    def _append_log(self, formatted: str):
        with self.lock:
            self.log_lines.append(formatted)
            if len(self.log_lines) > self.max_logs:
                self.log_lines = self.log_lines[-self.max_logs:]
        self._maybe_redraw()

    def _extract_model_and_short(self, display_name: str):
        """
        Parse "model | source" format safely.
        Returns (model_name, short_name).
        """
        if not display_name:
            return None, None
        if " | " in display_name:
            m, s = display_name.split(" | ", 1)
            return m.strip() or None, s.strip() or None
        return None, display_name.strip()

    # ------------- PUBLIC LOGGING API (DETECT + TRAIN) -------------
    def info(self, msg):   self._append_log(fmt_info(msg))
    def warn(self, msg):   self._append_log(fmt_warn(msg))
    def error(self, msg):  self._append_log(fmt_error(msg))
    def exit(self, msg):   self._append_log(fmt_exit(msg))
    def save(self, msg):   self._append_log(fmt_save(msg))

    # ------------- MODEL / WEIGHTS HELPERS -------------
    def model_fail(self, e):
        self.error(f"Could NOT initialize model: {e}")

    def missing_weights(self, runs_dir):
        runs_dir = Path(runs_dir)
        self.error("YOLO model weights NOT found.")
        self.warn(f"Expected to find at least one model directory inside: {fmt_path(runs_dir)}")
        self.warn("Run training first OR copy a model into the runs folder.")
        self.exit("Detection aborted due to missing weights.")

    def model_init(self, weights_path):
        weights_path = Path(weights_path)
        try:
            idx = weights_path.parts.index("runs")
            short = Path(*weights_path.parts[idx : idx + 3])
        except ValueError:
            short = weights_path
        self._append_log(fmt_model(f"Initializing model: {fmt_path(short)}"))

    # ------------- MEASUREMENT SAVE WRAPPER -------------
    def save_measurements(self, base_dir, files, model_name: str | None = None):
        """
        Backward compatible:
          - old calls: save_measurements(base_dir, files)
          - new calls: save_measurements(base_dir, files, model_name="yolo11n")
        """
        base_dir = Path(base_dir)
        try:
            source_name = base_dir.parent.parent.name
        except Exception:
            source_name = base_dir.name
        title = f"Measurements for {source_name}"
        self.add_final_save_block(title, base_dir, files, model_name=model_name)

    # ------------- VIDEO WRITER REGISTRATION -------------
    def register_writer(
        self,
        raw_name,
        writer,
        cap,
        source_type,
        out_file,
        display_name=None,
    ):
        safe_name = re.sub(r"[^\w\-]", "_", Path(out_file.name).stem) + out_file.suffix
        self.active_writers[safe_name] = {
            "writer": writer,
            "cap": cap,
            "source_type": source_type,
            "out_file": out_file,
            "source_name": raw_name,
            "display_name": display_name or raw_name,
        }
        ts = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        self.recording_initialized(ts)
        return safe_name

    def recording_initialized(self, ts: str):
        if not self._recording_initialized_once:
            self._recording_initialized_once = True
            self.info(f"Recording initialized at {ts}")

    def safe_release_writer(self, name):
        entry = self.active_writers.get(name)
        if not entry:
            return
        try:
            entry["writer"].release()
        except Exception:
            pass
        try:
            entry["cap"].release()
        except Exception:
            pass
        self.active_writers.pop(name, None)

    def release_all_writers(self):
        for name in list(self.active_writers.keys()):
            self.safe_release_writer(name)

    # ------------- DETECTION IDENTITY HELPERS -------------
    def register_source_identity(self, idx: int, model_name: str, short_source_name: str, full_display_name: str | None = None):
        """
        Lets detect.py populate stable identity BEFORE frames start.
        This is the key to having correct grouped sections immediately.
        """
        i = idx - 1
        if i < 0 or i >= self.total_sources:
            return
        with self.lock:
            src = self.sources[i]
            src["model_name"] = model_name
            src["short_name"] = short_source_name
            if full_display_name:
                src["name"] = full_display_name
            elif model_name and short_source_name:
                src["name"] = f"{model_name} | {short_source_name}"
        self._maybe_redraw()

    # per-source class registration (multi-model safe)
    def register_source_classes(self, idx: int, classes_list):
        if not classes_list:
            return
        i = idx - 1
        if i < 0 or i >= self.total_sources:
            return
        with self.lock:
            self.sources[i]["classes"] = list(classes_list)

    # per-model class log (shown in info region)
    def model_classes_loaded(self, model_name: str, classes_list):
        if not model_name or not classes_list:
            return
        key = str(model_name)
        if key in self._classes_logged_for_model:
            return
        self._classes_logged_for_model.add(key)
        self.info(f"Loaded {len(classes_list)} classes: {classes_list}")

    def _format_class_lines(self, counts: dict, width: int, classes_list=None):
        display_entries = []

        is_placeholder = bool(counts) and all(str(v) == "--" for v in counts.values())

        if classes_list:
            ordered = list(classes_list)
        elif getattr(self, "all_classes", None):
            ordered = list(self.all_classes)
        else:
            ordered = list(counts.keys())

        if not ordered:
            return ["  (no detections yet)"]

        for c in ordered:
            val = "--" if is_placeholder else counts.get(c, 0)
            display_entries.append(f"{fmt_label(c)}: {val}")

        n = len(display_entries)

        if n <= 5:
            cols = 1
        elif n <= 8:
            cols = 2
        elif n <= 15:
            cols = 3 if width > 90 else 2
        else:
            cols = max(1, width // 18)

        max_len = max(len(e) for e in display_entries) + 4

        lines = []
        for i in range(0, n, cols):
            row = display_entries[i : i + cols]
            row = [r.ljust(max_len) for r in row]
            lines.append("  " + "".join(row).rstrip())

        return lines

    # ------------- TIME / FPS HELPERS -------------
    def _format_time_str(
        self,
        frame_count: int,
        prev_time: float,
        start_time: float,
        fps_video: float = None,
        total_frames: int = None,
        source_type: str = "video",
        source_idx: int = 0,
    ):
        now = time.time()
        instantaneous = 1.0 / (now - prev_time + 1e-6)
        instantaneous = min(instantaneous, 60.0)

        prev_smooth = self._fps_smooth.get(source_idx, instantaneous)
        fps_smooth = 0.9 * prev_smooth + 0.1 * instantaneous
        fps_smooth = min(fps_smooth, 60.0)
        self._fps_smooth[source_idx] = fps_smooth

        eta_str = None
        if source_type == "video" and fps_video and total_frames:
            elapsed = (frame_count + 1) / float(fps_video)
            total = total_frames / float(fps_video)
            remaining = max(0.0, total - elapsed)

            e_m, e_s = divmod(int(elapsed), 60)
            t_m, t_s = divmod(int(total), 60)
            r_m, r_s = divmod(int(remaining), 60)

            time_str = f"{e_m:02d}:{e_s:02d}/{t_m:02d}:{t_s:02d}"
            eta_str = f"{r_m:02d}:{r_s:02d}"
        else:
            elapsed = int(now - start_time)
            e_m, e_s = divmod(elapsed, 60)
            time_str = f"{e_m:02d}:{e_s:02d}"

        return fps_smooth, time_str, now, eta_str

    def format_time_fps(
        self,
        frame_count,
        prev_time,
        start_time,
        fps_video=None,
        total_frames=None,
        source_type="video",
        source_idx=None,
    ):
        if source_idx is None:
            source_idx = 0

        fps_smooth, time_str, now, eta_str = self._format_time_str(
            frame_count=frame_count,
            prev_time=prev_time,
            start_time=start_time,
            fps_video=fps_video,
            total_frames=total_frames,
            source_type=source_type,
            source_idx=source_idx,
        )
        return fps_smooth, time_str, now, eta_str

    # ------------- REDRAW -------------
    def _group_sources_by_model(self):
        """
        Returns list of tuples: [(model_name, [src_dicts...]), ...]
        Preserves discovery order (stable).
        """
        order = []
        buckets = {}
        for src in self.sources:
            m = src.get("model_name")
            if not m and src.get("name"):
                m2, short = self._extract_model_and_short(src["name"])
                if m2 and not src.get("model_name"):
                    src["model_name"] = m2
                if short and not src.get("short_name"):
                    src["short_name"] = short
                m = src.get("model_name")

            m = m or "unknown"
            if m not in buckets:
                buckets[m] = []
                order.append(m)
            buckets[m].append(src)
        return [(m, buckets[m]) for m in order]

    def _redraw_locked(self):
        width, _ = self._get_term_size()

        print("\033[3J", end="")
        clear_terminal()
        print("\033[H", end="")

        print(fmt_bold("YOLO4r Detection"))
        print("-" * width)
        print()

        grouped = self._group_sources_by_model()

        for gi, (model_name, srcs) in enumerate(grouped):
            # model header
            print(fmt_model(model_name))
            print()

            for src in srcs:
                # prefer short name in UI section
                display = src.get("short_name")
                if not display:
                    _, display = self._extract_model_and_short(src.get("name") or "")
                display = display or "source"

                name_fmt = fmt_source(display)

                if src["completed"]:
                    header = (
                        f"{name_fmt}: "
                        f"{fmt_label('Frames')}: -- | "
                        f"{fmt_label('FPS')}: -- | "
                        f"{fmt_label('Time')}: -- | "
                        f"{fmt_label('ETA')}: --"
                    )
                else:
                    eta_display = src.get("eta", "--")
                    show_eta = (src.get("source_type") == "video")

                    if show_eta:
                        header = (
                            f"{name_fmt}: "
                            f"{fmt_label('Frames')}: {src['frame_count']} | "
                            f"{fmt_label('FPS')}: {src['fps']:.1f} | "
                            f"{fmt_label('Time')}: {src['time_str']} | "
                            f"{fmt_label('ETA')}: {WHITE}{eta_display}{RESET}"
                        )
                    else:
                        header = (
                            f"{name_fmt}: "
                            f"{fmt_label('Frames')}: {src['frame_count']} | "
                            f"{fmt_label('FPS')}: {src['fps']:.1f} | "
                            f"{fmt_label('Time')}: {src['time_str']}"
                        )

                print(header)

                for ln in self._format_class_lines(src["counts"], width, classes_list=src.get("classes")):
                    print(ln)
                print()

            # divider between models
            print("-" * width)
            print()

        # logs region
        for ln in self.log_lines[-self.max_logs:]:
            print(ln[:width])

        print("", flush=True)

    def _maybe_redraw(self):
        if self.freeze_ui or self.in_shutdown:
            return
        with self.lock:
            now = time.time()
            if now - self.last_redraw_time < self.redraw_interval:
                return
            self.last_redraw_time = now
            self._redraw_locked()

    # ------------- DETECTION UPDATE API -------------
    def update_frame_status(
        self, idx, display_name, frame_count, fps_smooth, counts, time_str, eta=None
    ):
        i = idx - 1
        if i < 0 or i >= self.total_sources:
            return

        with self.lock:
            src = self.sources[i]
            src["name"] = display_name
            m, short = self._extract_model_and_short(display_name)
            if m and not src.get("model_name"):
                src["model_name"] = m
            if short and not src.get("short_name"):
                src["short_name"] = short

            src["frame_count"] = frame_count
            src["fps"] = fps_smooth
            src["time_str"] = time_str
            src["counts"] = dict(counts)
            if eta is not None:
                src["eta"] = eta

            if src.get("source_type") is None:
                low = (display_name or "").lower()
                src["source_type"] = "usb" if "| usb" in low or low.startswith("usb") else "video"

        self._maybe_redraw()

    # ------------- SOURCE COMPLETION -------------
    def mark_source_complete(self, idx):
        i = idx - 1
        if i < 0 or i >= self.total_sources:
            return

        with self.lock:
            src = self.sources[i]
            src["completed"] = True
            src["frame_count"] = "--"
            src["fps"] = "--"
            src["time_str"] = "--"
            src["eta"] = "--"

            ordered_classes = src.get("classes") or (list(self.all_classes) if self.all_classes else [])
            src["counts"] = {cls: "--" for cls in ordered_classes}

        # keep full name in log line
        self.info(f"Source '{fmt_bold(src['name'] or 'unknown')}' completed.")
        self._redraw_locked()

    # ------------- ERROR HELPERS -------------
    def open_capture_fail(self, src):
        self.error(f"Could not open source: {fmt_path(src)}")

    def read_frame_fail(self, src):
        self.error(f"Could not read frame from {fmt_path(src)}")

    def inference_fail(self, src, e):
        self.error(f"Inference failed for {fmt_path(src)}: {e}")

    # ------------- SAVE BLOCKS -------------
    def add_final_save_block(self, title, base_dir: Path, files: list, model_name: str | None = None):
        base_dir = Path(base_dir)
        try:
            idx = base_dir.parts.index("measurements")
            short = Path(*base_dir.parts[idx:])
        except ValueError:
            short = base_dir

        block = []
        block.append(fmt_save(f"{fmt_bold(title)}"))
        block.append(fmt_save(f"Saved to: {fmt_path(short)}"))

        for f in files:
            name = Path(f).name
            block.append(f"      - {name}")

        key = model_name or "unknown"
        if key not in self.final_save_blocks_by_model:
            self.final_save_blocks_by_model[key] = []
        self.final_save_blocks_by_model[key].append(block)

    # ------------- FINAL EXIT BLOCK -------------
    def render_final_exit_block(self):
        width, _ = self._get_term_size()
        print("\n" + "-" * width + "\n")

        # exit lines
        for line in self.final_exit_events:
            print(fmt_exit(line))
        print()

        # divider between exit lines and save sections
        print("-" * width)
        print()

        # grouped saves by model
        for model_name, blocks in self.final_save_blocks_by_model.items():
            print(fmt_model(model_name))
            print()

            for block in blocks:
                for ln in block:
                    print(ln)
                print()

            print("-" * width)
            print()

        print(fmt_exit("All detection threads safely terminated.") + "\n")

    # ------------- STOP SIGNAL -------------
    def stop_signal_received(self, single_thread=True):
        msg = (
            "Stop signal received. Terminating pipeline..."
            if single_thread
            else "Stop signal received. Terminating pipelines..."
        )
        self.final_exit_events.append(msg)
        self.final_exit_events.append("Saving CSV spreadsheets...")
        self.in_shutdown = True

    def all_threads_terminated(self):
        self.freeze_ui = False
        self.render_final_exit_block()

    # ------------- FALLBACK UNION CLASSES (kept for safety) -------------
    def classes_loaded(self, classes_list):
        """
        Old behavior (union). Still supported but NOT preferred for multi-model UI.
        """
        if classes_list is None:
            return
        self.all_classes = list(classes_list)

    # ------------- MODEL SELECTION (unchanged) -------------
    def prompt_model_selection(self, runs_dir, exclude_test=False):
        runs_dir = Path(runs_dir)
        dirs = sorted(
            [
                d
                for d in runs_dir.iterdir()
                if d.is_dir() and (not exclude_test or d.name.lower() != "test")
            ],
            reverse=True,
        )

        if not dirs:
            self.missing_weights(runs_dir)
            return None

        self.freeze_ui = True
        self.info(f"{len(dirs)} models found:")

        print("\n" + fmt_bold("Available models") + ":")
        for i, d in enumerate(dirs, 1):
            print(f"   {fmt_bold(i)}. {d.name}")
        print()

        try:
            while True:
                try:
                    ch = input(f"Select model (1-{len(dirs)}) or Ctrl+C: ").strip()
                except KeyboardInterrupt:
                    print("\n" + fmt_exit("Model selection cancelled") + "\n")
                    return None

                if ch.isdigit():
                    ch = int(ch)
                    if 1 <= ch <= len(dirs):
                        return dirs[ch - 1]

                self.warn("Invalid selection.")
        finally:
            self.freeze_ui = False
            self._maybe_redraw()


# ------------- SHARED INSTANCE FOR TRAINING -------------
console = Console(total_sources=0)
