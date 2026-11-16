"""Build editable SVG references from context-aware mapping data."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import textwrap
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)

SHEETS = {
    'fps': ('steam-controller-2026-fps.svg', 'fps-mode'),
    'flight_base': ('steam-controller-2026-flight-base-controls.svg', 'flight-base-controls'),
    'flight_mining_salvage': ('steam-controller-2026-flight-mining-and-salvage.svg', 'flight-mining-and-salvage'),
}

GROUPS = [
    ('Movement and left controls', ['left_stick', 'l3', 'lt', 'lb', 'dpad', 'left_trackpad']),
    ('Aim, weapons and right controls', ['right_stick', 'r3', 'gyro', 'right_stick_touch', 'rt', 'rb', 'right_trackpad']),
    ('Buttons, rear controls and menus', ['a', 'b', 'x', 'y', 'l4', 'l5', 'r4', 'r5', 'back', 'start']),
]

NAMES = {'left_stick': 'LEFT STICK', 'right_stick': 'RIGHT STICK', 'gyro': 'GYRO',
         'right_stick_touch': 'RIGHT STICK TOUCH', 'dpad': 'D-PAD',
         'left_trackpad': 'LEFT TRACKPAD', 'right_trackpad': 'RIGHT TRACKPAD'}

CONTEXT_NAMES = {
    'shared': 'General', 'fps_movement': 'Movement', 'fps_combat': 'Combat',
    'fps_interaction': 'Interaction', 'fps_tools': 'Tools', 'vehicle_movement': 'Flight',
    'vehicle_systems': 'Systems / interaction', 'vehicle_combat': 'Combat',
    'quantum': 'Quantum', 'scanning': 'Scanning', 'mining': 'Mining',
    'salvage': 'Salvage', 'vehicle_tractor': 'Tractor beam', 'ground_vehicle': 'Ground vehicle',
    'turret': 'Turret', 'eva': 'EVA', 'camera': 'View',
}


def element(parent, name, **attrs):
    return ET.SubElement(parent, f'{{{SVG}}}{name}', {k: str(v) for k, v in attrs.items()})


def text(parent, x, y, value, size=20, color='#172033', weight=500):
    node = element(parent, 'text', x=x, y=y, fill=color, style=f'font-family:Arial,sans-serif;font-size:{size}px;font-weight:{weight}')
    node.text = value
    return node


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


def wrapped(parent, x, y, value, width=74, **style):
    for line in textwrap.wrap(value, width=width, break_long_words=False, break_on_hyphens=False):
        text(parent, x, y, line, **style)
        y += 25
        
    return y


def input_label(path):
    final = path.split('.')[-1]
    named = {'regular': 'Press', 'long_press': 'Long press', 'double_press': 'Double press', 'hold': 'Hold'}
    
    if final in named:
        return named[final]
        
    group, _ = physical_control(path)
    if group.endswith('trackpad'):
        if final == 'center':
            return 'Click'
        if final.endswith('trackpad'):
            return 'Unassigned'
        if group == 'right_trackpad' and ('.fps.' in path or '.modifiers.' in path):
            return 'Scroll'
        return 'Press'
        
    return 'Touch enabled' if group == 'gyro' else 'Move'


def binding_panel(parent, x, y, record):
    path, binding, layer, direction, uses = record
    panel = element(parent, 'g', **{'data-binding': path})
    gesture = input_label(path)
    label = ' · '.join(filter(None, [layer.upper() if layer != 'base' else 'Base', direction, gesture]))
    y = wrapped(panel, x, y, f'{label}  →  {binding["output"]}', size=18, color='#9a5200', weight=700)
    
    if not uses:
        y = wrapped(panel, x, y, binding['action'])
        
    for index, use in uses:
        row = element(panel, 'g', **{'data-use': f'{path}.uses.{index}'})
        context = CONTEXT_NAMES[use['context']]
        gesture = f' ({use["input"]})' if use.get('input') else ''
        y = wrapped(row, x, y, f'{context}: {use["action"]}{gesture}')
        
        if use.get('note'):
            y = wrapped(row, x + 12, y, use['note'], width=78, size=17, color='#586174')
            
    return y + 16


def control_panel(parent, x, y, key, records):
    text(parent, x, y, NAMES.get(key, key.upper()), size=23, weight=800)
    y += 29
    
    for record in records:
        y = binding_panel(parent, x, y, record)
        
    element(parent, 'path', d=f'M {x} {y-3} H {x+760}', stroke='#dce2ea')
    return y + 30


def controller_diagram(root):
    element(root, 'image', id='controller-front', x=780, y=155, width=1000, height=650, preserveAspectRatio='xMidYMid', href='assets/steam-controller-2026.png')
    callouts = [
        ('LB / LT', 935, 198, 600, 220), ('BACK', 1110, 245, 620, 300),
        ('D-PAD', 980, 315, 600, 390), ('LEFT STICK / L3', 1140, 400, 600, 490),
        ('LEFT TRACKPAD', 1100, 575, 600, 650),
        ('RB / RT', 1625, 198, 1870, 220), ('START', 1445, 245, 1870, 300),
        ('A / B / X / Y', 1585, 320, 1870, 390),
        ('RIGHT STICK / R3 / TOUCH', 1415, 400, 1870, 490),
        ('RIGHT TRACKPAD', 1450, 575, 1870, 650),
    ]
    
    for label, ax, ay, bx, by in callouts:
        element(root, 'path', d=f'M {ax} {ay} L {bx} {by}', fill='none', stroke='#2164df',
                **{'stroke-width': 2})
        tx = bx - 15 if bx < 1000 else bx + 15
        node = text(root, tx, by - 9, label, size=21, weight=700)
        
        if bx < 1000:
            node.set('text-anchor', 'end')
            
    text(root, 1280, 835, 'Rear: L4 / L5 on the left · R4 / R5 on the right', size=20).set('text-anchor', 'middle')


def add_header(root, title):
    text(root, 70, 66, 'STAR CITIZEN · STEAM CONTROLLER 2026', size=38, weight=800)
    text(root, 70, 112, title, size=28, color='#087f7a', weight=800)
    description = (
        'All listed actions use your existing bindings. '
        'Context determines what the game does.'
    )
    text(root, 70, 143, description, size=18, color='#586174')


def add_input_legend(root, mode):
    if mode == 'fps':
        legend = (
            'Base = no modifier · L4 = hold L4 · L5 = weapon selection · '
            'Hold ≠ a separate Steam Long Press')
    else:
        legend = (
            'Base = no modifier · L4 / L5 = hold that rear button · '
            'Hold ≠ a separate Steam Long Press')
        
    text(root, 70, 892, legend, size=20, weight=700)


def add_control_column(root, x, heading, controls, selected):
    y = 951
    text(root, x, y, heading.upper(), size=20, color='#087f7a', weight=800)
    y += 43
    
    for key in controls:
        if key in selected:
            y = control_panel(root, x, y, key, selected[key])
            
    return y


def add_control_columns(root, selected):
    bottoms = []
    for column, (heading, controls) in enumerate(GROUPS):
        x = 70 + column * 820
        bottom = add_control_column(root, x, heading, controls, selected)
        bottoms.append(bottom)
        
    return max(bottoms)


def resize_canvas(root, background, content_bottom):
    height = content_bottom + 75
    root.set('height', str(height))
    root.set('viewBox', f'0 0 2560 {height}')
    background.set('height', str(height))
    
    return height


def add_footer(root, height):
    reference = (
        'Reference: Alpha 4.10.2 defaults + custom bindings · '
        'Check notes for toggled or delayed inputs.')
    text(root, 70, height - 34, reference, size=18, color='#586174')


def build_sheet(mappings, sheet_id):
    sheet = mappings['sheets'][sheet_id]
    root = ET.Element(f'{{{SVG}}}svg', {'width': '2560', 'version': '1.1', 'data-sheet': sheet_id})
    background = element(root, 'rect', width=2560, height=1, fill='white')
    add_header(root, sheet['title'])
    controller_diagram(root)
    add_input_legend(root, sheet['mode'])
    selected = select_bindings(mappings, sheet_id)
    content_bottom = add_control_columns(root, selected)
    height = resize_canvas(root, background, content_bottom)
    add_footer(root, height)
    
    return ET.ElementTree(root)


def write_templates(mappings, directory=Path('templates')):
    for sheet_id, (filename, _) in SHEETS.items():
        tree = build_sheet(mappings, sheet_id)
        ET.indent(tree, space='  ')
        tree.write(directory / filename, encoding='utf-8', xml_declaration=True)
