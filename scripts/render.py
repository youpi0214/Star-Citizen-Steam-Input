
from __future__ import annotations

import argparse
import base64
import mimetypes
import shutil
import subprocess
import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET


def get_by_path(data: dict, dotted_path: str):
    value = data
    for part in dotted_path.split("."):
        if not isinstance(value, dict) or part not in value:
            raise KeyError(dotted_path)
        value = value[part]
    return value


def load_mappings(mappings_path: Path) -> dict | None:
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit("Missing dependency: PyYAML. Install with: pip install pyyaml") from exc
    return yaml.safe_load(mappings_path.read_text(encoding="utf-8"))


def apply_bindings(root: ET.Element, mappings: dict, mode: str) -> None:
    for element in root.iter():
        binding = element.get("data-bind")
        if not binding:
            continue
        effective_binding = binding.replace("modes.fps.", f"modes.{mode}.", 1)
        try:
            element.text = str(get_by_path(mappings, effective_binding))
        except KeyError:
            # Keep fallback template text visible while a binding is unresolved.
            continue


def update_mode_name(root: ET.Element, mappings: dict, mode: str) -> None:
    for element in root.iter():
        if element.get("id") == "mode_name":
            try:
                element.text = str(get_by_path(mappings, f"modes.{mode}.name")).upper()
            except KeyError:
                element.text = mode.upper()
            break


def image_data_uri(asset: Path) -> str:
    mime = mimetypes.guess_type(asset.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(asset.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def embed_images(root: ET.Element, template_path: Path) -> None:
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] != "image":
            continue
        for key in ("href", "{http://www.w3.org/1999/xlink}href"):
            href = element.get(key)
            if not href or href.startswith(("data:", "http:", "https:")):
                continue
            embedded = image_data_uri(template_path.parent / href)
            element.set(key, embedded)
            element.set("{http://www.w3.org/1999/xlink}href", embedded)


def convert_to_png(svg_path: Path, png_path: Path, width: int) -> None:
    renderer = shutil.which("rsvg-convert")
    if renderer is None:
        raise SystemExit("Missing dependency: rsvg-convert. Install librsvg to export raster images.")
    subprocess.run([
        renderer, "--format=png", f"--width={width}",
        "--background-color=white", "--output", str(png_path), str(svg_path),
    ], check=True)


def convert_to_jpeg(png_path: Path, output_path: Path) -> None:
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("Missing dependency: Pillow. Install with: pip install pillow") from exc
    with Image.open(png_path) as image:
        image.convert("RGB").save(output_path, quality=95, subsampling=0)


def export_raster(tree: ET.ElementTree, output_path: Path, width: int) -> None:
    with tempfile.TemporaryDirectory(prefix="controller-render-") as temporary:
        svg = Path(temporary) / "sheet.svg"
        png = Path(temporary) / "sheet.png"
        tree.write(svg, encoding="utf-8", xml_declaration=True)
        convert_to_png(svg, png, width)
        if output_path.suffix.lower() == ".png":
            shutil.copyfile(png, output_path)
        else:
            convert_to_jpeg(png, output_path)


def export_image(tree: ET.ElementTree, output_path: Path, width: int) -> None:
    suffix = output_path.suffix.lower()
    if suffix not in (".svg", ".png", ".jpg", ".jpeg"):
        raise ValueError("Output must use .png, .jpg, .jpeg, or .svg")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if suffix == ".svg":
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
    else:
        export_raster(tree, output_path, width)


def render(template_path: Path, mappings_path: Path | None, output_path: Path, mode: str,
           width: int = 5120) -> None:
    mappings = load_mappings(mappings_path) if mappings_path is not None else None
    tree = ET.parse(template_path)
    root = tree.getroot()
    if mappings is not None:
        apply_bindings(root, mappings, mode)
        update_mode_name(root, mappings, mode)
    embed_images(root, template_path)
    export_image(tree, output_path, width)


def resolve_template(mode: str, explicit_template: Path | None) -> Path:
    if explicit_template is not None:
        return explicit_template

    mode_template = Path(f"templates/steam-controller-2026-{mode}.svg")
    if mode_template.exists():
        return mode_template

    return Path("templates/steam-controller-2026.svg")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export finished controller SVG templates as high-resolution images.")
    parser.add_argument("--mode", choices=("fps", "flight"), required=True)
    parser.add_argument("--data", type=Path, help="Optionally replace template labels with YAML mappings")
    parser.add_argument("--template", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--format", choices=("png", "jpeg", "svg"), default="png")
    parser.add_argument("--width", type=int, default=5120, help="Raster width in pixels (default: 5120)")
    args = parser.parse_args()
    if args.width <= 0:
        parser.error("--width must be positive")

    template = resolve_template(args.mode, args.template)
    output = args.output or Path(f"output/{args.mode}.{args.format}")
    render(template, args.data, output, args.mode, args.width)
    print(f"Rendered {output} from {template}")


if __name__ == "__main__":
    main()
