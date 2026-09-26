"""Build the brand book page from the same geometry as the logo files.

    python guidelines.py            -> ../guidelines/index.html (standalone page)
    python guidelines.py --fragment -> page body for publishing as an Artifact
"""
import sys
from pathlib import Path

from shapely import affinity
from shapely.ops import nearest_points

import export
from lettering import A, D, W, X, set_text
from lockups import (FULL_NAME, MARK_GAP, app_icon, clear_space_box, filemaster_lockup, master_lockup,
                     master_logotype, master_pieces, square_handshake, square_si)
from marks import document, handshake

ROOT = Path(__file__).resolve().parent.parent
N = export._num


class Sprite:
    def __init__(self):
        self.symbols, self.boxes = [], {}

    def add(self, sid, geom):
        x0, y0, x1, y1 = geom.bounds
        self.boxes[sid] = (x1 - x0, y1 - y0)
        self.symbols.append(f'<symbol id="{sid}" viewBox="0 0 {N(x1 - x0)} {N(y1 - y0)}">'
                            f'<path fill="currentColor" fill-rule="evenodd" d="{export.path_d(geom, x0, y0)}"/></symbol>')

    def add_tile(self, sid, side, radius, mark, bg='#123E8C', fg='#FFFFFF'):
        self.boxes[sid] = (side, side)
        self.symbols.append(f'<symbol id="{sid}" viewBox="0 0 {N(side)} {N(side)}">'
                            f'<rect width="{N(side)}" height="{N(side)}" rx="{N(radius)}" fill="{bg}"/>'
                            f'<path fill="{fg}" fill-rule="evenodd" d="{export.path_d(mark)}"/></symbol>')

    def use(self, sid, cls='', label='', extra=''):
        w, h = self.boxes[sid]
        aria = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
        return f'<svg class="{cls}" viewBox="0 0 {N(w)} {N(h)}" {aria}{extra}><use href="#{sid}"/></svg>'

    def html(self):
        return ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
                + ''.join(self.symbols) + '</defs></svg>')


def construction_svg():
    """Logotype + full name with guide lines and the key measurements, in logo units."""
    left, mark, right = master_pieces()
    logo = master_logotype()
    full = master_lockup()
    lx0, _, lx1, _ = logo.bounds
    ox, oy, w, h = -330.0, -215.0, lx1 + 400.0, 400.0
    guides = [(-A, '升部线', 'ascender'), (-X, 'x 高 100', 'x-height'), (0, '基线', 'baseline'), (D, '降部线', 'descender'),
              (D + FULL_NAME['gap'], '全称顶线', ''), (D + FULL_NAME['gap'] + FULL_NAME['cap'], '全称基线', '')]
    g = [f'<svg class="diagram" viewBox="{N(ox)} {N(oy)} {N(w)} {N(h)}" role="img" '
         f'aria-label="标准制图：x 高 100，笔画 20，握手从降部线到升部线">']
    for y, zh, en in guides:
        g.append(f'<line class="dg-guide" x1="-24" y1="{N(y)}" x2="{N(lx1 + 24)}" y2="{N(y)}"/>')
        g.append(f'<text class="dg-label" x="-40" y="{N(y + 6)}" text-anchor="end">{zh}</text>')
    g.append(f'<path class="dg-ink" fill-rule="evenodd" d="{export.path_d(full)}"/>')
    # handshake box: descender -> ascender
    mx0, my0, mx1, my1 = mark.bounds
    g.append(f'<rect class="dg-box" x="{N(mx0)}" y="{N(-A)}" width="{N(mx1 - mx0)}" height="{N(A + D)}"/>')
    g.append(f'<text class="dg-note" x="{N((mx0 + mx1) / 2)}" y="{N(-A - 16)}" text-anchor="middle">握手高 = 升部 + 降部 = 210</text>')
    # optical gaps either side of the handshake
    for a, b in ((left, mark), (mark, right)):
        p, q = nearest_points(a, b)
        g.append(f'<line class="dg-dim" x1="{N(p.x)}" y1="{N(p.y)}" x2="{N(q.x)}" y2="{N(q.y)}"/>')
        g.append(f'<circle class="dg-pt" cx="{N(p.x)}" cy="{N(p.y)}" r="4"/><circle class="dg-pt" cx="{N(q.x)}" cy="{N(q.y)}" r="4"/>')
    p, _ = nearest_points(left, mark)
    _, q = nearest_points(mark, right)
    g.append(f'<text class="dg-note" x="{N(p.x - 6)}" y="46" text-anchor="end">间距 22</text>')
    g.append(f'<text class="dg-note" x="{N(q.x + 6)}" y="46" text-anchor="start">22</text>')
    # pen width on the stem of the first t (centre line x = 28)
    g.append(f'<line class="dg-dim" x1="{N(18)}" y1="-58" x2="{N(38)}" y2="-58"/>'
             f'<text class="dg-note" x="28" y="-170" text-anchor="middle">笔画 20</text>'
             f'<line class="dg-lead" x1="28" y1="-162" x2="28" y2="-66"/>')
    g.append('</svg>')
    return ''.join(g)


def clearspace_svg():
    full = master_lockup()
    cs = clear_space_box(full, X)
    x0, y0, x1, y1 = cs.bounds
    pad = 26
    s = [f'<svg class="diagram" viewBox="{N(x0 - pad)} {N(y0 - pad)} {N(x1 - x0 + 2 * pad)} {N(y1 - y0 + 2 * pad)}" '
         f'role="img" aria-label="安全空间：四周至少留出 1 个 x 高">',
         f'<rect class="dg-zone" x="{N(x0)}" y="{N(y0)}" width="{N(x1 - x0)}" height="{N(y1 - y0)}"/>',
         f'<rect class="dg-box" x="{N(full.bounds[0])}" y="{N(full.bounds[1])}" width="{N(full.bounds[2] - full.bounds[0])}" '
         f'height="{N(full.bounds[3] - full.bounds[1])}"/>',
         f'<path class="dg-ink" fill-rule="evenodd" d="{export.path_d(full)}"/>']
    for cx, cy in ((x0, y0), (x1 - X, y0), (x0, y1 - X), (x1 - X, y1 - X)):
        s.append(f'<rect class="dg-unit" x="{N(cx)}" y="{N(cy)}" width="{N(X)}" height="{N(X)}"/>'
                 f'<text class="dg-unit-t" x="{N(cx + X / 2)}" y="{N(cy + X / 2 + 12)}" text-anchor="middle">x</text>')
    s.append('</svg>')
    return ''.join(s)


def heart_reveal_svg():
    hs = handshake()
    shell = hs.buffer(16, quad_segs=24)
    ring = max([shell] if shell.geom_type == 'Polygon' else list(shell.geoms), key=lambda p: p.area).exterior
    x0, y0, x1, y1 = shell.bounds
    pad = 14
    pts = 'M' + 'L'.join(f'{N(x - x0 + pad)} {N(y - y0 + pad)}' for x, y in list(ring.simplify(0.3).coords)[:-1]) + 'Z'
    return (f'<svg class="reveal" viewBox="0 0 {N(x1 - x0 + 2 * pad)} {N(y1 - y0 + 2 * pad)}" role="img" '
            f'aria-label="握手的外轮廓是一颗心"><path class="rv-heart" d="{pts}"/>'
            f'<path class="rv-hand" fill-rule="evenodd" d="{export.path_d(hs, x0 - pad, y0 - pad)}"/></svg>')


def build_sprite():
    sp = Sprite()
    sp.add('lockup', master_lockup())
    sp.add('logotype', master_logotype())
    sp.add('mark', handshake())
    sp.add('plain', set_text('teamwith.si'))
    sp.add('fm', filemaster_lockup())
    sp.add('fm-logotype', filemaster_lockup(with_full_name=False))
    sp.add('doc', document())
    side, radius, m = app_icon()
    sp.add_tile('app', side, radius, m)
    side, radius, m = app_icon(mark=document(), mark_ratio=0.58)
    sp.add_tile('app-fm', side, radius, m)
    side, radius, m = app_icon(mark_ratio=0.66, thicken=2.5)
    sp.add_tile('fav', side, radius, m)
    sp.add_tile('sq-hand', 1000.0, 0, square_handshake())
    sp.add_tile('sq-si', 1000.0, 0, square_si())
    sp.add_tile('sq-hand-w', 1000.0, 0, square_handshake(), '#FFFFFF', '#123E8C')
    sp.add_tile('sq-si-w', 1000.0, 0, square_si(), '#FFFFFF', '#123E8C')
    return sp


def page(fragment=False):
    sp = build_sprite()
    u = sp.use
    body = BODY
    for key, val in {
        'SPRITE': sp.html(),
        'TOP_LOGO': u('logotype', 'top-logo', 'teamwith.si'),
        'HERO': u('lockup', 'hero-logo', 'team with Super Intelligence 主标志'),
        'PLAIN': u('plain', 'idea-plain', 'teamwith.si 原始域名'),
        'LOGOTYPE_IDEA': u('logotype', 'idea-logo', 'team with 握手 si'),
        'REVEAL': heart_reveal_svg(),
        'LOCKUP': u('lockup', 'spec-logo', '主标志'),
        'LOGOTYPE': u('logotype', 'spec-logo', '简标'),
        'APP': u('app', 'spec-app', 'App 图标'),
        'MARK': u('mark', 'spec-mark', '握手图形'),
        'SQ_HAND': u('sq-hand', 'sq', '方形标志：握手'),
        'SQ_SI': u('sq-si', 'sq', '方形标志：Si'),
        'SQ_HAND_W': u('sq-hand-w', 'sq sq-w', '方形标志：握手，白底'),
        'SQ_SI_W': u('sq-si-w', 'sq sq-w', '方形标志：Si，白底'),
        'CONSTRUCTION': construction_svg(),
        'CLEARSPACE': clearspace_svg(),
        'MIN_LOCKUP': u('lockup', 'min-lockup', '主标志最小尺寸'),
        'MIN_LOGOTYPE': u('logotype', 'min-logotype', '简标最小尺寸'),
        'MIN_FAV': u('fav', 'min-fav', 'favicon'),
        'FM': u('fm', 'spec-logo', 'filemaster.teamwith.si'),
        'FM_LOGOTYPE': u('fm-logotype', 'spec-logo', 'filemaster 简标'),
        'APP_FM': u('app-fm', 'spec-app', 'FileMaster App 图标'),
        'APP_SM': u('app', 'dock-icon', 'teamwith.si'),
        'APP_FM_SM': u('app-fm', 'dock-icon', 'FileMaster'),
        'FAV_TAB': u('fav', 'tab-fav', ''),
        'NAV_LOGO': u('logotype', 'nav-logo', 'teamwith.si'),
        'CARD_LOCKUP': u('lockup', 'card-logo', 'teamwith.si'),
        'CARD_MARK': u('mark', 'card-mark', ''),
        'DONT_STRETCH': u('logotype', 'dont-logo', '', ' preserveAspectRatio="none" style="aspect-ratio:10/1"'),
        'DONT_COLOR': u('logotype', 'dont-logo dont-orange', ''),
        'DONT_DOT': u('plain', 'dont-logo', ''),
        'DONT_ROTATE': u('logotype', 'dont-logo dont-rot', ''),
        'DONT_FX': u('logotype', 'dont-logo dont-fx', ''),
        'DONT_MARK': u('mark', 'dont-mark', ''),
    }.items():
        body = body.replace('{{' + key + '}}', val)
    if fragment:
        return HEAD + body
    return ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + HEAD + '</head>\n<body>\n' + body + '</body>\n</html>\n')


HEAD = """<title>teamwith.si 品牌手册</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+SC:wght@400;500;700;900&family=Nunito:wght@400;600;700;800;900&display=swap">
<style>
:root{
  --paper:#F3F5F9; --surface:#FFFFFF; --ink:#111A2E; --muted:#56637F; --faint:#8490A8; --line:#DCE2EC;
  --accent:#123E8C; --tint:#E8EEF8; --wrong:#C23B35;
  --sans:"Nunito","Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#0A1122; --surface:#111B31; --ink:#E6EBF5; --muted:#A2AEC6; --faint:#6E7B97; --line:#223050;
  --accent:#8FB0F0; --tint:#15223D; --wrong:#E66E68; color-scheme:dark}}
:root[data-theme="dark"]{
  --paper:#0A1122; --surface:#111B31; --ink:#E6EBF5; --muted:#A2AEC6; --faint:#6E7B97; --line:#223050;
  --accent:#8FB0F0; --tint:#15223D; --wrong:#E66E68; color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.75;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:1120px;margin-inline:auto;padding-inline:clamp(16px,4vw,40px)}
a{color:var(--accent)}
a:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
code,.mono{font-family:var(--mono);font-size:.9em}
h1,h2,h3{text-wrap:balance;margin:0}
h1{font-size:clamp(30px,5.2vw,54px);line-height:1.18;font-weight:900;letter-spacing:.01em}
h2{font-size:clamp(24px,3.2vw,32px);font-weight:900;line-height:1.3}
h3{font-size:17px;font-weight:800;line-height:1.4}
p{margin:0}
.eyebrow{font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);font-weight:700}
.lead{font-size:clamp(16px,1.9vw,18.5px);color:var(--muted);max-width:62ch}
.top{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-block:22px}
.top-logo{height:30px;width:auto;color:var(--accent)}
.top-meta{font-size:13px;color:var(--muted);font-weight:600}
.toc{display:flex;flex-wrap:wrap;gap:6px 18px;padding-block:6px 20px;font-size:14px;font-weight:700}
.toc a{text-decoration:none;color:var(--muted)}
.toc a:hover{color:var(--accent)}
.toc span{font-family:var(--mono);font-size:11.5px;color:var(--faint);margin-right:5px}
section{padding-block:clamp(48px,7vw,84px);border-top:1px solid var(--line)}
.hero{border-top:0;padding-top:clamp(24px,5vw,56px);display:grid;gap:22px}
.sec-head{display:grid;grid-template-columns:auto 1fr;column-gap:18px;row-gap:10px;align-items:baseline;margin-bottom:34px}
.num{font-family:var(--mono);font-size:14px;color:var(--accent);font-weight:500}
.sec-head .lead{grid-column:2}
.grid{display:grid;gap:18px}
.g2{grid-template-columns:repeat(2,minmax(0,1fr))}
.g3{grid-template-columns:repeat(3,minmax(0,1fr))}
.span2{grid-column:span 2}
@media (max-width:760px){.g2,.g3{grid-template-columns:minmax(0,1fr)}.span2{grid-column:auto}}
.spec{margin:0;border-radius:18px;padding:clamp(22px,4.5vw,56px);display:grid;place-items:center;min-height:220px;
  border:1px solid var(--line)}
.sp-white{background:#FFFFFF;color:#123E8C}
.sp-blue{background:#123E8C;color:#FFFFFF;border-color:#123E8C}
.sp-navy{background:#0B2554;color:#FFFFFF;border-color:#0B2554}
.sp-mist{background:#E8EEF8;color:#123E8C}
.item{display:grid;gap:12px;align-content:start}
.cap{font-size:14px;color:var(--muted);line-height:1.65}
.cap b{color:var(--ink);font-weight:800}
.hero-spec{min-height:0;padding-block:clamp(40px,9vw,120px)}
.hero-logo{width:min(900px,100%);height:auto}
.spec-logo{width:min(560px,100%);height:auto}
.spec-app{width:132px;height:132px;border-radius:30px;box-shadow:0 10px 30px -12px rgba(11,37,84,.45)}
.spec-mark{width:120px;height:auto}
.sq-row{display:flex;flex-wrap:wrap;gap:18px;justify-content:center}
.sq{width:120px;height:120px;border-radius:16px;box-shadow:0 10px 26px -14px rgba(11,37,84,.55)}
.sq-w{box-shadow:0 0 0 1px #DCE2EC,0 10px 26px -14px rgba(11,37,84,.35)}
.idea{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:18px 30px;width:100%}
.idea-plain{width:min(330px,100%);height:auto;color:#9AA6BC}
.idea-logo{width:min(380px,100%);height:auto}
.idea-arrow{font-size:30px;color:#123E8C;font-weight:300}
.reveal{width:min(230px,70%);height:auto}
.rv-heart{fill:none;stroke:#C23B35;stroke-width:3;stroke-dasharray:10 8}
.rv-hand{fill:#123E8C}
.pen{display:grid;gap:18px;justify-items:center;width:100%}
.pen-stroke{width:min(260px,80%);height:28px;border-radius:999px;background:#123E8C}
.pen-row{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
.pen-row span{font-family:var(--mono);font-size:12.5px;color:#123E8C;background:#E8EEF8;border-radius:999px;padding:3px 12px}
.scroll{overflow-x:auto;border-radius:18px;border:1px solid var(--line);background:#FFFFFF}
.diagram{display:block;width:100%;min-width:640px;height:auto}
.dg-guide{stroke:#9DB0D6;stroke-width:1.6;stroke-dasharray:7 7}
.dg-label{font:600 19px var(--sans);fill:#56637F}
.dg-note{font:700 19px var(--sans);fill:#C23B35}
.dg-ink{fill:#123E8C;fill-opacity:.9}
.dg-box{fill:none;stroke:#C23B35;stroke-width:1.8;stroke-dasharray:6 5}
.dg-dim{stroke:#C23B35;stroke-width:3}
.dg-lead{stroke:#C23B35;stroke-width:1.5}
.dg-pt{fill:#C23B35}
.dg-zone{fill:#E8EEF8;stroke:#9DB0D6;stroke-width:2;stroke-dasharray:8 7}
.dg-unit{fill:rgba(18,62,140,.10);stroke:#9DB0D6;stroke-width:1.5}
.dg-unit-t{font:italic 700 34px var(--sans);fill:#123E8C}
.specs{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px 26px;margin-top:26px}
.specs div{border-top:1px solid var(--line);padding-top:10px}
.specs dt{font-size:13px;color:var(--muted);font-weight:700}
.specs dd{margin:2px 0 0;font-size:15px;font-weight:600}
dl{margin:0}
.mins{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px;margin-top:18px}
.min{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:22px;display:grid;gap:14px}
.min-stage{height:84px;display:flex;align-items:center;justify-content:center;background:#FFFFFF;border-radius:12px;color:#123E8C}
.min-lockup{width:200px;height:auto}.min-logotype{width:96px;height:auto}.min-fav{width:16px;height:16px}
.swatches{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px}
.sw{border-radius:18px;overflow:hidden;border:1px solid var(--line);background:var(--surface)}
.sw-chip{height:128px;padding:16px;display:flex;align-items:flex-end;font-weight:800;font-size:15px}
.sw-body{padding:14px 16px 16px;display:grid;gap:3px;font-size:13px;color:var(--muted)}
.sw-body b{color:var(--ink);font-size:15px}
.sw-body code{color:var(--ink)}
.ratio{display:flex;height:44px;border-radius:12px;overflow:hidden;margin-top:18px;border:1px solid var(--line)}
.ratio div{display:flex;align-items:center;padding-inline:12px;font-size:12.5px;font-weight:700;white-space:nowrap;overflow:hidden}
.type{display:grid;gap:16px}
.type-card{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:clamp(20px,3.5vw,34px);display:grid;gap:10px}
.type-meta{font-size:13px;color:var(--muted);font-weight:700}
.t-nunito{font-family:"Nunito",sans-serif;font-weight:900;font-size:clamp(26px,4.4vw,44px);line-height:1.15;color:var(--accent)}
.t-sc{font-family:"Noto Sans SC",sans-serif;font-weight:900;font-size:clamp(24px,4vw,40px);line-height:1.25}
.t-body{font-family:"Noto Sans SC",sans-serif;font-size:16px;color:var(--muted);max-width:60ch}
.t-mono{font-family:var(--mono);font-size:15px}
.domain{font-family:var(--mono);font-size:clamp(17px,2.6vw,24px);font-weight:500;text-align:center;color:#56637F;letter-spacing:.02em}
.domain b{color:#C23B35;font-weight:700;font-size:1.25em}
.rules{display:grid;gap:10px;margin:22px 0 0;padding:0;list-style:none;counter-reset:r}
.rules li{counter-increment:r;display:grid;grid-template-columns:28px 1fr;gap:10px;font-size:15px;max-width:72ch}
.rules li::before{content:counter(r);font-family:var(--mono);font-size:12px;color:#FFFFFF;background:var(--accent);
  border-radius:999px;width:22px;height:22px;display:grid;place-items:center;margin-top:3px}
:root[data-theme="dark"] .rules li::before{color:#0A1122}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .rules li::before{color:#0A1122}}
.cards{display:flex;flex-wrap:wrap;gap:22px;justify-content:center;align-items:center;padding:clamp(18px,4vw,40px);
  background:var(--tint);border-radius:18px;border:1px solid var(--line)}
.bc{width:min(360px,100%);aspect-ratio:90/54;border-radius:10px;box-shadow:0 18px 40px -18px rgba(11,37,84,.55);
  position:relative;overflow:hidden}
.bc-front{background:#FFFFFF;color:#123E8C;display:flex;flex-direction:column;justify-content:space-between;padding:8% 8% 7%}
.card-logo{display:block;width:62%;height:auto}
.bc-info{font-size:clamp(9px,2.4vw,11.5px);line-height:1.6;color:#56637F}
.bc-info b{color:#111A2E;font-size:1.2em}
.bc-back{background:#123E8C;color:#FFFFFF;display:flex;align-items:center;justify-content:center}
.card-mark{display:block;width:24%;height:auto;margin-bottom:6%}
.bc-url{position:absolute;bottom:9%;left:0;right:0;text-align:center;font-family:var(--mono);font-size:clamp(9px,2.2vw,11px);
  letter-spacing:.12em;color:#9FB6E6}
.browser{border-radius:16px;overflow:hidden;border:1px solid var(--line);background:#FFFFFF;
  box-shadow:0 22px 50px -26px rgba(11,37,84,.45);color:#111A2E}
.b-tabs{background:#E6EAF1;padding:10px 12px 0;display:flex}
.b-tab{background:#FFFFFF;border-radius:10px 10px 0 0;padding:8px 14px;display:flex;align-items:center;gap:8px;
  font-size:12.5px;font-weight:600;max-width:100%;min-width:0}
.b-tab span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tab-fav{width:16px;height:16px;flex:none}
.b-url{background:#FFFFFF;border-bottom:1px solid #E6EAF1;padding:8px 14px}
.b-url div{background:#F1F4F9;border-radius:999px;padding:5px 14px;font-family:var(--mono);font-size:12px;color:#56637F}
.b-nav{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:16px clamp(14px,3vw,30px);
  border-bottom:1px solid #EEF1F6;flex-wrap:wrap}
.nav-logo{height:26px;width:auto;color:#123E8C}
.b-links{display:flex;gap:18px;font-size:13.5px;font-weight:700;color:#56637F;flex-wrap:wrap}
.b-btn{background:#123E8C;color:#FFFFFF;border-radius:999px;padding:7px 16px;font-size:13px;font-weight:800;white-space:nowrap}
.b-hero{padding:clamp(28px,6vw,64px) clamp(14px,3vw,30px);display:grid;gap:10px;background:linear-gradient(180deg,#FFFFFF, #F3F6FB)}
.b-hero h3{font-family:"Noto Sans SC",sans-serif;font-size:clamp(22px,4vw,38px);font-weight:900;line-height:1.25;color:#111A2E}
.b-hero p{font-size:14.5px;color:#56637F}
.dock{display:flex;gap:28px;justify-content:center;align-items:flex-start;padding:30px 20px;background:var(--tint);
  border-radius:18px;border:1px solid var(--line);flex-wrap:wrap}
.dock figure{margin:0;display:grid;gap:8px;justify-items:center;font-size:13px;font-weight:700;color:var(--muted)}
.dock-icon{width:76px;height:76px;border-radius:17px;box-shadow:0 10px 24px -12px rgba(11,37,84,.6)}
.donts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.dont{background:var(--surface);border:1px solid var(--line);border-radius:18px;overflow:hidden}
.dont-stage{background:#FFFFFF;height:130px;display:grid;place-items:center;padding:14px 20px;color:#123E8C;position:relative;
  overflow:hidden}
.dont-stage::after{content:"✕";position:absolute;top:10px;right:12px;width:26px;height:26px;border-radius:999px;background:#C23B35;
  color:#FFFFFF;font-size:14px;font-weight:900;display:grid;place-items:center}
.dont p{padding:12px 16px 14px;font-size:14px;color:var(--muted)}
.dont p b{color:var(--ink)}
.dont-logo{width:min(240px,90%);height:auto}
.dont-orange{color:#E8612C}
.dont-rot{transform:rotate(-9deg)}
.dont-fx{filter:drop-shadow(4px 5px 0 #F2B233) drop-shadow(0 8px 12px rgba(0,0,0,.35))}
.dont-font{display:flex;align-items:center;gap:6px;font-family:Georgia,"Times New Roman",serif;font-size:31px;color:#123E8C;white-space:nowrap}
.dont-mark{width:38px;height:auto}
.files{display:grid;gap:10px;margin-top:6px}
.file{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:4px 18px;padding-block:10px;border-top:1px solid var(--line);font-size:14.5px}
.file code{color:var(--accent);word-break:break-all}
.file span{color:var(--muted)}
@media (max-width:640px){.file{grid-template-columns:minmax(0,1fr)}}
.cmd{margin-top:22px;background:#0B1730;color:#DCE6F8;border-radius:14px;padding:16px 18px;font-family:var(--mono);font-size:13.5px;
  overflow-x:auto;white-space:pre}
footer{border-top:1px solid var(--line);padding-block:30px 48px;font-size:13px;color:var(--muted);display:flex;gap:10px 30px;flex-wrap:wrap}
@media print{
  @page{size:A4;margin:12mm}
  :root{--paper:#FFFFFF;--surface:#FFFFFF}
  body{font-size:13px;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .toc{display:none}
  section{padding-block:26px;break-inside:auto}
  .sec-head{margin-bottom:18px;break-after:avoid-page}
  #files{break-before:page}
  .g2{grid-template-columns:repeat(2,minmax(0,1fr))}.g3{grid-template-columns:repeat(3,minmax(0,1fr))}.span2{grid-column:span 2}
  .spec{min-height:150px;padding:22px}
  .hero-spec{padding-block:56px}
  .item,.spec,.sw,.dont,.min,.type-card,.browser,.cards,.dock,.scroll,.file,.specs div,.rules li{break-inside:avoid}
  .scroll{overflow:visible}.diagram{min-width:0}
  .spec-app,.sq,.dock-icon,.bc,.browser{box-shadow:none}
}
</style>
"""

BODY = """{{SPRITE}}
<header class="top wrap">{{TOP_LOGO}}<span class="top-meta">品牌手册 v1.0 · 2026.09</span></header>
<nav class="toc wrap" aria-label="目录">
 <a href="#idea"><span>01</span>创意</a><a href="#lockups"><span>02</span>标志组合</a><a href="#grid"><span>03</span>标准制图</a>
 <a href="#space"><span>04</span>安全空间</a><a href="#color"><span>05</span>标准色</a><a href="#type"><span>06</span>字体</a>
 <a href="#family"><span>07</span>子品牌</a><a href="#apply"><span>08</span>应用</a><a href="#donts"><span>09</span>禁用</a><a href="#files"><span>10</span>文件</a>
</nav>
<main class="wrap">
<section class="hero">
 <p class="eyebrow">teamwith.si · Brand Identity</p>
 <h1>把域名里的「.」变成一次握手</h1>
 <p class="lead">teamwith.si 读作 team with Super Intelligence，和超级智能组队。标志把域名中间的点换成一次握手，握手的外轮廓是一颗心。字母和握手出自同一支单线圆头笔，整串字本身就是标志。</p>
 <figure class="spec sp-white hero-spec">{{HERO}}</figure>
</section>

<section id="idea">
 <div class="sec-head"><span class="num">01</span><h2>创意</h2><p class="lead">三个想法叠在一起：点即握手，握手即心，一支笔写完全部。</p></div>
 <div class="grid g2">
  <div class="item span2"><figure class="spec sp-white"><div class="idea">{{PLAIN}}<span class="idea-arrow" aria-hidden="true">→</span>{{LOGOTYPE_IDEA}}</div></figure>
   <p class="cap"><b>点即握手。</b>teamwith 和 si 之间的点本来就是连接符。换成握手后，先读到名字，再看出这个点是两只握住的手。</p></div>
  <div class="item"><figure class="spec sp-white">{{REVEAL}}</figure>
   <p class="cap"><b>握手即心。</b>两只手合起来的外轮廓是一颗心。合作之外，还有信任。</p></div>
  <div class="item"><figure class="spec sp-white"><div class="pen"><div class="pen-stroke" aria-hidden="true"></div>
   <div class="pen-row"><span>笔画 20</span><span>圆头</span><span>圆角转折</span></div></div></figure>
   <p class="cap"><b>一支笔。</b>字母、握手、产品图标都用同一支单线圆头笔画成，粗细一致，所以整行字读起来是一个整体。</p></div>
 </div>
</section>

<section id="lockups">
 <div class="sec-head"><span class="num">02</span><h2>标志组合</h2><p class="lead">三种组合，按使用尺寸选择。颜色只用皇家蓝、白色和纯黑单色。</p></div>
 <div class="grid g2">
  <div class="item"><figure class="spec sp-white">{{LOCKUP}}</figure><p class="cap"><b>主标志（含全称）</b>　默认使用。官网首页、名片、文档封面、对外材料。</p></div>
  <div class="item"><figure class="spec sp-blue">{{LOCKUP}}</figure><p class="cap"><b>主标志 · 反白</b>　放在皇家蓝或深夜蓝底色上。</p></div>
  <div class="item"><figure class="spec sp-white">{{LOGOTYPE}}</figure><p class="cap"><b>简标（不含全称）</b>　宽度小于 200 px 时使用，如导航栏、页眉、水印。</p></div>
  <div class="item"><figure class="spec sp-navy">{{LOGOTYPE}}</figure><p class="cap"><b>简标 · 深色底</b>　深色界面与暗色模式。</p></div>
  <div class="item"><figure class="spec sp-white">{{APP}}</figure><p class="cap"><b>图形标 · App 图标</b>　白色握手在皇家蓝圆角方块中，占方块高度的 60%。</p></div>
  <div class="item"><figure class="spec sp-mist">{{MARK}}</figure><p class="cap"><b>图形标 · 单独使用</b>　头像、贴纸、周边。握手不单独加文字以外的装饰。</p></div>
  <div class="item span2"><figure class="spec sp-mist"><div class="sq-row">{{SQ_HAND}}{{SQ_SI}}{{SQ_HAND_W}}{{SQ_SI_W}}</div></figure>
   <p class="cap"><b>方形标志 1:1 · 握手 / Si</b>　社交头像、公众号、群头像。Si 用大写 S 配小写 i，S 的顶与 i 点齐平，字组接近正方形。满版正方形不带圆角，由平台自己裁成圆形或圆角；图形按视觉重心居中，裁成圆形也不会切到。</p></div>
 </div>
</section>

<section id="grid">
 <div class="sec-head"><span class="num">03</span><h2>标准制图</h2><p class="lead">以 x 高为 100 个单位建立网格，所有尺寸都是它的倍数或约数。</p></div>
 <div class="scroll">{{CONSTRUCTION}}</div>
 <dl class="specs">
  <div><dt>x 高 / 笔画</dt><dd>100 / 20，笔画为 x 高的五分之一</dd></div>
  <div><dt>升部 / 降部</dt><dd>150 / 60</dd></div>
  <div><dt>握手高度</dt><dd>210，从降部线到升部线，与字母共用一支笔</dd></div>
  <div><dt>握手两侧间距</dt><dd>22，按轮廓最近点计算的光学间距</dd></div>
  <div><dt>全称字高 / 笔画</dt><dd>54 / 9，距主标 36</dd></div>
  <div><dt>全称排列</dt><dd>左右与主标对齐，词距为字距的 2.6 倍</dd></div>
 </dl>
</section>

<section id="space">
 <div class="sec-head"><span class="num">04</span><h2>安全空间与最小尺寸</h2><p class="lead">标志四周至少留出 1 个 x 高的空白，其他文字和图形不进入这个区域。</p></div>
 <div class="scroll">{{CLEARSPACE}}</div>
 <div class="mins">
  <div class="min"><div class="min-stage">{{MIN_LOCKUP}}</div><p class="cap"><b>主标志 ≥ 200 px</b>　印刷 ≥ 45 mm 宽。再小时全称行不易辨认，改用简标。</p></div>
  <div class="min"><div class="min-stage">{{MIN_LOGOTYPE}}</div><p class="cap"><b>简标 ≥ 96 px</b>　印刷 ≥ 22 mm 宽。</p></div>
  <div class="min"><div class="min-stage">{{MIN_FAV}}</div><p class="cap"><b>favicon 16 / 32 px</b>　使用加粗版握手，笔画加厚 2.5 个单位，保证手指在小尺寸下不糊。</p></div>
 </div>
</section>

<section id="color">
 <div class="sec-head"><span class="num">05</span><h2>标准色</h2><p class="lead">皇家蓝是唯一的品牌主色，其余颜色用于底色和正文。CMYK 为直接换算值，印刷前请打样校色。</p></div>
 <div class="swatches">
  <div class="sw"><div class="sw-chip" style="background:#123E8C;color:#FFFFFF">皇家蓝</div><div class="sw-body"><b>Royal Blue</b><code>#123E8C</code><span>RGB 18 62 140</span><span>CMYK 87 56 0 45</span><span>参考 PANTONE 7687 C</span></div></div>
  <div class="sw"><div class="sw-chip" style="background:#0B2554;color:#FFFFFF">深夜蓝</div><div class="sw-body"><b>Deep Navy</b><code>#0B2554</code><span>RGB 11 37 84</span><span>CMYK 87 56 0 67</span><span>深色底、页脚</span></div></div>
  <div class="sw"><div class="sw-chip" style="background:#E8EEF8;color:#123E8C">雾蓝</div><div class="sw-body"><b>Mist</b><code>#E8EEF8</code><span>RGB 232 238 248</span><span>CMYK 6 4 0 3</span><span>浅色底、卡片</span></div></div>
  <div class="sw"><div class="sw-chip" style="background:#FFFFFF;color:#123E8C;box-shadow:inset 0 -1px 0 #DCE2EC">纸白</div><div class="sw-body"><b>White</b><code>#FFFFFF</code><span>RGB 255 255 255</span><span>CMYK 0 0 0 0</span><span>主背景</span></div></div>
  <div class="sw"><div class="sw-chip" style="background:#111A2E;color:#FFFFFF">墨色</div><div class="sw-body"><b>Ink</b><code>#111A2E</code><span>RGB 17 26 46</span><span>CMYK 63 43 0 82</span><span>正文文字</span></div></div>
 </div>
 <div class="ratio" role="img" aria-label="用色比例：纸白 60%，皇家蓝 25%，深夜蓝 10%，雾蓝 5%">
  <div style="flex:60;background:#FFFFFF;color:#56637F">纸白 60%</div><div style="flex:25;background:#123E8C;color:#FFFFFF">皇家蓝 25%</div>
  <div style="flex:10;background:#0B2554;color:#FFFFFF">10%</div><div style="flex:5;background:#E8EEF8;color:#123E8C"></div>
 </div>
</section>

<section id="type">
 <div class="sec-head"><span class="num">06</span><h2>字体</h2><p class="lead">标志字是定制的单线圆头字，没有对应的字库，不能用任何字体重新打出来。版面文字用下面三款开源字体。</p></div>
 <div class="type">
  <div class="type-card"><p class="type-meta">英文标题与正文 · Nunito（SIL OFL）</p><p class="t-nunito">team with Super Intelligence</p><p class="t-body">圆头人文无衬线，笔画末端和标志字一样是圆的，放在标志旁边不打架。</p></div>
  <div class="type-card"><p class="type-meta">中文 · 思源黑体 / Noto Sans SC（SIL OFL）</p><p class="t-sc">和超级智能组队，把事做成</p><p class="t-body">标题用 Black 或 Bold，正文用 Regular，行高 1.7 以上。</p></div>
  <div class="type-card"><p class="type-meta">数据与代码 · IBM Plex Mono（SIL OFL）</p><p class="t-mono">filemaster.teamwith.si　#123E8C　v1.0</p></div>
 </div>
</section>

<section id="family">
 <div class="sec-head"><span class="num">07</span><h2>子品牌</h2><p class="lead">规则只有一条：子域名里的每一个点，都换成它自己的图标。</p></div>
 <div class="grid">
  <figure class="spec sp-white" style="gap:26px"><p class="domain">filemaster<b>.</b>teamwith<b>.</b>si</p>{{FM}}</figure>
  <div class="grid g2">
   <div class="item"><figure class="spec sp-white">{{FM_LOGOTYPE}}</figure><p class="cap"><b>filemaster 简标</b>　小尺寸时去掉全称行。</p></div>
   <div class="item"><figure class="spec sp-white">{{APP_FM}}</figure><p class="cap"><b>FileMaster App 图标</b>　和主品牌同一个圆角方块、同一支笔，只换图形。</p></div>
  </div>
 </div>
 <ul class="rules">
  <li><span>产品名用同一套单线字，全部小写，放在最前面。</span></li>
  <li><span>产品图标用同一支笔画（20 单位、圆头），站在降部线上，高度是握手的 0.9 倍，视觉分量才对等。</span></li>
  <li><span>图标两侧留 22 单位的光学间距，和握手一致。</span></li>
  <li><span>主标志连同下方全称整块不动，前缀只在左侧拼接。以后新增任何 xxx.teamwith.si 都照此办理。</span></li>
 </ul>
</section>

<section id="apply">
 <div class="sec-head"><span class="num">08</span><h2>应用示范</h2><p class="lead">名片、官网和 App 图标上的实际效果。</p></div>
 <div class="grid">
  <div class="cards">
   <div class="bc bc-front">{{CARD_LOCKUP}}<div class="bc-info"><b>姓名 Name</b><br>职位 Title<br>hello@teamwith.si　·　teamwith.si</div></div>
   <div class="bc bc-back">{{CARD_MARK}}<div class="bc-url">TEAMWITH.SI</div></div>
  </div>
  <div class="browser" aria-label="官网页头示范">
   <div class="b-tabs"><div class="b-tab">{{FAV_TAB}}<span>teamwith.si · 和超级智能组队</span></div></div>
   <div class="b-url"><div>https://teamwith.si</div></div>
   <div class="b-nav">{{NAV_LOGO}}<div class="b-links"><span>产品</span><span>方案</span><span>定价</span><span>关于</span></div><span class="b-btn">开始协作</span></div>
   <div class="b-hero"><h3>和超级智能组队，把事做成。</h3><p>team with Super Intelligence</p></div>
  </div>
  <div class="dock"><figure>{{APP_SM}}<figcaption>teamwith</figcaption></figure><figure>{{APP_FM_SM}}<figcaption>FileMaster</figcaption></figure></div>
 </div>
</section>

<section id="donts">
 <div class="sec-head"><span class="num">09</span><h2>禁用示例</h2><p class="lead">标志文件请直接使用，不做任何改动。</p></div>
 <div class="donts">
  <div class="dont"><div class="dont-stage">{{DONT_STRETCH}}</div><p><b>不要拉伸或压扁。</b>缩放时锁定比例。</p></div>
  <div class="dont"><div class="dont-stage">{{DONT_COLOR}}</div><p><b>不要换成其他颜色。</b>只用皇家蓝、白或黑。</p></div>
  <div class="dont"><div class="dont-stage">{{DONT_DOT}}</div><p><b>不要把握手换回句点。</b>握手是标志的核心。</p></div>
  <div class="dont"><div class="dont-stage">{{DONT_ROTATE}}</div><p><b>不要旋转或倾斜。</b></p></div>
  <div class="dont"><div class="dont-stage">{{DONT_FX}}</div><p><b>不要加阴影、描边或渐变。</b></p></div>
  <div class="dont"><div class="dont-stage"><div class="dont-font">team with{{DONT_MARK}}si</div></div><p><b>不要用字体重新打字。</b>标志字是定制的。</p></div>
 </div>
</section>

<section id="files">
 <div class="sec-head"><span class="num">10</span><h2>文件</h2><p class="lead">所有文件在仓库 brand/ 目录下，由同一份脚本生成，改规则后重新运行即可全部同步。</p></div>
 <div class="files">
  <div class="file"><code>brand/logo/teamwith-si.svg</code><span>主标志（含全称），另有 _white、_black</span></div>
  <div class="file"><code>brand/logo/teamwith-si_logotype.svg</code><span>简标（不含全称）</span></div>
  <div class="file"><code>brand/logo/teamwith-si_mark.svg</code><span>握手图形</span></div>
  <div class="file"><code>brand/logo/teamwith-si_app-icon.svg</code><span>App 图标，PNG 为 1024 / 512 / 180 px</span></div>
  <div class="file"><code>brand/logo/favicon.ico · favicon.svg</code><span>网站图标（加粗版）</span></div>
  <div class="file"><code>brand/logo/square/</code><span>方形标志 1:1：握手、Si，蓝底 / 白底 / 透明，PNG 1024 / 512 px</span></div>
  <div class="file"><code>brand/logo/png/</code><span>各版本 PNG，透明底</span></div>
  <div class="file"><code>brand/products/filemaster/</code><span>filemaster.teamwith.si 组合、简标、文件图标</span></div>
  <div class="file"><code>brand/source/</code><span>生成脚本：单线字、握手、组合规则</span></div>
 </div>
 <div class="cmd">cd brand/source
pip install -r requirements.txt
python build.py        # 重新生成全部标志文件
python guidelines.py   # 重新生成本手册</div>
</section>
</main>
<footer class="wrap"><span>teamwith.si 品牌手册 v1.0 · 2026-09-26</span><span>握手图形改自 Material Symbols「handshake」（Apache-2.0）</span></footer>
"""


if __name__ == '__main__':
    fragment = '--fragment' in sys.argv
    out = Path(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else ROOT / 'guidelines' / 'index.html'
    export.write(out, page(fragment))
    print('wrote', out)
