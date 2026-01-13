# utils/detect/class_config.py
import yaml
from dataclasses import dataclass
from pathlib import Path
from ultralytics import YOLO

from ..paths import get_model_config_dir


@dataclass
class ClassConfig:
    """
    Per-model class configuration. This replaces global FOCUS_CLASSES / CONTEXT_CLASSES.
    """
    model_name: str
    config_path: Path
    focus: list
    context: list

    @property
    def all_classes(self):
        return list(self.focus) + list(self.context)

    def save(self, printer=None):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "FOCUS_CLASSES": list(self.focus),
            "CONTEXT_CLASSES": list(self.context),
        }
        with open(self.config_path, "w") as f:
            yaml.safe_dump(data, f, sort_keys=False)

        if printer:
            self._printer_save_msg(printer)

    def _printer_save_msg(self, printer):
        # Clean saved path for message: configs/<model>/classes_config.yaml
        # (matches your existing UX)
        try:
            model_dir = get_model_config_dir(self.model_name)
            short_path = f"configs/{model_dir.name}/classes_config.yaml"
        except Exception:
            short_path = str(self.config_path)
        printer.info(f"Class configuration saved to: {short_path}")

    @property
    def display_classes(self):
        """
        What the UI should display.
        """
        out = list(self.focus)
        if self.context:
            out.append("OBJECTS")
        return out

def _model_config_path(model_name: str) -> Path:
    """Return /configs/<model>/classes_config.yaml"""
    model_dir = get_model_config_dir(model_name)
    return model_dir / "classes_config.yaml"


def _load_yaml_config(path: Path, printer=None, model_name: str = None):
    if not path.exists():
        return None

    try:
        with open(path, "r") as f:
            saved = yaml.safe_load(f) or {}

        if not isinstance(saved, dict):
            raise ValueError("Invalid format for mapping classes.")

        focus = saved.get("FOCUS_CLASSES", []) or []
        context = saved.get("CONTEXT_CLASSES", []) or []

        # Ensure lists
        if not isinstance(focus, list):
            focus = []
        if not isinstance(context, list):
            context = []

        return {"focus": focus, "context": context}

    except Exception:
        # Clean error message (same spirit as your current code)
        if printer and model_name:
            printer.error(f"Class config YAML is corrupted for model '{model_name}'.")
        elif printer:
            printer.error("Class config YAML is corrupted.")
        return None


def _detect_classes_from_weights(weights_path: Path, printer=None):
    detected = []
    try:
        mdl = YOLO(str(weights_path))
        names_dict = mdl.names or {}
        detected = [names_dict[i] for i in sorted(names_dict.keys())]
    except Exception as e:
        if printer:
            printer.error(f"Failed to load classes: {e}")
        detected = []
    return detected

def load_or_create_classes(
    model_name: str,
    weights_path: str | Path,
    force_reload: bool = False,
    printer=None,
) -> ClassConfig:
    """
    Public entrypoint:
    - If YAML exists and is valid -> load it.
    - Otherwise -> regenerate from YOLO(weights).names, set focus to detected classes and context empty, then save.
    - Returns a ClassConfig object every time.
    """
    model_name = str(model_name).strip()
    weights_path = Path(weights_path)

    cfg_path = _model_config_path(model_name)

    # ----- Load existing YAML -----
    if (not force_reload) and cfg_path.exists():
        loaded = _load_yaml_config(cfg_path, printer=printer, model_name=model_name)
        if loaded is not None:
            cc = ClassConfig(
                model_name=model_name,
                config_path=cfg_path,
                focus=loaded["focus"],
                context=loaded["context"],
            )
            if printer:
                printer.info(f"Loaded {len(cc.all_classes)} classes: {cc.all_classes}")
            return cc

        if printer:
            printer.warn("Class config YAML is invalid or unreadable. Regenerating...")

    # ----- Regenerate from weights -----
    detected_classes = _detect_classes_from_weights(weights_path, printer=printer)

    cc = ClassConfig(
        model_name=model_name,
        config_path=cfg_path,
        focus=detected_classes,
        context=[],
    )

    # Save YAML
    cc.save(printer=printer)

    if printer:
        printer.info(
            f"Generated class config YAML with {len(detected_classes)} classes: {detected_classes}"
        )

    return cc
