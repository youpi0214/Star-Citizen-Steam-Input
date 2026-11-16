"""Compact controller-centered quick references; full descriptions stay in YAML."""
from __future__ import annotations

import textwrap
import xml.etree.ElementTree as ET

if __package__:
    from . import controller_geometry as geometry
else:
    import controller_geometry as geometry

SVG = 'http://www.w3.org/2000/svg'
FONT_SIZE = 25
LINE_HEIGHT = 31
TEXT = '#172033'
TEAL = '#087f7a'
COLORS = {'L4': '#ac5800', 'L5': '#7350a1'}
HEADINGS = {
    'lb': 'LB', 'lt': 'LT', 'back': 'BACK', 'start': 'START', 'rt': 'RT', 'rb': 'RB',
    'dpad': 'D-PAD', 'left_stick': 'LEFT STICK / L3', 'left_trackpad': 'LEFT TRACKPAD',
    'y': 'Y', 'x': 'X', 'b': 'B', 'a': 'A', 'right_stick': 'RIGHT STICK / R3 / TOUCH',
    'right_trackpad': 'RIGHT TRACKPAD', 'rear': 'REAR CONTROLS · NOT SHOWN',
    'gyro': 'GYRO',
}


def element(parent, name, **attrs):
    return ET.SubElement(parent, f'{{{SVG}}}{name}', {k: str(v) for k, v in attrs.items()})


def text(parent, x, y, value, size=FONT_SIZE, color=TEXT, weight=500):
    node = element(parent, 'text', x=x, y=y, fill=color,
                   style=f'font-family:Arial,sans-serif;font-size:{size}px;font-weight:{weight}')
    node.text = value
    return node


def expanded_path(reference, mode):
    if reference.startswith('global.'):
        return reference
    return f'modes.{mode}.{reference}'


def record_index(selected):
    return {record[0]: record for records in selected.values() for record in records}


def annotate_bindings(parent, references, mode, records):
    for reference in references:
        path = expanded_path(reference, mode)
        if path not in records:
            raise ValueError(f'Display row references an unavailable binding: {path}')
        binding = element(parent, 'g', **{'data-binding': path})
        for index, _ in records[path][4]:
            element(binding, 'g', **{'data-use': f'{path}.uses.{index}'})


def label_lines(label, width):
    # Conservative wrapping for proportional sans-serif text at 27 px.
    characters = int(width / (FONT_SIZE * 0.56))
    return textwrap.wrap(label, width=characters, break_long_words=False,
                         break_on_hyphens=False)


def draw_row(parent, x, y, width, row, mode, records, alignment):
    node = element(parent, 'g', **{'data-label': row['label']})
    annotate_bindings(node, row['bindings'], mode, records)
    color = TEXT
    for layer, layer_color in COLORS.items():
        if any(f'modifiers.{layer.lower()}.' in reference for reference in row['bindings']):
            color = layer_color
            break

    if row['bindings'] == ['global.l4.regular']:
        color = COLORS['L4']
    elif mode == 'flight' and row['bindings'] == ['controls.l5.regular']:
        color = COLORS['L5']
    for index, line in enumerate(label_lines(row['label'], width)):
        indent = 18 if index and alignment == 'start' else 0
        line_node = text(node, x + indent, y, line, color=color)
        line_node.set('text-anchor', alignment)
        y += LINE_HEIGHT
    return y


def draw_callout(root, control, rows, mode, records, sheet_id):
    x, y, width = geometry.callout_position(sheet_id, control)
    group = element(root, 'g', id=f'callout-{control}', **{'data-control': control})
    alignment = 'start'
    text_x = x

    if control in geometry.RIGHT_ALIGNED:
        alignment, text_x = 'end', x + width
    elif control in geometry.CENTERED:
        alignment, text_x = 'middle', x + width / 2

    heading = text(group, text_x, y, HEADINGS[control], size=30, weight=800)
    heading.set('text-anchor', alignment)
    bottom = y + 43
    
    for row in rows:
        bottom = draw_row(group, text_x, bottom, width, row, mode, records, alignment)
    group.set('data-bounds', f'{x} {y-31} {width} {bottom-y+10}')
    
    return group


def add_arrow_marker(root):
    defs = element(root, 'defs')
    marker = element(defs, 'marker', id='button-arrow', viewBox='0 0 8 8', refX=7,
                     refY=4, markerWidth=8, markerHeight=8, orient='auto',
                     markerUnits='userSpaceOnUse')
    element(marker, 'path', d='M 0 0 L 8 4 L 0 8 Z', fill='#2164df')


def draw_leader(root, control, caption, sheet_id):
    bends = list(geometry.LEADER_BENDS[control])

    x, y, width, height = map(float, caption.get('data-bounds').split())

    if control in {'lt', 'rt', 'back'}:
        bends[0] = (x + width / 2, y + height + 15)
    elif control == 'lb':
        bends[0] = (x + width, y + height + 15)
    elif control == 'rb':
        # Keep this diagonal below RT's text and above the Y caption.
        bends[0] = (x - 30, max(400, min(y + height + 15, 410)))

    if control == 'back':
        bends = [(geometry.anchor_position(control)[0], y + height + 15)]
    elif control == 'start':
        bends = [(geometry.anchor_position(control)[0], y + height + 15)]
    elif control == 'rt':
        if sheet_id == 'fps':
            bends = [(x - 30, max(399, y + height + 15))]
        else:
            bends = [(x + 30, y + height + 15)]

    override = geometry.SHEET_LEADER_STARTS.get(sheet_id, {}).get(control)
    if override is not None:
        bends[0] = override

    points = [*bends, geometry.anchor_position(control)]
    commands = [f'{"M" if i == 0 else "L"} {x:.2f} {y:.2f}'
                for i, (x, y) in enumerate(points)]
    
    return element(root, 'path', d=' '.join(commands), fill='none', stroke='#2164df',
                   **{'stroke-width': 2.4, 'marker-end': 'url(#button-arrow)',
                      'data-anchor': control})


def add_header(root, title):
    text(root, 60, 68, 'STAR CITIZEN · STEAM CONTROLLER 2026', size=44, weight=800)
    text(root, 60, 111, title, size=32, color=TEAL, weight=800)


def add_controller(root):
    element(root, 'image', id='controller-front', x=geometry.IMAGE_X, y=geometry.IMAGE_Y,
            width=geometry.IMAGE_WIDTH, height=geometry.IMAGE_HEIGHT,
            preserveAspectRatio='xMidYMid', href='assets/steam-controller-2026.png')


def legend_text(parent, y, value, **style):
    node = text(parent, 900, y, value, **style)
    node.set('text-anchor', 'end')
    return node


def add_legends(root, mode, sheet_id):
    group = element(root, 'g', id='modifier-legend')
    offset = -110 if sheet_id == 'fps' else 0
    group.set('transform', f'translate(0,{offset})')
    legend_text(group, 1800, 'HOW TO READ THE CALLOUTS', size=30, color=TEAL, weight=800)
    legend_text(group, 1843, 'No prefix: normal action')
    legend_text(group, 1877, '[H] Hold · [2] Double press')
    legend_text(group, 1914, 'L4: hold L4 while using the control', color=COLORS['L4'])

    if mode == 'flight':
        legend_text(group, 1951, 'L5: hold L5 while using the control', color=COLORS['L5'])
    else:
        legend_text(group, 1951, 'L5 selects a weapon; it is not a modifier.')



def draw_sheet(mappings, sheet_id, selected):
    sheet = mappings['sheets'][sheet_id]
    width, height = geometry.CANVAS_WIDTH, geometry.CANVAS_HEIGHT
    root = ET.Element(f'{{{SVG}}}svg', {'width': str(width), 'height': str(height), 'viewBox': f'0 0 {width} {height}', 'version': '1.1', 'data-sheet': sheet_id})
    background = element(root, 'rect', width=width, height=height, fill='white')
    add_arrow_marker(root)
    add_header(root, sheet['title'])
    add_controller(root)
    
    callouts = sheet['display']['callouts']
    records = record_index(selected)

    for control, rows in callouts.items():
        caption = draw_callout(root, control, rows, sheet['mode'], records, sheet_id)

        if control in geometry.ANCHORS:
            draw_leader(root, control, caption, sheet_id)

    add_legends(root, sheet['mode'], sheet_id)

    content_bottom = max(float(node.get('y')) for node in root.iter(f'{{{SVG}}}text'))
    height = int(content_bottom + 80)
    root.set('height', str(height))
    root.set('viewBox', f'0 0 {width} {height}')
    background.set('height', str(height))

    return ET.ElementTree(root)
