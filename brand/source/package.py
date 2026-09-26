"""Assemble the release zip with every final file and the usage guide:  python package.py"""
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

import cairosvg

import build
import export
import guidelines
import usage

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOGO, FM = ROOT / 'logo', ROOT / 'products' / 'filemaster'
NAME = 'teamwith-si_brand_v1.0'
STAGE = ROOT / 'dist' / NAME
COLOURS = ('', '_white', '_black')


def render_pdf(html, pdf):
    env = dict(os.environ)
    if 'NODE_PATH' not in env:
        env['NODE_PATH'] = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
    subprocess.run(['node', str(HERE / 'render_pdf.cjs'), str(html), str(pdf)], check=True, env=env)


def put(src, rel):
    dst = STAGE / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def put_vector(stem, src_dir, folder):
    """svg/ and print-ready pdf/ for every colourway of one lockup."""
    for c in COLOURS:
        svg = src_dir / f'{stem}{c}.svg'
        put(svg, f'{folder}/svg/{svg.name}')
        pdf = STAGE / folder / 'pdf' / f'{stem}{c}.pdf'
        pdf.parent.mkdir(parents=True, exist_ok=True)
        cairosvg.svg2pdf(url=str(svg), write_to=str(pdf))


def put_pngs(pattern, src_dir, folder):
    for png in sorted(src_dir.glob(pattern)):
        put(png, f'{folder}/png/{png.name}')


def main():
    build.main()
    export.write(ROOT / 'guidelines' / 'index.html', guidelines.page())
    export.write(ROOT / 'guidelines' / 'usage-guide.html', usage.page())
    render_pdf(ROOT / 'guidelines' / 'index.html', ROOT / 'guidelines' / 'brand-book.pdf')
    render_pdf(ROOT / 'guidelines' / 'usage-guide.html', ROOT / 'guidelines' / 'usage-guide.pdf')

    if STAGE.exists():
        shutil.rmtree(STAGE)
    put(ROOT / 'guidelines' / 'usage-guide.pdf', '00_README_使用说明.pdf')
    put(ROOT / 'guidelines' / 'brand-book.pdf', '00_Brand-Book_品牌手册.pdf')
    put(ROOT / 'guidelines' / 'index.html', '00_Brand-Book_品牌手册.html')

    put_vector('teamwith-si', LOGO, '01_Primary-Lockup')
    for c in COLOURS:
        put_pngs(f'teamwith-si{c}_[0-9]*.png', LOGO / 'png', '01_Primary-Lockup')
    put_vector('teamwith-si_logotype', LOGO, '02_Logotype')
    put_pngs('teamwith-si_logotype*.png', LOGO / 'png', '02_Logotype')
    put_vector('teamwith-si_mark', LOGO, '03_Mark')
    put_pngs('teamwith-si_mark*.png', LOGO / 'png', '03_Mark')

    for svg in sorted((LOGO / 'square').glob('*.svg')):
        put(svg, f'04_Square/svg/{svg.name}')
    put_pngs('*.png', LOGO / 'square' / 'png', '04_Square')

    put(LOGO / 'teamwith-si_app-icon.svg', '05_App-Icon/teamwith-si_app-icon.svg')
    put_pngs('teamwith-si_app-icon_*.png', LOGO / 'png', '05_App-Icon')

    put(LOGO / 'favicon.ico', '06_Favicon/favicon.ico')
    put(LOGO / 'favicon.svg', '06_Favicon/favicon.svg')
    put_pngs('favicon_*.png', LOGO / 'png', '06_Favicon')

    put_vector('filemaster.teamwith-si_stacked', FM, '07_FileMaster')
    put_vector('filemaster.teamwith-si', FM, '07_FileMaster')
    put_vector('filemaster.teamwith-si_logotype', FM, '07_FileMaster')
    put_vector('filemaster_icon', FM, '07_FileMaster')
    put_pngs('*.png', FM / 'png', '07_FileMaster')

    put(HERE / 'vendor' / 'material-symbols' / 'LICENSE', 'licenses/Material-Symbols_Apache-2.0.txt')
    (STAGE / 'licenses' / 'NOTICE.txt').write_text(
        'teamwith.si brand files v1.0\n\n'
        'The handshake pictogram is adapted from Google Material Symbols "handshake"\n'
        '(rounded, weight 700), licensed under the Apache License 2.0 (see\n'
        'Material-Symbols_Apache-2.0.txt). The lettering and all lockups were drawn\n'
        'for this project and contain no font software.\n')

    archive = STAGE.parent / f'{NAME}.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(STAGE.rglob('*')):
            if f.is_file():
                z.write(f, f.relative_to(STAGE.parent))
    print('wrote', archive)


if __name__ == '__main__':
    main()
