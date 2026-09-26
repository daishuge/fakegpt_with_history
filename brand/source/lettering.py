"""Monoline lettering for the teamwith.si logotype.

Every glyph is a centreline drawn with one round-capped pen, so the letters and
the pictograms share a single stroke. Units: x-height = 100, baseline at y = 0,
y grows downwards (SVG convention).
"""
import math

from shapely import affinity
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

X = 100.0   # x-height
W = 20.0    # pen width of the logotype
C = 140.0   # cap height
A = 150.0   # ascender
D = 60.0    # descender

H = W / 2
R = (X - W) / 2          # centreline radius of a bowl whose ink spans 0..X
CY = -X / 2              # bowl centre


def arc(cx, cy, r, a0, a1, n=48):
    """Points on a circle; angles in degrees, counter-clockwise as seen on screen."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy - r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def ink(strokes, dots=(), pen=W):
    parts = [LineString(s).buffer(pen / 2, quad_segs=16) for s in strokes]
    parts += [Point(x, y).buffer(r, quad_segs=16) for x, y, r in dots]
    return unary_union(parts)


# ---------------------------------------------------------------- lowercase

def _bowl():
    return arc(H + R, CY, R, 0, 360, 96)


def _n(stem_top):
    return [[(H, -(stem_top - H)), (H, -H)], arc(H + R, CY, R, 180, 0) + [(H + 2 * R, -H)]]


def _s(top, ru, rl, a_top=36, a_bot=-146):
    cx = H + rl
    yu, yl = -(top - H) + ru, -H - rl
    return [arc(cx, yu, ru, a_top, 270, 50) + arc(cx, yl, rl, 90, a_bot, 60)[1:]]


def _hooked_stem(x, top, r=26.0, tail=8.0):
    """Stem that turns right into the baseline (t, l)."""
    return [(x, -top), (x, -(H + r))] + arc(x + r, -(H + r), r, 180, 270, 24) + [(x + r + tail, -H)]


LOWER = {
    'a': lambda: ink([_bowl(), [(H + 2 * R, -(X - H)), (H + 2 * R, -H)]]),
    'c': lambda: ink([arc(H + R, CY, R, 42, 318, 80)]),
    'e': lambda: ink([arc(H + R, CY, R, 0, 322, 90), [(H, CY), (H + 2 * R, CY)]]),
    'f': lambda: ink([[(20, -H), (20, -(A - H - 26))] + arc(46, -(A - H - 26), 26, 180, 90, 24) + [(56, -(A - H))],
                      [(2, -(X - H)), (54, -(X - H))]]),
    'g': lambda: ink([_bowl(), [(H + 2 * R, -(X - H)), (H + 2 * R, 26)] + arc(H + 2 * R - 30, 26, 30, 0, -150, 30)]),
    'h': lambda: ink(_n(A)),
    'i': lambda: ink([[(H, -(X - H)), (H, -H)]], dots=[(H, -X - 30, W * 0.62)]),
    'l': lambda: ink([[(H, -(A - H)), (H, -H)]]),
    'm': lambda: ink([[(H, -(X - H)), (H, -H)],
                      [(H, -X + 30 + H)] + arc(H + 30, -X + 30 + H, 30, 180, 0, 40) + [(H + 60, -H)],
                      [(H + 60, -X + 30 + H)] + arc(H + 90, -X + 30 + H, 30, 180, 0, 40) + [(H + 120, -H)]]),
    'n': lambda: ink(_n(X)),
    'o': lambda: ink([_bowl()]),
    'p': lambda: ink([_bowl(), [(H, -(X - H)), (H, D - H)]]),
    'r': lambda: ink([[(H, -(X - H)), (H, -H)], arc(H + R, CY, R, 180, 62, 40)]),
    's': lambda: ink(_s(X, 19.0, 21.0)),
    't': lambda: ink([_hooked_stem(20.0, 128.0), [(2, -(X - H)), (54, -(X - H))]]),
    'u': lambda: ink([[(H, -(X - H)), (H, CY)] + arc(H + R, CY, R, 180, 360, 48),
                      [(H + 2 * R, -(X - H)), (H + 2 * R, -H)]]),
    'w': lambda: ink([[(H, -(X - H)), (H + 28, -H), (H + 56, -(X - H) + 4), (H + 84, -H), (H + 112, -(X - H))]]),
    'S': lambda: ink(_s(C, 29.0, 31.0, 32, -148)),
    'I': lambda: ink([[(H, -(C - H)), (H, -H)]]),
    '.': lambda: ink([], dots=[(H * 1.25, -H * 1.25, H * 1.25)]),
}


def _place_after(prev, g, gap):
    """Slide g rightwards until its outline sits exactly `gap` from prev (optical spacing)."""
    lo, hi = prev.bounds[0] - g.bounds[2], prev.bounds[2] - g.bounds[0] + gap
    for _ in range(40):
        mid = (lo + hi) / 2
        if affinity.translate(g, mid, 0).distance(prev) > gap:
            hi = mid
        else:
            lo = mid
    return affinity.translate(g, hi, 0)


def set_text(text, gap=0.18 * X, space=0.30 * X):
    """Set a string of lowercase glyphs (plus S, I, '.') with optical spacing."""
    placed, prev, extra = [], None, 0.0
    for ch in text:
        if ch == ' ':
            extra = space
            continue
        g = LOWER[ch]()
        g = affinity.translate(g, -g.bounds[0], 0) if prev is None else _place_after(prev, g, gap + extra)
        placed.append(g)
        prev, extra = g, 0.0
    return unary_union(placed)


# ---------------------------------------------------------------- capitals (full-name line)

def cap_glyph(ch, cap, pen):
    h = pen / 2
    yt, yb, ym = -(cap - h), -h, -cap / 2
    r = (cap - pen) / 2
    if ch == 'S':
        tot = (cap - pen) / 2
        ru, rl = tot * 0.485, tot * 0.515
        cx = h + rl
        s = [arc(cx, yt + ru, ru, 32, 270, 60) + arc(cx, yb - rl, rl, 90, -148, 70)[1:]]
    elif ch == 'U':
        ru = (0.74 * cap - pen) / 2
        s = [[(h, yt), (h, yb - ru)] + arc(h + ru, yb - ru, ru, 180, 360, 40) + [(h + 2 * ru, yt)]]
    elif ch in 'PR':
        rb, a = 0.265 * cap, 0.16 * cap
        s = [[(h, yt), (h, yb)], [(h, yt), (h + a, yt)] + arc(h + a, yt + rb, rb, 90, -90, 36) + [(h, yt + 2 * rb)]]
        if ch == 'R':
            s.append([(h + a * 0.9, yt + 2 * rb), (h + a + rb * 0.95, yb)])
    elif ch == 'E':
        we = 0.50 * cap
        s = [[(h + we, yt), (h, yt), (h, yb), (h + we, yb)], [(h, ym), (h + we * 0.86, ym)]]
    elif ch == 'I':
        s = [[(h, yt), (h, yb)]]
    elif ch == 'N':
        wn = 0.64 * cap
        s = [[(h, yb), (h, yt), (h + wn, yb), (h + wn, yt)]]
    elif ch == 'T':
        wt = 0.60 * cap
        s = [[(h, yt), (h + wt, yt)], [(h + wt / 2, yt), (h + wt / 2, yb)]]
    elif ch == 'L':
        s = [[(h, yt), (h, yb), (h + 0.44 * cap, yb)]]
    elif ch == 'C':
        s = [arc(h + r, ym, r, 42, 318, 80)]
    elif ch == 'G':
        s = [arc(h + r, ym, r, 42, 360, 80) + [(h + r * 1.1, ym)]]
    else:
        raise KeyError(ch)
    return ink(s, pen=pen)


def caps_line(text, cap, pen, width=None, word_weight=2.6):
    """Tracked capitals. With `width`, extra space is spread over the gaps (word gaps count more)."""
    gap, space = 0.22 * cap, 0.55 * cap
    placed, weights, prev, extra = [], [], None, 0.0
    for ch in text:
        if ch == ' ':
            extra = space
            continue
        g = cap_glyph(ch, cap, pen)
        if prev is None:
            g = affinity.translate(g, -g.bounds[0], 0)
        else:
            g = _place_after(prev, g, gap + extra)
            weights.append(word_weight if extra else 1.0)
        placed.append(g)
        prev, extra = g, 0.0
    if width:
        unit = (width - (placed[-1].bounds[2] - placed[0].bounds[0])) / sum(weights)
        shift, out = 0.0, [placed[0]]
        for g, wgt in zip(placed[1:], weights):
            shift += unit * wgt
            out.append(affinity.translate(g, shift, 0))
        placed = out
    return unary_union(placed)
