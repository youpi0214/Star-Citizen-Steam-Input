#!/usr/bin/env python3

from __future__ import annotations

import argparse
import copy
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

    # Allow one template to render different modes by rewriting data-bind prefixes.
    for element in root.iter():
        binding = element.attrib.get("data-bind")
        if not binding:
            continue

        effective_binding = binding.replace("modes.fps.", f"modes.{mode}.", 1)
        try:
            value = get_by_path(mappings, effective_binding)
        except KeyError:
            # Keep the template text visible when a field does not exist yet.
            continue

        element.text = str(value)

    # Update mode label if present.
    for element in root.iter():
        if element.attrib.get("id") == "mode_name":
            try:
                element.text = str(get_by_path(mappings, f"modes.{mode}.name"))
            except KeyError:
                element.text = mode.title()
            break

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Star Citizen controller mapping SVG from YAML data.")
    parser.add_argument("--mode", choices=("fps", "flight"), required=True)
    parser.add_argument("--data", type=Path, default=Path("data/mappings.yaml"))
    parser.add_argument("--template", type=Path, default=Path("templates/steam-controller-2026.svg"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    output = args.output or Path(f"output/{args.mode}.svg")
    render(args.template, args.data, output, args.mode)
    print(f"Rendered {output}")


if __name__ == "__main__":
    main()
