"""Assemble the logotype, the full-name lockup, product lockups and the app icon."""
from shapely import affinity
from shapely.geometry import box
from shapely.ops import unary_union

from lettering import D, X, caps_line, set_text
from marks import document, handshake

MARK_GAP = 0.22 * X                 # optical gap between a pictogram and its neighbours
FULL_NAME = dict(cap=54.0, pen=9.0, gap=36.0)


def seat(mark):
    """Pictograms stand on the descender line and reach the ascender line."""
    return affinity.translate(mark, -mark.bounds[0], D - mark.bounds[3])


def _slide(fixed, g, gap, direction=1):
    """Move g horizontally until its outline is exactly `gap` from `fixed`."""
    if direction < 0:
        mirror = lambda s: affinity.scale(s, -1, 1, origin=(0, 0))
        return mirror(_slide(mirror(fixed), mirror(g), gap))
    lo, hi = fixed.bounds[0] - g.bounds[2], fixed.bounds[2] - g.bounds[0] + gap
    for _ in range(40):
        mid = (lo + hi) / 2
        if affinity.translate(g, mid, 0).distance(fixed) > gap:
            hi = mid
        else:
            lo = mid
    return affinity.translate(g, hi, 0)


def logotype(parts):
    """parts: sequence of text strings and pictogram geometries, left to right."""
    placed = []
    for p in parts:
        g = set_text(p) if isinstance(p, str) else seat(p)
        placed.append(affinity.translate(g, -g.bounds[0], 0) if not placed else _slide(placed[-1], g, MARK_GAP))
    return unary_union(placed)


def master_logotype():
    """team with [handshake] si — the dot of teamwith.si becomes a handshake."""
    return logotype(['team with', handshake(), 'si'])


def master_pieces():
    """The logotype as separate pieces (left words, handshake, right word) for construction drawings."""
    left = set_text('team with')
    left = affinity.translate(left, -left.bounds[0], 0)
    mark = _slide(left, seat(handshake()), MARK_GAP)
    right = _slide(mark, set_text('si'), MARK_GAP)
    return left, mark, right


def full_name_line(logo):
    x0, _, x1, y1 = logo.bounds
    line = caps_line('SUPER INTELLIGENCE', FULL_NAME['cap'], FULL_NAME['pen'], width=x1 - x0)
    return affinity.translate(line, x0 - line.bounds[0], y1 + FULL_NAME['gap'] - line.bounds[1])


def master_lockup():
    logo = master_logotype()
    return unary_union([logo, full_name_line(logo)])


def product_lockup(label, icon, with_full_name=True):
    """Prefix module (label + icon) attached in front of the untouched master lockup."""
    master = master_lockup() if with_full_name else master_logotype()
    logo = master_logotype()
    ic = _slide(logo, seat(icon), MARK_GAP, direction=-1)
    lab = _slide(ic, set_text(label), MARK_GAP, direction=-1)
    return unary_union([lab, ic, master])


def filemaster_lockup(with_full_name=True):
    return product_lockup('file master', document(), with_full_name)


def app_icon(mark_ratio=0.60, radius_ratio=0.225, thicken=0.0, mark=None):
    """Returns (side, corner_radius, mark geometry positioned inside a side x side tile)."""
    m = handshake() if mark is None else mark
    if thicken:
        m = m.buffer(thicken, quad_segs=16)
    w, h = m.bounds[2] - m.bounds[0], m.bounds[3] - m.bounds[1]
    side = h / mark_ratio
    m = affinity.translate(m, -m.bounds[0] + (side - w) / 2, -m.bounds[1] + (side - h) / 2)
    return side, side * radius_ratio, m


def clear_space_box(geom, margin=X):
    x0, y0, x1, y1 = geom.bounds
    return box(x0 - margin, y0 - margin, x1 + margin, y1 + margin)


def square(geom, side=1000.0, height_ratio=0.58, optical=0.5):
    """Centre a mark in a side x side square. Vertical position blends the box centre with the ink centroid."""
    k = side * height_ratio / (geom.bounds[3] - geom.bounds[1])
    g = affinity.scale(geom, k, k, origin=(0, 0))
    x0, y0, x1, y1 = g.bounds
    cy = (1 - optical) * (y0 + y1) / 2 + optical * g.centroid.y
    return affinity.translate(g, side / 2 - (x0 + x1) / 2, side / 2 - cy)


def square_handshake(side=1000.0):
    return square(handshake(), side, 0.58)


def square_si(side=1000.0, height_ratio=0.50):
    return square(set_text('si'), side, height_ratio)
