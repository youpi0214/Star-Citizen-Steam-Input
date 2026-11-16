"""Build editable SVG references from context-aware mapping data."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)

SHEETS = {
    'fps': ('steam-controller-2026-fps.svg', 'fps-mode'),
    'flight_base': ('steam-controller-2026-flight-base-controls.svg', 'flight-base-controls'),
    'flight_mining_salvage': ('steam-controller-2026-flight-mining-and-salvage.svg', 'flight-mining-and-salvage'),
}

if __package__:
    from .sheet_layout import draw_sheet
else:
    from sheet_layout import draw_sheet


def bindings(data, path):
    if 'action' in data and 'output' in data:
        yield path, data
        return
        
    for key, value in data.items():
        if isinstance(value, dict):
            yield from bindings(value, f'{path}.{key}')


def physical_control(path):
    parts = path.split('.')
    key = parts[1] if parts[0] == 'global' else parts[parts.index('controls') + 1]
    group = 'dpad' if key.startswith('dpad_') else key
    group = 'left_stick' if key.startswith('left_stick') else group
    direction = key.removeprefix('dpad_') if group == 'dpad' else ''
    
    if key in ('left_stick_x', 'left_stick_y'):
        direction = key[-1].upper() + ' axis'
    if group.endswith('trackpad'):
        direction = {'up': '↑', 'down': '↓', 'left': '←', 'right': '→', 'center': 'click'}.get(parts[-1], '')
    return group, direction


def select_bindings(mappings, sheet_id):
    sheet = mappings['sheets'][sheet_id]
    mode = sheet['mode']
    sources = [('base', mappings['global'], 'global'), ('base', mappings['modes'][mode]['controls'], f'modes.{mode}.controls')]

    for layer, data in mappings['modes'][mode]['modifiers'].items():
        sources.append((layer, data['controls'], f'modes.{mode}.modifiers.{layer}.controls'))

    selected = defaultdict(list)
    for layer, data, prefix in sources:
        if layer not in sheet['layers']:
            continue
        for path, binding in bindings(data, prefix):
            uses = [(i, use) for i, use in enumerate(binding.get('uses', []))
                    if use['context'] in sheet['contexts']]
            if not uses and not sheet.get('include_unclassified_outputs'):
                continue
            group, direction = physical_control(path)
            selected[group].append((path, binding, layer, direction, uses))
            
    return selected



def build_sheet(mappings, sheet_id):
    selected = select_bindings(mappings, sheet_id)
    return draw_sheet(mappings, sheet_id, selected)


def write_templates(mappings, directory=Path('templates')):
    for sheet_id, (filename, _) in SHEETS.items():
        tree = build_sheet(mappings, sheet_id)
        ET.indent(tree, space='  ')
        tree.write(directory / filename, encoding='utf-8', xml_declaration=True)
