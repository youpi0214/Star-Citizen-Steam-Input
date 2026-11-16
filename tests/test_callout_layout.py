from itertools import combinations
from pathlib import Path
import re
import struct
import unittest
import xml.etree.ElementTree as ET

from scripts import controller_geometry as geometry
from scripts.reference_sheets import SHEETS

ROOT = Path(__file__).resolve().parents[1]


def bounds(node):
    x, y, width, height = map(float, node.get('data-bounds').split())
    return x, y, x + width, y + height


def rectangles_overlap(first, second):
    return (max(first[0], second[0]) < min(first[2], second[2])
            and max(first[1], second[1]) < min(first[3], second[3]))


def segment_crosses_rectangle(start, end, rectangle):
    """Clip a line segment to a rectangle; touching an edge is an intersection."""
    left, top, right, bottom = rectangle
    x, y = start
    dx, dy = end[0] - x, end[1] - y
    enter, leave = 0.0, 1.0

    for direction, distance in [(-dx, x-left), (dx, right-x),
                                (-dy, y-top), (dy, bottom-y)]:
        if direction == 0:
            if distance < 0:
                return False
            continue

        crossing = distance / direction
        if direction < 0:
            enter = max(enter, crossing)
        else:
            leave = min(leave, crossing)

    return enter <= leave


def segments_intersect(first_start, first_end, second_start, second_end):
    def side(start, end, point):
        return ((end[0] - start[0]) * (point[1] - start[1])
                - (end[1] - start[1]) * (point[0] - start[0]))

    return (
        side(first_start, first_end, second_start)
        * side(first_start, first_end, second_end) < 0
        and side(second_start, second_end, first_start)
        * side(second_start, second_end, first_end) < 0
    )


def leader_points(node):
    coordinates = re.findall(r'[ML]\s+([-\d.]+)\s+([-\d.]+)', node.get('d'))
    return [(float(x), float(y)) for x, y in coordinates]


class CalloutLayoutTests(unittest.TestCase):
    def setUp(self):
        self.templates = {
            sheet: ET.parse(ROOT / 'templates' / filename).getroot()
            for sheet, (filename, _) in SHEETS.items()
        }

    def test_anchor_coordinates_match_source_image_dimensions(self):
        png = (ROOT / 'templates/assets/steam-controller-2026.png').read_bytes()
        dimensions = struct.unpack('>II', png[16:24])

        self.assertEqual(dimensions, (geometry.SOURCE_WIDTH, geometry.SOURCE_HEIGHT))
        self.assertEqual(set(geometry.ANCHORS), set(geometry.CONTROL_REGIONS))

    def test_arrow_tips_land_inside_physical_control_regions(self):
        scale = geometry.IMAGE_WIDTH / geometry.SOURCE_WIDTH

        for sheet, root in self.templates.items():
            for node in root.iter():
                control = node.get('data-anchor')
                if not control:
                    continue

                with self.subTest(sheet=sheet, control=control):
                    end_x, end_y = leader_points(node)[-1]
                    source_x = (end_x - geometry.IMAGE_X) / scale
                    source_y = (end_y - geometry.IMAGE_Y) / scale
                    left, top, right, bottom = geometry.CONTROL_REGIONS[control]

                    self.assertLessEqual(left, source_x)
                    self.assertLessEqual(source_x, right)
                    self.assertLessEqual(top, source_y)
                    self.assertLessEqual(source_y, bottom)

    def test_callouts_fit_on_canvas_without_overlapping(self):
        for sheet, root in self.templates.items():
            width, height = float(root.get('width')), float(root.get('height'))
            callouts = [node for node in root.iter() if node.get('data-bounds')]

            for node in callouts:
                with self.subTest(sheet=sheet, control=node.get('data-control')):
                    left, top, right, bottom = bounds(node)
                    self.assertGreaterEqual(left, 0)
                    self.assertGreaterEqual(top, 0)
                    self.assertLessEqual(right, width)
                    self.assertLessEqual(bottom, height)

            for first, second in combinations(callouts, 2):
                with self.subTest(sheet=sheet, pair=(first.get('id'), second.get('id'))):
                    self.assertFalse(rectangles_overlap(bounds(first), bounds(second)))

    def test_leaders_do_not_cross_caption_boxes(self):
        for sheet, root in self.templates.items():
            boxes = [node for node in root.iter() if node.get('data-bounds')]
            leaders = [node for node in root.iter() if node.get('data-anchor')]

            for leader in leaders:
                points = leader_points(leader)
                for box in boxes:
                    with self.subTest(sheet=sheet, leader=leader.get('data-anchor'),
                                      caption=box.get('data-control')):
                        for start, end in zip(points, points[1:]):
                            self.assertFalse(segment_crosses_rectangle(start, end, bounds(box)))

    def test_x_and_b_leaders_do_not_cross(self):
        for sheet, root in self.templates.items():
            leaders = {
                node.get('data-anchor'): leader_points(node)
                for node in root.iter() if node.get('data-anchor')
            }

            for first in zip(leaders['x'], leaders['x'][1:]):
                for second in zip(leaders['b'], leaders['b'][1:]):
                    self.assertFalse(segments_intersect(*first, *second), sheet)

    def test_trigger_leaders_connect_to_their_caption_edges(self):
        for sheet, root in self.templates.items():
            captions = {
                node.get('data-control'): bounds(node)
                for node in root.iter() if node.get('data-control')
            }

            for node in root.iter():
                if node.get('data-anchor') not in {'lt', 'rt'}:
                    continue

                left, _, right, bottom = captions[node.get('data-anchor')]
                x, y = leader_points(node)[0]

                expected_x = (left + right) / 2
                if node.get('data-anchor') == 'rt':
                    expected_x = left - 30 if sheet == 'fps' else left + 30
                self.assertAlmostEqual(x, expected_x, places=2)
                expected_y = max(399, bottom + 15) if sheet == 'fps' and node.get('data-anchor') == 'rt' else bottom + 15
                self.assertAlmostEqual(y, expected_y, places=2)

    def test_sheet_specific_caption_and_leader_adjustments(self):
        for sheet, root in self.templates.items():
            leaders = {node.get('data-anchor'): leader_points(node)
                       for node in root.iter() if node.get('data-anchor')}
            back_start, back_end = leaders['back']
            self.assertAlmostEqual(back_start[0], back_end[0], places=2)

            start, end = leaders['start']
            self.assertAlmostEqual(start[0], end[0], places=2)
            self.assertLess(start[1], 500)

            self.assertEqual(leaders['rb'][0],
                             geometry.SHEET_LEADER_STARTS[sheet]['rb'])
            legend = next(node for node in root.iter() if node.get('id') == 'modifier-legend')
            expected = 'translate(0,-110)' if sheet == 'fps' else 'translate(0,0)'
            self.assertEqual(legend.get('transform'), expected)

    def test_requested_leaders_are_straight(self):
        for sheet, root in self.templates.items():
            for node in root.iter():
                if node.get('data-anchor') in {'lb', 'rt', 'rb', 'y', 'b'}:
                    with self.subTest(sheet=sheet, control=node.get('data-anchor')):
                        self.assertEqual(len(leader_points(node)), 2)

    def test_only_visible_controls_have_arrows(self):
        for sheet, root in self.templates.items():
            targets = {node.get('data-anchor') for node in root.iter() if node.get('data-anchor')}
            callouts = {node.get('data-control') for node in root.iter() if node.get('data-control')}

            self.assertEqual(targets, callouts - {'rear', 'gyro'}, sheet)
            self.assertEqual(len(targets), 15, sheet)


if __name__ == '__main__':
    unittest.main()
