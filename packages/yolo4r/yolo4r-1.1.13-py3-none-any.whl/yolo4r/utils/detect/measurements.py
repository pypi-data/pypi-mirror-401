# utils/detect/measurements.py
import csv
import math
import yaml
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from shapely.geometry import Polygon

from ..paths import MEASURE_CONFIG_YAML, CONFIGS_DIR


# -------------------- CONFIG --------------------
class MeasurementConfig:
    """Central configuration for all measurement parameters."""

    DEFAULTS = {
        "avg_group_size": 3,              # grouping for average_counts.csv
        "interval_sec": 5,                # interval for aggregator + counter snapshots + motion
        "session_sec": 10,                # session summary window size (seconds)
        "interaction_timeout_sec": 2.0,   # gap before ending an interaction
        "overlap_threshold": 0.1,         # IoU threshold
        "motion_threshold_px": 10.0,      # min pixel movement to count motion
        "motion_min_frames": 3,           # min frames to confirm motion
    }

    def __init__(self, config_path=None):
        CONFIGS_DIR.mkdir(parents=True, exist_ok=True)
        self.config_path = Path(config_path) if config_path else MEASURE_CONFIG_YAML

        # If missing - create with defaults
        if not self.config_path.exists():
            with open(self.config_path, "w") as f:
                yaml.safe_dump(self.DEFAULTS, f, sort_keys=False)

        # Load config
        with open(self.config_path, "r") as f:
            data = yaml.safe_load(f) or {}

        # Apply defaults if missing
        for k, v in self.DEFAULTS.items():
            setattr(self, k, data.get(k, v))


# -------------------- INTERVAL CLOCK --------------------
class IntervalClock:
    """
    Grid-aligned interval clock (no drift).
    - All rollovers are aligned to: anchor + k*interval_sec
    - Each consumer can track its own current interval start, but the mapping
      from ts->interval_start is identical everywhere.
    """
    def __init__(self, interval_sec: float, anchor_ts: datetime | None = None):
        self.interval_sec = float(interval_sec)
        self.anchor_ts = anchor_ts  # usually video start_time

    def interval_start(self, ts: datetime) -> datetime:
        if self.anchor_ts is None:
            # anchor at first timestamp seen
            self.anchor_ts = ts
            return ts

        dt = (ts - self.anchor_ts).total_seconds()
        k = int(dt // self.interval_sec)
        return self.anchor_ts + timedelta(seconds=k * self.interval_sec)

    def tick(self, ts: datetime, current_start: datetime | None):
        """
        Args:
          ts: current timestamp
          current_start: the caller's current interval start (or None)

        Returns:
          (rolled: bool, new_start: datetime, old_start: datetime|None)

        Notes:
          - Caller stores new_start as its current_start
          - This clock object itself does NOT store per-consumer state
        """
        new_start = self.interval_start(ts)
        if current_start is None:
            return False, new_start, None
        if new_start != current_start:
            return True, new_start, current_start
        return False, current_start, None

# -------------------- COUNTING UTILITIES --------------------
def add_ratio_to_counts(counts: dict, focus_classes: list, context_classes: list):
    """
    Add human-readable ratios only when context classes are enabled
    (keeps your existing behavior).
    """
    if not context_classes:
        return counts

    focus_values = [int(counts.get(cls, 0)) for cls in focus_classes]

    non_zero = [v for v in focus_values if v != 0]
    if len(non_zero) > 1:
        gcd_val = non_zero[0]
        for v in non_zero[1:]:
            gcd_val = math.gcd(gcd_val, v)
        if gcd_val > 1:
            focus_values = [v // gcd_val for v in focus_values]

    counts["RATIO"] = ":".join(str(v) for v in focus_values)
    return counts


def compute_counts_from_boxes(boxes_list, names, focus_classes=None, context_classes=None):
    focus_classes = list(focus_classes or [])
    context_classes = set(context_classes or [])

    counts = {c: 0 for c in focus_classes}
    if context_classes:
        counts["OBJECTS"] = 0

    for b in boxes_list:
        cls_id = b[5]
        cls_name = names.get(cls_id)

        if cls_name in counts:                  # focus
            counts[cls_name] += 1
        elif context_classes and cls_name in context_classes:
            counts["OBJECTS"] += 1              # context means OBJECTS only

    return add_ratio_to_counts(counts, focus_classes, context_classes)

# -------------------- COUNTER --------------------
class Counter:
    """
    Snapshot counts at interval rollovers, plus grouped averages.
    """

    def __init__(self, out_folder=None, config=None, start_time=None, class_config=None, focus_classes=None, context_classes=None):
        self.out_folder = Path(out_folder) if out_folder else None
        self.config = config or MeasurementConfig()
        self.start_time = start_time

        # Per-model classes
        if class_config is not None:
            self.focus_classes = list(getattr(class_config, "focus", []))
            self.context_classes = list(getattr(class_config, "context", []))

        self.clock = IntervalClock(self.config.interval_sec, anchor_ts=self.start_time)
        self._interval_start = None
        self.snapshot_buffer = []
        self.creation_ref = None
        self.group_number = 1

    def update_counts(self, boxes, names, timestamp=None):
        now = timestamp or datetime.now()

        # ---- Interval Rollover ----
        rolled, new_start, old_start = self.clock.tick(now, self._interval_start)
        self._interval_start = new_start
        if not rolled:
            return
        boundary = old_start

        counts = compute_counts_from_boxes(
            boxes, names,
            focus_classes=self.focus_classes,
            context_classes=self.context_classes,
        )

        # Convert system timestamp to video timestamp
        if self.start_time:
            if not self.creation_ref:
                self.creation_ref = boundary
            elapsed = (boundary - self.creation_ref).total_seconds()
            video_ts = self.start_time + timedelta(seconds=elapsed)
        else:
            video_ts = boundary

        self.snapshot_buffer.append((video_ts, counts))

    def _compute_averages(self):
        if not self.snapshot_buffer:
            return []

        group_size = int(self.config.avg_group_size) or 1
        averages = []

        for i in range(0, len(self.snapshot_buffer), group_size):
            block = self.snapshot_buffer[i : i + group_size]

            summed = defaultdict(float)
            for _, c in block:
                for cls, val in c.items():
                    if cls != "RATIO":
                        summed[cls] += float(val)

            divisor = len(block)
            avg_counts = {cls: summed[cls] / divisor for cls in summed}
            avg_counts = add_ratio_to_counts(avg_counts, self.focus_classes, self.context_classes)

            midpoint = block[0][0] + (block[-1][0] - block[0][0]) / 2
            averages.append(
                {
                    "Group": self.group_number,
                    "Time": midpoint.strftime("%H:%M:%S"),
                    "Counts": avg_counts,
                }
            )
            self.group_number += 1

        return averages

    def save_results(self):
        """Save counts.csv and average_counts.csv."""
        if not self.out_folder:
            return None

        self.out_folder.mkdir(parents=True, exist_ok=True)
        saved = []

        all_cols = (
            self.focus_classes
            + (["OBJECTS"] if self.context_classes else [])
            + (["RATIO"] if self.context_classes else [])
        )

        # SNAPSHOT CSV
        f_snap = self.out_folder / "counts.csv"
        with open(f_snap, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["TIME"] + all_cols)
            for ts, c in self.snapshot_buffer:
                row = [ts.strftime("%H:%M:%S")] + [c.get(cls, "") for cls in all_cols]
                w.writerow(row)
        saved.append(f_snap)

        # AVERAGE CSV
        averages = self._compute_averages()
        if averages:
            f_avg = self.out_folder / "average_counts.csv"
            with open(f_avg, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["GROUP", "TIME"] + all_cols)
                for a in averages:
                    row = [a["Group"], a["Time"]] + [a["Counts"].get(cls, "") for cls in all_cols]
                    w.writerow(row)
            saved.append(f_avg)

        return saved


# -------------------- INTERACTIONS --------------------
class Interactions:
    def __init__(self, out_folder=None, config=None, start_time=None, is_obb=False, class_config=None, focus_classes=None, context_classes=None):
        self.out_folder = Path(out_folder) if out_folder else None
        self.config = config or MeasurementConfig()
        self.start_time = start_time
        self.is_obb = is_obb

        if class_config is not None:
            self.focus_classes = list(getattr(class_config, "focus", []))
            self.context_classes = list(getattr(class_config, "context", []))

        self.active = {}
        self.records = []
        self.clock = IntervalClock(self.config.interval_sec, anchor_ts=self.start_time)
        self._interval_start = None
        self.ref_time = None

    def _normalize(self, dt):
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)

    def _video_time(self, ts):
        if not self.start_time or not self.ref_time:
            return ts
        delta = (self._normalize(ts) - self._normalize(self.ref_time)).total_seconds()
        return self.start_time + timedelta(seconds=delta)

    def _obb_to_polygon(self, box):
        x1, y1, x2, y2 = box[:4]
        return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

    def _iou_polygon(self, boxA, boxB):
        polyA = Polygon(self._obb_to_polygon(boxA))
        polyB = Polygon(self._obb_to_polygon(boxB))
        if not polyA.is_valid or not polyB.is_valid:
            return 0.0
        inter = polyA.intersection(polyB).area
        if inter <= 0:
            return 0.0
        union = polyA.area + polyB.area - inter
        if union <= 0:
            return 0.0
        return inter / union

    def _iou_aabb(self, a, b):
        ax1, ay1, ax2, ay2 = a[:4]
        bx1, by1, bx2, by2 = b[:4]

        iw = max(0, min(ax2, bx2) - max(ax1, bx1))
        ih = max(0, min(ay2, by2) - max(ay1, by1))
        if iw == 0 or ih == 0:
            return 0.0

        inter = iw * ih
        union = (ax2 - ax1) * (ay2 - ay1) + (bx2 - bx1) * (by2 - by1) - inter
        if union <= 0:
            return 0.0

        return inter / union

    def _overlap(self, a, b, threshold):
        if self.is_obb:
            return self._iou_polygon(a, b) > threshold
        return self._iou_aabb(a, b) > threshold

    def process_frame(self, boxes, names, ts):
        
        if self.ref_time is None:
            interval_start = self.clock.interval_start(ts)
            self.ref_time = interval_start
        
        if not self.ref_time:
            self.ref_time = ts

        video_ts = self._video_time(ts)

        birds = [b for b in boxes if names.get(b[5]) in self.focus_classes]
        objs = [b for b in boxes if self.context_classes and names.get(b[5]) in self.context_classes]

        active_now = set()

        if self.context_classes:
            # focus-to-context interactions
            for b in birds:
                name_b = names.get(b[5])
                for o in objs:
                    name_o = names.get(o[5])
                    if b is o:
                        continue
                    if self._overlap(b, o, self.config.overlap_threshold):
                        pair = (name_b, name_o)
                        active_now.add(pair)
                        self._activate(pair, video_ts)
        else:
            # focus-to-focus interactions
            for i, b1 in enumerate(birds):
                for j in range(i + 1, len(birds)):
                    b2 = birds[j]
                    name1, name2 = names.get(b1[5]), names.get(b2[5])
                    if name1 == name2:
                        continue
                    if self._overlap(b1, b2, self.config.overlap_threshold):
                        pair = tuple(sorted((name1, name2)))
                        active_now.add(pair)
                        self._activate(pair, video_ts)

        self._finalize_inactive(active_now, video_ts)

    def _activate(self, pair, ts):
        if pair not in self.active:
            self.active[pair] = {"start": ts, "last": ts}
        else:
            self.active[pair]["last"] = ts

    def _finalize_inactive(self, active_now, ts):
        ended = []
        for pair, info in list(self.active.items()):
            if (
                pair not in active_now
                and (ts - info["last"]).total_seconds() >= float(self.config.interaction_timeout_sec)
            ):
                self._record(pair, info["start"], info["last"])
                ended.append(pair)
        for p in ended:
            del self.active[p]

    def finalize(self):
        for pair, info in list(self.active.items()):
            self._record(pair, info["start"], info["last"])
        self.active.clear()
        return self.records

    def _record(self, pair, start, end):
        dur = round((end - start).total_seconds(), 2)
        if dur <= 0:
            return

        if self.context_classes:
            row = {
                "TIME0": start.strftime("%H:%M:%S"),
                "TIME1": end.strftime("%H:%M:%S"),
                "FOCUS": pair[0],
                "CONTEXT": pair[1],
                "DURATION": dur,
            }
        else:
            row = {
                "TIME0": start.strftime("%H:%M:%S"),
                "TIME1": end.strftime("%H:%M:%S"),
                "CLASS1": pair[0],
                "CLASS2": pair[1],
                "DURATION": dur,
            }

        self.records.append(row)

    def save_results(self):
        if not self.records or not self.out_folder:
            return None

        self.out_folder.mkdir(parents=True, exist_ok=True)
        out_file = self.out_folder / "interactions.csv"

        headers = ["TIME0", "TIME1", "FOCUS", "CONTEXT", "DURATION"] if self.context_classes else ["TIME0", "TIME1", "CLASS1", "CLASS2", "DURATION"]

        with open(out_file, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=headers)
            w.writeheader()
            for r in sorted(self.records, key=lambda x: x["TIME0"]):
                w.writerow(r)

        return out_file


# -------------------- AGGREGATOR --------------------
class Aggregator:
    """
    Frame-level accumulation -> interval rollups -> session summary.

    Multi-model safe: uses per-instance focus/context classes.
    """
    def __init__(self, out_folder, config=None, start_time=None, class_config=None):
        self.out_folder = Path(out_folder)
        self.config = config or MeasurementConfig()
        self.start_time = start_time

        if class_config is None:
            raise ValueError("class_config is required (legacy global classes removed).")

        self.focus_classes = list(getattr(class_config, "focus", []))
        self.context_classes = list(getattr(class_config, "context", []))

        self.clock = IntervalClock(self.config.interval_sec, anchor_ts=self.start_time)
        self._interval_start = None
        self._interval_sums = defaultdict(float)
        self._interval_frames = 0

        self.intervals = []   # finalized intervals
        self.frame_data = [] 

    def push_frame_data(self, timestamp, current_boxes_list=None, names=None, counts_dict=None):
        if counts_dict is None and current_boxes_list is not None and names is not None:
            counts_dict = compute_counts_from_boxes(
                current_boxes_list, names,
                focus_classes=self.focus_classes,
                context_classes=self.context_classes,
            )

        counts_dict = dict(counts_dict or {})
        counts_dict.pop("RATIO", None)

        self.frame_data.append((timestamp, counts_dict))

        rolled, new_start, old_start = self.clock.tick(timestamp, self._interval_start)
        if self._interval_start is None:
            self._interval_start = new_start

        if rolled and old_start is not None:
            self.intervals.append(self._finalize_interval(old_start, dict(self._interval_sums)))
            self._interval_sums.clear()
            self._interval_frames = 0
            self._interval_start = new_start

        for cls, val in counts_dict.items():
            self._interval_sums[cls] += float(val)
        self._interval_frames += 1

    def finalize(self):
        """Flush the last partial interval (call on shutdown)."""
        if self._interval_frames > 0 and self._interval_start is not None:
            self.intervals.append(self._finalize_interval(self._interval_start, dict(self._interval_sums)))
            self._interval_sums.clear()
            self._interval_frames = 0

    def _finalize_interval(self, start_ts, summed: dict):
        summed = add_ratio_to_counts(summed, self.focus_classes, self.context_classes)
        midpoint = start_ts + timedelta(seconds=float(self.config.interval_sec) / 2.0)
        return {"TIME": midpoint.strftime("%H:%M:%S"), "Counts": summed}
    
    def save_interval_results(self):
        self.finalize()
        if not self.intervals:
            return None

        self.out_folder.mkdir(parents=True, exist_ok=True)
        out_file = self.out_folder / "frame_counts.csv"

        all_cols = (
            self.focus_classes
            + (["OBJECTS"] if self.context_classes else [])
            + (["RATIO"] if self.context_classes else [])
        )

        with open(out_file, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["TIME"] + all_cols)
            for iv in self.intervals:
                row = [iv["TIME"]] + [iv["Counts"].get(cls, "") for cls in all_cols]
                w.writerow(row)

        return out_file

    def save_session_summary(self):
        self.finalize()
        intervals = self.intervals
        if not intervals:
            return None

        interval_sec = float(getattr(self.config, "interval_sec", 1) or 1)
        session_sec = float(getattr(self.config, "session_sec", interval_sec) or interval_sec)
        intervals_per_session = max(1, int(round(session_sec / interval_sec)))

        session_totals = defaultdict(float)
        session_rates = defaultdict(list)

        for i in range(0, len(intervals), intervals_per_session):
            block = intervals[i : i + intervals_per_session]
            if not block:
                continue

            block_duration = max(1e-9, len(block) * interval_sec)

            block_totals = defaultdict(float)
            for iv in block:
                for cls, val in iv["Counts"].items():
                    if cls != "RATIO":
                        block_totals[cls] += float(val)

            for cls, total in block_totals.items():
                session_totals[cls] += total
                session_rates[cls].append(total / block_duration)

        if self.context_classes:
            obj_total = session_totals.pop("OBJECTS", 0.0)  # OBJECTS already collapsed above
            session_totals["OBJECTS"] = obj_total
            # rates for OBJECTS already exist in "OBJECTS" key if present; if not, keep safe:
            session_rates.setdefault("OBJECTS", [])

        focus_total = sum(session_totals.get(cls, 0.0) for cls in self.focus_classes) or 1.0

        summary_rows = []
        for cls, total in session_totals.items():
            rates = session_rates.get(cls, [])
            mean_rate = sum(rates) / len(rates) if rates else 0.0
            std_dev = math.sqrt(sum((r - mean_rate) ** 2 for r in rates) / len(rates)) if rates else 0.0
            prop = (total / focus_total) if cls in self.focus_classes else "n/a"

            summary_rows.append(
                {
                    "CLASS": cls,
                    "TOTAL_COUNT": round(total, 3),
                    "AVG_RATE": round(mean_rate, 3),
                    "STD_DEV": round(std_dev, 3),
                    "PROP": prop if isinstance(prop, str) else round(prop, 3),
                }
            )

        self.out_folder.mkdir(parents=True, exist_ok=True)
        out_file = self.out_folder / "session_summary.csv"
        with open(out_file, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["CLASS", "TOTAL_COUNT", "AVG_RATE", "STD_DEV", "PROP"])
            w.writeheader()
            for row in summary_rows:
                w.writerow(row)

        return out_file

# -------------------- MOTION --------------------
class Motion:
    """
    Interval-based, per-object motion analysis with jitter suppression.

    Motion is counted ONLY if:
    - displacement >= threshold
    - sustained for >= min_frames
    - counted once per object per interval
    """
    def __init__(self, paths, frame_width, frame_height, config=None, start_time=None, class_config=None):
        self.out_folder = Path(paths["motion"])
        self.config = config or MeasurementConfig()
        self.start_time = start_time

        if class_config is None:
            raise ValueError("`class_config` registration is required.")

        self.focus_classes = list(getattr(class_config, "focus", []))
        self.context_classes = list(getattr(class_config, "context", []))

        self.clock = IntervalClock(self.config.interval_sec, anchor_ts=self.start_time)
        self._interval_start = None

        self.motion_threshold_px = float(self.config.motion_threshold_px)
        self.min_frames = int(getattr(self.config, "motion_min_frames", 3))

        self.prev_centers = defaultdict(list)
        self.persist = defaultdict(lambda: defaultdict(int))
        self.locked = defaultdict(set)

        self.motion_events = defaultdict(int)
        self.interval_displacement = defaultdict(float)
        self.frames_with_motion = defaultdict(int)
        self.interval_frames = 0

        self.rows_counts = []
        self.rows_intensity = []
        self.rows_prevalence = []

    def _center(self, box):
        x1, y1, x2, y2 = box[:4]
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)

    def _dist(self, a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    @staticmethod
    def log_transform(x):
        return round(math.log1p(x), 3)

    def process_frame(self, boxes, names, ts):
        self.interval_frames += 1

        current = defaultdict(list)
        for b in boxes:
            cls = names.get(b[5])
            if cls in self.focus_classes:
                current[cls].append(self._center(b))

        for cls in self.focus_classes:
            curr = current.get(cls, [])
            prev = self.prev_centers.get(cls, [])

            if not curr or not prev:
                self.prev_centers[cls] = curr
                continue

            used_prev = set()

            for i, c in enumerate(curr):
                best_j = None
                best_d = None

                for j, p in enumerate(prev):
                    if j in used_prev:
                        continue
                    d = self._dist(c, p)
                    if best_d is None or d < best_d:
                        best_d = d
                        best_j = j

                if best_j is None:
                    continue

                used_prev.add(best_j)

                if best_d >= self.motion_threshold_px:
                    self.persist[cls][best_j] += 1
                else:
                    self.persist[cls][best_j] = 0

                if self.persist[cls][best_j] >= self.min_frames and best_j not in self.locked[cls]:
                    self.motion_events[cls] += 1
                    self.interval_displacement[cls] += best_d
                    self.frames_with_motion[cls] += 1
                    self.locked[cls].add(best_j)

            self.prev_centers[cls] = curr

        rolled, new_start, old_start = self.clock.tick(ts, self._interval_start)
        self._interval_start = new_start
        if rolled:
            self._finalize_interval(old_start)
            self._reset_interval()

    def _finalize_interval(self, ts):
        t = ts.strftime("%H:%M:%S")

        counts = add_ratio_to_counts(
            {cls: self.motion_events.get(cls, 0) for cls in self.focus_classes},
            self.focus_classes,
            self.context_classes,
        )

        intensity = {
            cls: self.log_transform(self.interval_displacement.get(cls, 0.0))
            for cls in self.focus_classes
        }

        prevalence = {
            cls: round(self.frames_with_motion.get(cls, 0) / max(self.interval_frames, 1), 3)
            for cls in self.focus_classes
        }

        self.rows_counts.append({"TIME": t, **counts})
        self.rows_intensity.append({"TIME": t, **intensity})
        self.rows_prevalence.append({"TIME": t, **prevalence})

    def _reset_interval(self):
        self.motion_events.clear()
        self.interval_displacement.clear()
        self.frames_with_motion.clear()
        self.persist.clear()
        self.locked.clear()
        self.interval_frames = 0

    def save_results(self):
        if not self.rows_counts:
            return None

        self.out_folder.mkdir(parents=True, exist_ok=True)
        outputs = []

        outputs.append(self._write("motion_counts.csv", self.rows_counts, include_ratio=True))
        outputs.append(self._write("motion_intensity.csv", self.rows_intensity))
        outputs.append(self._write("motion_prevalence.csv", self.rows_prevalence))

        return [p for p in outputs if p]

    def _write(self, name, rows, include_ratio=False):
        headers = ["TIME"] + self.focus_classes
        if include_ratio and self.context_classes:
            headers += ["RATIO"]

        out = self.out_folder / name
        with open(out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=headers)
            w.writeheader()
            for r in rows:
                w.writerow(r)
        return out
