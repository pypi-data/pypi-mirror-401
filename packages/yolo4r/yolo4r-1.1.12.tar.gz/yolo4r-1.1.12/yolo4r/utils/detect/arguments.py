# utils/detect/arguments.py
import argparse
import sys

from ..help_text import print_detect_help


def _normalize_models(raw_args):
    """
    Extract models from:
      --model X (repeatable)
      --models A B C (space-separated list)
      model=X / m=X
      models=a,b,c
    and return (args_without_models, models_list)
    """
    args_out = []
    models = []

    i = 0
    while i < len(raw_args):
        a = raw_args[i]

        # --model / -m X (repeatable)
        if a in ("--model", "-m"):
            if i + 1 < len(raw_args) and not raw_args[i + 1].startswith("--"):
                models.append(raw_args[i + 1])
                i += 2
                continue
            args_out.append(a)
            i += 1
            continue

        # --models A B C  (consume until next flag)
        if a == "--models":
            j = i + 1
            while j < len(raw_args):
                nxt = raw_args[j]
                if nxt.startswith("--"):
                    break
                # stop if we hit key=value (so sources=... doesn't get eaten)
                if "=" in nxt:
                    break
                models.append(nxt)
                j += 1
            i = j
            continue

        # key=value forms
        if "=" in a:
            k, v = a.split("=", 1)
            kl = k.lower().strip()

            if kl in ("model", "m"):
                if v.strip():
                    models.append(v.strip())
                i += 1
                continue

            if kl == "models":
                parts = [p.strip() for p in v.split(",") if p.strip()]
                models.extend(parts)
                i += 1
                continue

        args_out.append(a)
        i += 1

    return args_out, models

def _inject_sources_if_needed(args_list):
    """
    Allow:
      yolo4r detect video.mp4 usb0
    to be interpreted as:
      yolo4r detect --sources video.mp4 usb0

    If user already provided --sources, do nothing.
    If args contain only positionals (no --flags), inject --sources at the front.
    If mix of flags and positionals, inject --sources before the first positional
    that isn't a value for a known flag.
    """
    if not args_list:
        return args_list

    if "--sources" in args_list:
        return args_list

    # If there are no flags at all, treat everything as sources
    if not any(a.startswith("--") for a in args_list):
        return ["--sources"] + args_list

    # Otherwise, scan and inject --sources before first "free" positional
    new = []
    i = 0
    while i < len(args_list):
        a = args_list[i]

        # known flags with values (ONLY those handled here)
        if a in ("--model", "-m"):
            new.append(a)
            if i + 1 < len(args_list):
                new.append(args_list[i + 1])
                i += 2
            else:
                i += 1
            continue

        if a == "--test":
            new.append(a)
            i += 1
            continue

        if a.startswith("--"):
            new.append(a)
            i += 1
            continue

        # first free positional -> sources start here
        new.append("--sources")
        new.extend(args_list[i:])
        break

    return new


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run object detection on video inputs and/or camera sources.",
        add_help=False,
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Use your test model directory...",
    )

    # sources can be omitted; we'll default to usb0
    parser.add_argument(
        "--sources",
        nargs="*",
        help="One or more camera/video sources",
    )

    # MULTI-MODEL:
    # repeatable: --model A --model B
    # also works with cli.py expansion for models=a,b
    parser.add_argument(
        "--model",
        "-m",
        action="append",
        default=[],
        help=(
            "Select one or more models. Repeatable.\n"
            "Examples:\n"
            "  --model sparrow-v2 --model yolo11n\n"
            "  model=sparrow-v2 model=yolo11n\n"
            "  models=sparrow-v2,yolo11n"
        ),
    )

    parser.add_argument(
        "--models",
        nargs="*",
        help="Alias for providing multiple models: --models A B C (same as repeating --model).",
    )

    # ---- Custom help routing ----
    raw_args = sys.argv[1:]
    if any(a in ("--help", "-h", "help") for a in raw_args):
        print_detect_help()
        sys.exit(0)

    # ---- Normalize model/model(s) key=value forms into a clean model list ----
    raw_wo_models, models = _normalize_models(raw_args)

    # ---- Inject --sources when appropriate ----
    final_argv = _inject_sources_if_needed(raw_wo_models)

    # ---- Parse everything else ----
    args = parser.parse_args(final_argv)

    # ---- Merge models collected from key=value with argparse-collected repeats ----
    merged_models = []
    merged_models.extend(args.model or [])
    merged_models.extend(getattr(args, "models", []) or [])
    merged_models.extend(models)

    # de-dupe while preserving order
    seen = set()
    deduped = []
    for m in merged_models:
        m = str(m).strip()
        if not m:
            continue
        if m not in seen:
            seen.add(m)
            deduped.append(m)

    args.model = deduped

    # default sources
    if not args.sources:
        args.sources = ["usb0"]

    return args
