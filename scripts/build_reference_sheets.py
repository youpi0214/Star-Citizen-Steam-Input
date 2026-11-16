#!/usr/bin/env python3
"""Rebuild editable SVG templates after changing contextual mappings."""
import argparse
from pathlib import Path

import yaml

from reference_sheets import write_templates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path('data/mappings.yaml'))
    parser.add_argument('--templates', type=Path, default=Path('templates'))
    args = parser.parse_args()
    args.templates.mkdir(parents=True, exist_ok=True)
    write_templates(yaml.safe_load(args.data.read_text(encoding='utf-8')), args.templates)


if __name__ == '__main__':
    main()
