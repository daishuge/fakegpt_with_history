"""Write shapely geometry out as tight SVG paths, PNGs and favicons."""
from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image


def _num(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return '0' if s == '-0' else s


def path_d(geom, ox=0.0, oy=0.0, tol=0.04):
    g = geom.simplify(tol, preserve_topology=True)
    polys = [g] if g.geom_type == 'Polygon' else list(g.geoms)
    out = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            pts = list(ring.coords)[:-1]
            out.append('M' + 'L'.join(f'{_num(x - ox)} {_num(y - oy)}' for x, y in pts) + 'Z')
    return ''.join(out)


def svg(layers, bounds=None, pad=0.0, title='teamwith.si', background=None):
    """layers: [(geometry, fill)]; bounds default to the union of all layers."""
    if bounds is None:
        bs = [g.bounds for g, _ in layers]
        bounds = (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))
    x0, y0, x1, y1 = bounds
    ox, oy = x0 - pad, y0 - pad
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_num(w)} {_num(h)}" '
            f'width="{_num(w)}" height="{_num(h)}" role="img" aria-label="{title}"><title>{title}</title>')
    body = [background] if background else []
    body += [f'<path fill="{fill}" fill-rule="evenodd" d="{path_d(g, ox, oy)}"/>' for g, fill in layers]
    return head + ''.join(body) + '</svg>\n'


def tile_svg(side, radius, mark, bg, fg, title='teamwith.si'):
    rect = f'<rect width="{_num(side)}" height="{_num(side)}" rx="{_num(radius)}" fill="{bg}"/>'
    return svg([(mark, fg)], bounds=(0, 0, side, side), title=title, background=rect)


def write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def png(svg_text, path, width):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(bytestring=svg_text.encode(), write_to=str(path), output_width=width)


def ico(svg_text, path, sizes=(16, 32, 48)):
    big = Image.open(BytesIO(cairosvg.svg2png(bytestring=svg_text.encode(), output_width=256)))
    big.save(path, sizes=[(s, s) for s in sizes])
