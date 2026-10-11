#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

try:
    import yaml
except ImportError as exc:
    raise SystemExit("Missing dependency: PyYAML. Install with: pip install pyyaml") from exc


def get_by_path(data: dict, dotted_path: str):
    value = data
    for part in dotted_path.split("."):
        if not isinstance(value, dict) or part not in value:
            raise KeyError(dotted_path)
        value = value[part]
    return value


def render(template_path: Path, mappings_path: Path, output_path: Path, mode: str) -> None:
    mappings = yaml.safe_load(mappings_path.read_text(encoding="utf-8"))
    tree = ET.parse(template_path)
    root = tree.getroot()

    for element in root.iter():
        binding = element.attrib.get("data-bind")
        if not binding:
            continue

        effective_binding = binding.replace("modes.fps.", f"modes.{mode}.", 1)
        try:
            value = get_by_path(mappings, effective_binding)
        except KeyError:
            # Keep fallback template text visible while a binding is unresolved.
            continue

        element.text = str(value)

    for element in root.iter():
        if element.attrib.get("id") == "mode_name":
            try:
                element.text = str(get_by_path(mappings, f"modes.{mode}.name")).upper()
            except KeyError:
                element.text = mode.upper()
            break

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


def resolve_template(mode: str, explicit_template: Path | None) -> Path:
    if explicit_template is not None:
        return explicit_template

    mode_template = Path(f"templates/steam-controller-2026-{mode}.svg")
    if mode_template.exists():
        return mode_template

    return Path("templates/steam-controller-2026.svg")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Star Citizen controller mapping SVG from YAML data.")
    parser.add_argument("--mode", choices=("fps", "flight"), required=True)
    parser.add_argument("--data", type=Path, default=Path("data/mappings.yaml"))
    parser.add_argument("--template", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    template = resolve_template(args.mode, args.template)
    output = args.output or Path(f"output/{args.mode}.svg")
    render(template, args.data, output, args.mode)
    print(f"Rendered {output} from {template}")


if __name__ == "__main__":
    main()
