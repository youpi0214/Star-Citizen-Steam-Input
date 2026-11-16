"""Controller-local anchor coordinates, measured on the 1548 × 1016 source PNG."""

SOURCE_WIDTH = 1548
SOURCE_HEIGHT = 1016
IMAGE_X = 950
IMAGE_Y = 460
IMAGE_WIDTH = 1700
IMAGE_HEIGHT = IMAGE_WIDTH * SOURCE_HEIGHT / SOURCE_WIDTH
CANVAS_WIDTH = 3600
CANVAS_HEIGHT = 2400

# Coordinates are in source-image pixels, not canvas pixels. Keep the point
# inside the named physical control when changing a leader's bends or label.
ANCHORS = {
    'lb': (287, 88),
    'lt': (363, 48),
    'back': (515, 150),
    'dpad': (311, 252),
    'left_stick': (557, 340),
    'left_trackpad': (493, 615),
    'rb': (1260, 88),
    'rt': (1184, 48),
    'start': (1033, 149),
    'y': (1231, 169),
    'x': (1149, 250),
    'b': (1318, 251),
    'a': (1238, 332),
    'right_stick': (991, 339),
    'right_trackpad': (1056, 613),
}

# Small regions around the photographed controls support independent anchor
# checks. Rear controls deliberately have no anchor on this front photograph.
CONTROL_REGIONS = {
    'lb': (265, 75, 315, 100), 'lt': (335, 37, 390, 62),
    'rb': (1235, 75, 1285, 100), 'rt': (1160, 37, 1210, 62),
    'back': (465, 125, 565, 175), 'start': (980, 125, 1085, 175),
    'dpad': (280, 225, 345, 280),
    'left_stick': (500, 285, 615, 400), 'right_stick': (935, 285, 1050, 400),
    'left_trackpad': (390, 525, 600, 710),
    'right_trackpad': (945, 525, 1165, 710),
    'y': (1200, 135, 1260, 205), 'x': (1115, 215, 1180, 280),
    'b': (1285, 215, 1350, 285), 'a': (1205, 300, 1270, 365),
}

# x, y, maximum text width. The widest callouts sit beside the sticks/pads.
CALLOUTS = {
    'lb': (100, 240, 800), 'lt': (1000, 145, 620),
    'back': (1660, 350, 330), 'start': (2020, 350, 350),
    'rt': (2500, 145, 500), 'rb': (3070, 145, 470),
    'dpad': (100, 520, 800), 'left_stick': (100, 850, 800),
    'left_trackpad': (100, 1260, 800),
    'y': (2750, 550, 790), 'x': (2750, 950, 790),
    'b': (2750, 790, 790), 'a': (2750, 1140, 790),
    'right_stick': (2750, 1340, 790), 'right_trackpad': (2750, 1700, 790),
    'rear': (1400, 1645, 800), 'gyro': (1400, 1850, 800),
}

# Routes start at the caption and end at the physical control. Bends can move
# freely; the final endpoint always comes from ANCHORS through anchor_position.
LEADER_BENDS = {
    'lb': [(930, 320)],
    'lt': [(1310, 335)], 'back': [(1516, 590)],
    'start': [(2084, 570)], 'rt': [(2750, 335)],
    'rb': [(3040, 350)],
    'dpad': [(930, 555), (1035, 555)],
    'left_stick': [(930, 885), (1035, 885)],
    'left_trackpad': [(930, 1295), (1035, 1295)],
    'y': [(2715, 575)],
    'x': [(2715, 975), (2650, 975), (2425, 806)],
    'b': [(2715, 815)],
    'a': [(2715, 1165), (2480, 1165)],
    'right_stick': [(2715, 1365), (2390, 1365)],
    'right_trackpad': [(2715, 1725), (2500, 1725)],
}


def anchor_position(control):
    x, y = ANCHORS[control]
    scale = IMAGE_WIDTH / SOURCE_WIDTH
    return IMAGE_X + x * scale, IMAGE_Y + y * scale


RIGHT_ALIGNED = {'lb', 'dpad', 'left_stick', 'left_trackpad'}
CENTERED = {'rear', 'gyro'}


# These adjustments belong to the individually reviewed sheets.
SHEET_CALLOUTS = {
    'fps': {
        'lt': (1130, 145, 350),
        'back': (1480, 350, 330),
        'rb': (2960, 400, 470),
    },
    'flight_base': {
        'lt': (1130, 145, 500),
        'back': (1480, 350, 330),
        'start': (2020, 350, 260),
        'rt': (2380, 145, 500),
        'rb': (2820, 300, 650),
    },
    'flight_mining_salvage': {
        'back': (1480, 350, 330),
        'start': (2020, 350, 260),
        'rt': (2380, 145, 500),
        'rb': (2820, 300, 650),
    },
}

SHEET_LEADER_STARTS = {
    'fps': {'rb': (2930, 440)},
    'flight_base': {'rb': (2790, 365)},
    'flight_mining_salvage': {'rb': (2790, 365)},
}


def callout_position(sheet_id, control):
    return SHEET_CALLOUTS.get(sheet_id, {}).get(control, CALLOUTS[control])
