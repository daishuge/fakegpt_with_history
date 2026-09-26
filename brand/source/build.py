"""Regenerate every teamwith.si logo file:  python build.py"""
from pathlib import Path

import export
from lockups import (app_icon, filemaster_lockup, filemaster_stack, master_logotype, master_lockup, square_handshake,
                     square_si)
from marks import document, handshake

ROOT = Path(__file__).resolve().parent.parent
LOGO, PRODUCTS = ROOT / 'logo', ROOT / 'products'

ROYAL_BLUE, NAVY, WHITE, BLACK = '#123E8C', '#0B2554', '#FFFFFF', '#000000'


def colourways(name, geom, folder, png_widths=()):
    for suffix, fill in (('', ROYAL_BLUE), ('_white', WHITE), ('_black', BLACK)):
        doc = export.svg([(geom, fill)])
        export.write(folder / f'{name}{suffix}.svg', doc)
        for w in png_widths:
            export.png(doc, folder / 'png' / f'{name}{suffix}_{w}.png', w)


def main():
    colourways('teamwith-si', master_lockup(), LOGO, (600, 1200, 2400))
    colourways('teamwith-si_logotype', master_logotype(), LOGO, (400, 1200))
    colourways('teamwith-si_mark', handshake(), LOGO, (256, 1024))

    side, radius, mark = app_icon()
    tile = export.tile_svg(side, radius, mark, ROYAL_BLUE, WHITE)
    export.write(LOGO / 'teamwith-si_app-icon.svg', tile)
    for w in (1024, 512, 180):
        export.png(tile, LOGO / 'png' / f'teamwith-si_app-icon_{w}.png', w)

    # small sizes get a slightly heavier pen so the fingers survive at 16-32 px
    side, radius, mark = app_icon(mark_ratio=0.66, thicken=2.5)
    fav = export.tile_svg(side, radius, mark, ROYAL_BLUE, WHITE)
    export.write(LOGO / 'favicon.svg', fav)
    for w in (32, 16):
        export.png(fav, LOGO / 'png' / f'favicon_{w}.png', w)
    export.ico(fav, LOGO / 'favicon.ico')

    # 1:1 squares for avatars: full bleed, platforms apply their own mask
    for name, geom in (('handshake', square_handshake()), ('si', square_si())):
        for suffix, bg, fg in (('', ROYAL_BLUE, WHITE), ('_white-bg', WHITE, ROYAL_BLUE)):
            doc = export.tile_svg(1000.0, 0, geom, bg, fg)
            export.write(LOGO / 'square' / f'teamwith-si_square-{name}{suffix}.svg', doc)
            for w in (1024, 512):
                export.png(doc, LOGO / 'square' / 'png' / f'teamwith-si_square-{name}{suffix}_{w}.png', w)
        export.write(LOGO / 'square' / f'teamwith-si_square-{name}_transparent.svg',
                     export.svg([(geom, ROYAL_BLUE)], bounds=(0, 0, 1000.0, 1000.0)))

    fm = PRODUCTS / 'filemaster'
    colourways('filemaster.teamwith-si_stacked', filemaster_stack(), fm, (1200, 2400))
    colourways('filemaster.teamwith-si', filemaster_lockup(), fm, (1200, 2400))
    colourways('filemaster.teamwith-si_logotype', filemaster_lockup(with_full_name=False), fm, (1200,))
    colourways('filemaster_icon', document(), fm, (256,))


if __name__ == '__main__':
    main()
