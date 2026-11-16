"""Keep documented actions visible as the mapping grows."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

import yaml

from scripts.reference_sheets import SHEETS, select_bindings

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / 'templates'
SVG_TEXT = '{http://www.w3.org/2000/svg}text'


def action_paths(data, prefix):
    for key, value in data.items():
        path = f'{prefix}.{key}'

        if isinstance(value, dict):
            yield from action_paths(value, path)
        elif key == 'action':
            yield path


def context_uses(data):
    if not isinstance(data, dict):
        return

    for use in data.get('uses', []):
        yield data, use

    for child in data.values():
        yield from context_uses(child)


def binding_sources(mappings):
    for mode, data in mappings['modes'].items():
        yield mode, 'base', mappings['global']
        yield mode, 'base', data['controls']

        for layer, modifier in data['modifiers'].items():
            yield mode, layer, modifier['controls']


def attribute_values(root, attribute):
    return {node.get(attribute) for node in root.iter() if node.get(attribute)}


def selected_records(selected):
    for records in selected.values():
        yield from records


def selected_use_paths(selected):
    for path, _, _, _, uses in selected_records(selected):
        for index, _ in uses:
            yield f'{path}.uses.{index}'


def control_contexts(selected, control):
    return {
        use['context']
        for _, _, _, _, uses in selected[control]
        for _, use in uses
    }


def controller_image(root):
    return next(node for node in root.iter() if node.get('id') == 'controller-front')


def run_script(name, *args, check=True):
    command = [sys.executable, str(ROOT / 'scripts' / name), *args]

    return subprocess.run(
        command,
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
    )


class ReferenceSheetTests(unittest.TestCase):
    def setUp(self):
        source = ROOT / 'data/mappings.yaml'
        self.mappings = yaml.safe_load(source.read_text(encoding='utf-8'))

    def test_sheet_definitions_use_registered_modes_contexts_and_layers(self):
        registered = set(self.mappings['contexts'])

        for sheet_id, sheet in self.mappings['sheets'].items():
            with self.subTest(sheet=sheet_id):
                self.assertIn(sheet['mode'], self.mappings['modes'])
                self.assertFalse(set(sheet['contexts']) - registered)

                mode = self.mappings['modes'][sheet['mode']]
                available_layers = {'base', *mode['modifiers']}

                self.assertFalse(set(sheet['layers']) - available_layers)

    def test_context_actions_have_registered_contexts_and_a_matching_sheet(self):
        registered = set(self.mappings['contexts'])
        sheets = self.mappings['sheets'].values()

        for mode, layer, source in binding_sources(self.mappings):
            for binding, use in context_uses(source):
                with self.subTest(mode=mode, layer=layer, use=use):
                    self.assertIn('output', binding)
                    self.assertIn(use['context'], registered)
                    self.assertTrue(use['action'])

                    matching_sheets = [
                        sheet for sheet in sheets
                        if sheet['mode'] == mode
                        and layer in sheet['layers']
                        and use['context'] in sheet['contexts']
                    ]

                    self.assertTrue(matching_sheets)

    def test_templates_cover_selected_contexts(self):
        for sheet_id, (filename, _) in SHEETS.items():
            with self.subTest(sheet=sheet_id):
                root = ET.parse(TEMPLATES / filename).getroot()
                selected = select_bindings(self.mappings, sheet_id)

                expected_bindings = {record[0] for record in selected_records(selected)}
                expected_uses = set(selected_use_paths(selected))

                self.assertEqual(attribute_values(root, 'data-binding'), expected_bindings)
                self.assertEqual(attribute_values(root, 'data-use'), expected_uses)
                self.assertEqual(root.get('data-sheet'), sheet_id)

    def test_all_physical_bindings_appear_on_a_sheet(self):
        mode_paths = {mode: set() for mode in self.mappings['modes']}

        for sheet_id, (filename, _) in SHEETS.items():
            root = ET.parse(TEMPLATES / filename).getroot()
            mode = self.mappings['sheets'][sheet_id]['mode']

            mode_paths[mode].update(attribute_values(root, 'data-binding'))

        for mode, paths in mode_paths.items():
            with self.subTest(mode=mode):
                actions = action_paths(self.mappings['modes'][mode], f'modes.{mode}')
                expected = {path.removesuffix('.action') for path in actions}
                missing = expected - paths

                self.assertFalse(missing, f'Missing bindings: {missing}')

    def test_template_text_stays_within_canvas_height(self):
        for filename, _ in SHEETS.values():
            root = ET.parse(TEMPLATES / filename).getroot()
            height = float(root.get('height'))

            for node in root.iter(SVG_TEXT):
                with self.subTest(template=filename, text=node.text):
                    self.assertLess(float(node.get('y')), height)

    def test_context_sheets_share_controller_geometry(self):
        geometry = []

        for filename, _ in SHEETS.values():
            root = ET.parse(TEMPLATES / filename).getroot()
            geometry.append(controller_image(root).attrib)

        for attributes in geometry[1:]:
            self.assertEqual(attributes, geometry[0])

    def test_flight_sheets_include_both_modifier_layers(self):
        for sheet_id, (filename, _) in SHEETS.items():
            if self.mappings['sheets'][sheet_id]['mode'] != 'flight':
                continue

            root = ET.parse(TEMPLATES / filename).getroot()
            paths = attribute_values(root, 'data-binding')

            for layer in ('l4', 'l5'):
                with self.subTest(sheet=sheet_id, layer=layer):
                    self.assertTrue(any(f'.modifiers.{layer}.' in path for path in paths))

    def test_rb_actions_match_the_gameplay_context(self):
        base = select_bindings(self.mappings, 'flight_base')
        profession = select_bindings(self.mappings, 'flight_mining_salvage')

        self.assertIn('vehicle_combat', control_contexts(base, 'rb'))
        self.assertNotIn('vehicle_combat', control_contexts(profession, 'rb'))
        self.assertIn('mining', control_contexts(profession, 'rb'))

    def test_checked_in_templates_match_context_builder(self):
        with tempfile.TemporaryDirectory() as directory:
            run_script('build_reference_sheets.py', '--templates', directory)

            for filename, _ in SHEETS.values():
                with self.subTest(template=filename):
                    expected = (TEMPLATES / filename).read_bytes()
                    generated = (Path(directory) / filename).read_bytes()

                    self.assertEqual(generated, expected)

    def test_all_sheets_export_to_self_contained_svgs(self):
        with tempfile.TemporaryDirectory() as directory:
            run_script(
                'render.py',
                '--mode', 'flight',
                '--sheet', 'all',
                '--format', 'svg',
                '--data', 'data/mappings.yaml',
                '--output-dir', directory,
            )

            outputs = sorted(path.name for path in Path(directory).iterdir())
            self.assertEqual(
                outputs,
                ['flight-base-controls.svg', 'flight-mining-and-salvage.svg'],
            )

            for name in outputs:
                with self.subTest(output=name):
                    root = ET.parse(Path(directory) / name).getroot()
                    image = controller_image(root)

                    self.assertTrue(image.get('href').startswith('data:image/png;base64,'))

    def test_ambiguous_or_unsupported_sheet_options_fail(self):
        invalid_options = [
            ('--mode', 'flight', '--sheet', 'l5'),
            ('--mode', 'fps', '--sheet', 'mining-salvage'),
            ('--mode', 'flight', '--format', 'jpeg'),
            ('--mode', 'flight', '--output', 'sheet.jpg'),
            ('--mode', 'flight', '--sheet', 'all', '--output', 'sheet.png'),
            ('--mode', 'flight', '--sheet', 'all', '--template', 'sheet.svg'),
        ]

        for args in invalid_options:
            with self.subTest(args=args):
                result = run_script('render.py', *args, check=False)

                self.assertEqual(result.returncode, 2, result.stderr)


if __name__ == '__main__':
    unittest.main()
