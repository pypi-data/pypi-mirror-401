# cli.py
import argparse
import sys


def print_global_help():
    print(
        """
YOLO4R - You Only Look Once for Research
==============================================

Available Commands:
  yolo4r train      Train, update, or resume a YOLO model.
  yolo4r detect     Run YOLO detection on one or more video/camera sources.
  yolo4r version    Show the YOLO4r version.
  yolo4r help       Show this help menu.

----------------------------------------------

Command Specific Help:
  yolo4r train help
  yolo4r detect help

----------------------------------------------

Examples:
  yolo4r train model=yolo11n architecture=custom_arch dataset=birds
  yolo4r train architecture=yolo12
  yolo4r train model=yolov8x name="best run ever!!" test

  # detect (single model)
  yolo4r detect model=sparrow-v2 sources=usb0 usb1
  yolo4r detect test trailcam.mp4 trailcam2.mov

  # detect (multi-model)
  yolo4r detect model=sparrow-v2 model=yolo11n sources=usb0
  yolo4r detect models=sparrow-v2,yolo11n usb0

YOLO4r Documentation & Support:
  https://github.com/kgoertle/yolo4r
"""
    )

def expand_key_value_args(argv):
    """
    Expands friendly CLI forms into argparse-friendly flags.

    Supports:
      model=..., weights=...              -> --model <value> (repeatable)
      models=a,b,c                        -> repeat --model a --model b --model c
      models=yolo11n yolov8-obb           -> --models yolo11n yolov8-obb
      sources=video.mp4 usb0              -> --sources video.mp4 usb0
      test / test=true                    -> --test
    """
    expanded = []

    mappings = {
        # naming (train)
        "name": "--name",
        "run": "--name",
        "run_name": "--name",

        # models (detect/train)
        "model": "--model",
        "weights": "--model",

        # train
        "update": "--update",
        "arch": "--arch",
        "architecture": "--arch",
        "backbone": "--arch",
        "data": "--dataset",
        "dataset": "--dataset",
        "labelstudio": "--labelstudio",
        "project": "--labelstudio",

        # detect
        "sources": "--sources",
        "source": "--sources",

        # shared
        "test": "--test",
    }

    boolean_true = {"1", "true", "yes", "on", ""}

    collecting_models = False
    collecting_sources = False

    for arg in argv:
        low = arg.lower()

        # stop collection if user explicitly starts a flag
        if arg.startswith("--"):
            collecting_models = False
            # if they started --sources, treat following positionals as sources (argparse will handle)
            if arg == "--sources":
                collecting_sources = True
            expanded.append(arg)
            continue

        # ---------- special case: plain "test" ----------
        if low == "test":
            expanded.append("--test")
            continue

        # ---------- key=value pattern ----------
        if "=" in arg:
            key, value = arg.split("=", 1)
            key = key.lower().strip()

            # entering a new key=value stops previous collection modes
            collecting_models = False
            collecting_sources = False

            # test=true / test=1 / test=
            if key == "test":
                if value.lower().strip() in boolean_true:
                    expanded.append("--test")
                continue

            # sources=...  (start sources mode)
            if key in ("sources", "source"):
                expanded.append("--sources")
                if value.strip():
                    expanded.append(value.strip())
                collecting_sources = True
                continue

            # models=... (comma or space form)
            if key == "models":
                # if comma-separated, expand to repeat --model
                if "," in value:
                    parts = [p.strip() for p in value.split(",") if p.strip()]
                    for p in parts:
                        expanded.append("--model")
                        expanded.append(p)
                    continue

                # space-separated: use --models + keep collecting additional bare args as models
                expanded.append("--models")
                if value.strip():
                    expanded.append(value.strip())
                collecting_models = True
                continue

            # normal key=value
            if key in mappings:
                expanded.append(mappings[key])
                if value.strip():
                    expanded.append(value.strip())
                continue

        # ---------- collection modes ----------
        if collecting_models:
            # bare token following models=... is another model
            expanded.append(arg)
            continue

        if collecting_sources:
            # bare token following sources=... is another source
            expanded.append(arg)
            continue

        # default passthrough
        expanded.append(arg)

    return expanded

def main():
    parser = argparse.ArgumentParser(
        prog="yolo4r",
        description="You Only Look Once for Research",
        add_help=True,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---- TRAIN ----
    train_parser = subparsers.add_parser("train", help="Train or update a model.")
    train_parser.set_defaults(func="train")

    # ---- DETECT ----
    detect_parser = subparsers.add_parser("detect", help="Run YOLO detection.")
    detect_parser.set_defaults(func="detect")

    # ---- VERSION ----
    version_parser = subparsers.add_parser("version", help="Show YOLO4R version.")
    version_parser.set_defaults(func="version")

    # ---- HELP ----
    help_parser = subparsers.add_parser("help", help="Show all YOLO4R commands.")
    help_parser.set_defaults(func="help")

    # ---- Parse command (not sub-arguments) ----
    args, unknown = parser.parse_known_args()

    # Expand key=value into standard flags
    unknown = expand_key_value_args(unknown)

    # ROUTING
    if args.func == "train":
        if "--help" in unknown or "-h" in unknown or "help" in unknown:
            from .utils.help_text import print_train_help
            print_train_help()
            return

        from .train import main as train_main
        sys.argv = ["yolo4r-train"] + unknown
        return train_main()

    elif args.func == "detect":
        if "--help" in unknown or "-h" in unknown or "help" in unknown:
            from .utils.help_text import print_detect_help
            print_detect_help()
            return

        from .detect import main as detect_main
        sys.argv = ["yolo4r-detect"] + unknown
        return detect_main()

    elif args.func == "version":
        from .version import YOLO4R_VERSION
        print(f"YOLO4R {YOLO4R_VERSION}")
        return

    elif args.func == "help":
        return print_global_help()

    else:
        parser.print_help()
