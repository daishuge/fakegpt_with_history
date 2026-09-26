"""Pictograms drawn with the logotype pen: the handshake (the '.' of teamwith.si) and product icons."""
import re
from pathlib import Path

from fontTools.pens.basePen import BasePen
from fontTools.svgLib.path import parse_path
from shapely import affinity
from shapely.geometry import Polygon
from shapely.ops import unary_union

from lettering import A, D, W, arc, ink

VENDOR = Path(__file__).parent / 'vendor' / 'material-symbols'


class _Flatten(BasePen):
    def __init__(self, steps=20):
        super().__init__(None)
        self.rings, self.cur, self.steps = [], [], steps

    def _moveTo(self, p):
        self._flush()
        self.cur = [p]

    def _lineTo(self, p):
        self.cur.append(p)

    def _curveToOne(self, p1, p2, p3):
        p0 = self._getCurrentPoint()
        for i in range(1, self.steps + 1):
            t = i / self.steps
            u = 1 - t
            self.cur.append(tuple(u**3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t**3 * d
                                  for a, b, c, d in zip(p0, p1, p2, p3)))

    def _qCurveToOne(self, p1, p2):
        p0 = self._getCurrentPoint()
        for i in range(1, self.steps + 1):
            t = i / self.steps
            u = 1 - t
            self.cur.append(tuple(u * u * a + 2 * u * t * b + t * t * c for a, b, c in zip(p0, p1, p2)))

    def _closePath(self):
        self._flush()

    _endPath = _closePath

    def _flush(self):
        if len(self.cur) > 2:
            self.rings.append(self.cur + [self.cur[0]])
        self.cur = []


def _signed_area(ring):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(ring, ring[1:])) / 2


def material_icon(name, stroke_units):
    """Load a Material Symbols outline icon and scale it so its stroke equals the logotype pen."""
    d = re.search(r' d="([^"]+)"', (VENDOR / name).read_text()).group(1)
    pen = _Flatten()
    parse_path(d, pen)
    rings = sorted((r for r in pen.rings if abs(_signed_area(r)) > 50), key=lambda r: -abs(_signed_area(r)))
    sign = _signed_area(rings[0])
    holes = [Polygon(r).buffer(0) for r in rings[1:] if _signed_area(r) * sign < 0]
    fills = [Polygon(r).buffer(0) for r in rings[1:] if _signed_area(r) * sign > 0]
    g = Polygon(rings[0]).buffer(0).difference(unary_union(holes)).union(unary_union(fills))
    k = W / stroke_units
    g = affinity.scale(g, k, k, origin=(0, 0))
    return affinity.translate(g, -g.bounds[0], -g.bounds[3])       # ink bottom-left at the origin


def handshake():
    """Two hands whose outline is a heart. Stroke 80 at weight 700 -> spans descender..ascender at pen W."""
    return material_icon('handshake_rounded_w700.svg', 80.0)


def document(lines=2):
    """A page with a folded corner, drawn with the logotype pen."""
    hgt = (A + D) * 0.9
    wid = hgt * 0.76
    fold = wid * 0.34
    r = W * 1.1
    x0, y0, x1, y1 = W / 2, -hgt + W / 2, wid - W / 2, -W / 2
    outline = ([(x1 - r, y1)] + arc(x1 - r, y1 - r, r, 270, 360, 10)
               + [(x1, y0 + fold), (x1 - fold, y0)]
               + [(x0 + r, y0)] + arc(x0 + r, y0 + r, r, 90, 180, 10)
               + [(x0, y1 - r)] + arc(x0 + r, y1 - r, r, 180, 270, 10) + [(x1 - r, y1)])
    strokes = [outline, [(x1 - fold, y0), (x1 - fold, y0 + fold), (x1, y0 + fold)]]
    for yy in (-hgt * 0.40, -hgt * 0.22)[:lines]:
        strokes.append([(x0 + wid * 0.2, yy), (x1 - wid * 0.2, yy)])
    return ink(strokes)
