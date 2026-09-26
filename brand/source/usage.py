"""A4 usage guide for the logo package (HTML, rendered to PDF by package.py)."""
from pathlib import Path

import export
from guidelines import build_sprite, clearspace_svg

ROOT = Path(__file__).resolve().parent.parent


def page():
    sp = build_sprite()
    u = sp.use
    body = BODY
    for key, val in {
        'SPRITE': sp.html(),
        'HEAD_LOGO': u('logotype', 'head-logo', 'teamwith.si'),
        'HERO': u('lockup', 'hero', 'teamwith.si 主标志'),
        'T_LOCKUP': u('lockup', 'th-w', ''), 'T_LOGOTYPE': u('logotype', 'th-w', ''),
        'T_MARK': u('mark', 'th-h', ''), 'T_SQ': u('sq-si', 'th-sq', ''), 'T_SQ2': u('sq-hand', 'th-sq', ''),
        'T_APP': u('app', 'th-sq r', ''), 'T_FAV': u('fav', 'th-fav', ''), 'T_FM': u('fm-stack', 'th-w', ''),
        'CLEAR': clearspace_svg(),
        'BG_WHITE': u('logotype', 'bg-logo', ''), 'BG_BLUE': u('logotype', 'bg-logo', ''),
        'BG_NAVY': u('logotype', 'bg-logo', ''), 'BG_MIST': u('logotype', 'bg-logo', ''),
        'BG_BLACK': u('logotype', 'bg-logo', ''),
        'D_STRETCH': u('logotype', 'd-logo', '', ' preserveAspectRatio="none" style="aspect-ratio:10/1"'),
        'D_COLOR': u('logotype', 'd-logo d-orange', ''), 'D_DOT': u('plain', 'd-logo', ''),
        'D_ROT': u('logotype', 'd-logo d-rot', ''), 'D_FX': u('logotype', 'd-logo d-fx', ''),
        'D_MARK': u('mark', 'd-mark', ''),
        'FM': u('fm-stack', 'fm', 'filemaster.teamwith.si 三行组合'),
        'FM_H': u('fm', 'fm-h', 'filemaster.teamwith.si 横版'),
    }.items():
        body = body.replace('{{' + key + '}}', val)
    return ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n<title>teamwith.si 标志包使用说明</title>\n'
            + STYLE + '</head>\n<body>\n' + body + '</body>\n</html>\n')


STYLE = """<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+SC:wght@400;500;700;900&family=Nunito:wght@600;800;900&display=swap">
<style>
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#FFFFFF}
body{font-family:"Nunito","Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif;color:#111A2E;font-size:9.4pt;line-height:1.6;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}
code,.mono{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.92em}
.sheet{width:210mm;height:297mm;padding:14mm 16mm 12mm;display:flex;flex-direction:column;gap:5.5mm;break-after:page;overflow:hidden;position:relative}
.sheet:last-child{break-after:auto}
.head{display:flex;justify-content:space-between;align-items:center;padding-bottom:3.5mm;border-bottom:.3mm solid #DCE2EC}
.head-logo{height:7mm;width:auto;color:#123E8C}
.head span{font-size:8pt;color:#56637F;font-weight:700;letter-spacing:.04em}
.foot{margin-top:auto;display:flex;justify-content:space-between;font-size:7.5pt;color:#8490A8;border-top:.3mm solid #DCE2EC;padding-top:3mm}
h1{font-size:21pt;font-weight:900;line-height:1.25;margin:0}
h2{font-size:12.5pt;font-weight:900;margin:0 0 2.5mm;display:flex;gap:2.5mm;align-items:baseline}
h2 i{font-style:normal;font-family:"IBM Plex Mono",monospace;font-size:8.5pt;color:#123E8C;font-weight:500}
p{margin:0}
.lead{color:#56637F;font-size:10pt;max-width:150mm}
.hero-box{border:.3mm solid #DCE2EC;border-radius:4mm;display:grid;place-items:center;padding:11mm 0}
.hero{width:120mm;height:auto;color:#123E8C}
.rows{display:grid;border-top:.3mm solid #DCE2EC}
.row{display:grid;grid-template-columns:30mm 40mm 1fr;gap:4mm;align-items:center;padding:2.3mm 0;border-bottom:.3mm solid #DCE2EC}
.row .th{display:flex;align-items:center;justify-content:center;height:11mm;color:#123E8C}
.th-w{width:28mm;height:auto}.th-h{height:10mm;width:auto}.th-sq{width:9mm;height:9mm}.r{border-radius:2mm}.th-fav{width:6mm;height:6mm}
.row code{color:#123E8C;font-weight:500}
.row b{display:block;font-size:9.4pt}
.row small{color:#56637F;font-size:8.3pt;line-height:1.5;display:block}
.pair{display:flex;gap:2mm;align-items:center}
.scene{display:grid;grid-template-columns:44mm 1fr;gap:1.5mm 5mm;border-top:.3mm solid #DCE2EC}
.scene div{padding:2.1mm 0;border-bottom:.3mm solid #DCE2EC}
.scene .k{font-weight:800}
.scene code{color:#123E8C}
.scene small{color:#56637F;display:block;font-size:8.2pt}
.naming{display:flex;flex-wrap:wrap;gap:0;font-family:"IBM Plex Mono",monospace;font-size:10.5pt;margin-top:1mm}
.naming span{display:grid;justify-items:center;padding:0 .3mm}
.naming em{font-style:normal;font-family:"Noto Sans SC",sans-serif;font-size:7.3pt;color:#56637F;border-top:.3mm solid #9DB0D6;padding-top:.6mm;margin-top:.6mm}
.naming .c1{color:#123E8C}.naming .c2{color:#C23B35}.naming .c3{color:#1D7A4B}.naming .c4{color:#8A5A00}
.notes{font-size:8.3pt;color:#56637F;margin-top:1.8mm}
.sw{display:grid;grid-template-columns:repeat(5,1fr);gap:3mm}
.sw div{border:.3mm solid #DCE2EC;border-radius:3mm;overflow:hidden}
.sw i{display:block;height:15mm}
.sw p{padding:2mm 2.4mm;font-size:7.6pt;line-height:1.45;color:#56637F}
.sw p b{display:block;color:#111A2E;font-size:8.8pt}
.two{display:grid;grid-template-columns:1fr 1fr;gap:6mm}
.clear{border:.3mm solid #DCE2EC;border-radius:3mm;padding:2mm;background:#FFFFFF}
.clear svg{width:100%;height:auto;display:block}
.dg-guide{stroke:#9DB0D6;stroke-width:1.6;stroke-dasharray:7 7}
.dg-ink{fill:#123E8C;fill-opacity:.9}
.dg-box{fill:none;stroke:#C23B35;stroke-width:1.8;stroke-dasharray:6 5}
.dg-zone{fill:#E8EEF8;stroke:#9DB0D6;stroke-width:2;stroke-dasharray:8 7}
.dg-unit{fill:rgba(18,62,140,.10);stroke:#9DB0D6;stroke-width:1.5}
.dg-unit-t{font:italic 700 34px "Nunito",sans-serif;fill:#123E8C}
ul.min{margin:0;padding:0;list-style:none;display:grid;gap:1.6mm}
ul.min li{display:grid;grid-template-columns:24mm 1fr;gap:3mm;font-size:8.8pt;border-bottom:.3mm solid #DCE2EC;padding-bottom:1.6mm}
ul.min b{color:#123E8C}
.bgs{display:grid;grid-template-columns:repeat(5,1fr);gap:2.5mm}
.bgs figure{margin:0;display:grid;gap:1.3mm}
.bgs .tile{height:15mm;border-radius:2.5mm;display:grid;place-items:center;border:.3mm solid #DCE2EC}
.bg-logo{width:80%;height:auto}
.bgs figcaption{font-size:7.4pt;color:#56637F;line-height:1.4}
.donts{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm}
.dont{border:.3mm solid #DCE2EC;border-radius:3mm;overflow:hidden}
.dont .st{height:17mm;display:grid;place-items:center;position:relative;color:#123E8C;overflow:hidden}
.dont .st::after{content:"✕";position:absolute;top:1.5mm;right:1.8mm;width:4.2mm;height:4.2mm;border-radius:50%;background:#C23B35;color:#FFFFFF;
  font-size:6.5pt;font-weight:900;display:grid;place-items:center}
.dont p{font-size:7.9pt;padding:1.6mm 2.4mm 2mm;color:#56637F;border-top:.3mm solid #EEF1F6}
.dont p b{color:#111A2E}
.d-logo{width:34mm;height:auto}.d-orange{color:#E8612C}.d-rot{transform:rotate(-9deg)}
.d-fx{filter:drop-shadow(1.2px 1.5px 0 #F2B233) drop-shadow(0 2px 3px rgba(0,0,0,.35))}
.d-font{display:flex;align-items:center;gap:1mm;font-family:Georgia,"Times New Roman",serif;font-size:13pt;white-space:nowrap}
.d-mark{width:5.5mm;height:auto}
.fm-box{border:.3mm solid #DCE2EC;border-radius:3mm;padding:4.5mm 8mm 3.5mm;display:grid;gap:2mm;justify-items:center}
.fm-note{margin-bottom:1.5mm}
.tight{gap:4.2mm}
.tight .kv div{padding:1.5mm 0}
.domain{font-family:"IBM Plex Mono",monospace;font-size:11pt;color:#56637F}
.domain b{color:#C23B35;font-size:1.3em}
.fm{width:82mm;height:auto;color:#123E8C}
.fm-h{width:104mm;height:auto;color:#123E8C}
.fm-note{font-size:7.8pt;color:#56637F}
ol{margin:0;padding-left:5mm;display:grid;gap:1.2mm;font-size:8.9pt}
.kv{display:grid;grid-template-columns:34mm 1fr;border-top:.3mm solid #DCE2EC}
.kv div{padding:2mm 0;border-bottom:.3mm solid #DCE2EC;font-size:8.8pt}
.kv .k{font-weight:800}
.cmd{background:#0B1730;color:#DCE6F8;border-radius:2.5mm;padding:3mm 4mm;font-family:"IBM Plex Mono",monospace;font-size:8pt;white-space:pre;line-height:1.55}
</style>
"""

BODY = """{{SPRITE}}
<div class="sheet">
 <div class="head">{{HEAD_LOGO}}<span>标志包使用说明 · v1.0 · 2026-09</span></div>
 <h1>teamwith.si 标志包使用说明</h1>
 <p class="lead">这个压缩包里是 teamwith.si 的全部终版标志。按下面的文件夹和场景对照挑文件即可，不需要自己改图。完整规范见包里的「品牌手册」。</p>
 <div class="hero-box">{{HERO}}</div>
 <section>
  <h2><i>01</i>包里有什么</h2>
  <div class="rows">
   <div class="row"><div class="th">{{T_LOCKUP}}</div><code>01_Primary-Lockup</code><div><b>主标志（含全称）</b><small>默认使用。官网首页、名片、海报、PPT 封面。SVG / PDF / PNG，皇家蓝、白、黑三色。</small></div></div>
   <div class="row"><div class="th">{{T_LOGOTYPE}}</div><code>02_Logotype</code><div><b>简标（不含全称）</b><small>宽度小于 200 px 的地方：导航栏、页眉页脚、水印。</small></div></div>
   <div class="row"><div class="th">{{T_MARK}}</div><code>03_Mark</code><div><b>握手图形</b><small>单独使用的图形：贴纸、周边、装饰。</small></div></div>
   <div class="row"><div class="th pair">{{T_SQ2}}{{T_SQ}}</div><code>04_Square</code><div><b>方形标志 1:1 · 握手 / Si</b><small>社交头像、公众号、群头像。蓝底、白底、透明三种，PNG 1024 / 512 px。</small></div></div>
   <div class="row"><div class="th">{{T_APP}}</div><code>05_App-Icon</code><div><b>App 图标</b><small>应用商店与手机桌面。1024 / 512 / 180 px。</small></div></div>
   <div class="row"><div class="th">{{T_FAV}}</div><code>06_Favicon</code><div><b>网站图标</b><small>浏览器标签页。16 / 32 px 用加粗版，favicon.ico 放在网站根目录。</small></div></div>
   <div class="row"><div class="th">{{T_FM}}</div><code>07_FileMaster</code><div><b>子品牌 filemaster.teamwith.si</b><small>三行组合（标准）、横版、横版简标、文件图标。</small></div></div>
   <div class="row"><div class="th"><code>PDF · HTML</code></div><code>00_Brand-Book</code><div><b>品牌手册</b><small>标准制图、安全空间、标准色、字体、应用示范、禁用示例的完整版本。</small></div></div>
   <div class="row"><div class="th"><code>TXT</code></div><code>licenses</code><div><b>授权文件</b><small>握手图形的开源许可证（Apache-2.0），随包保留即可。</small></div></div>
  </div>
 </section>
 <div class="foot"><span>teamwith.si</span><span>1 / 4</span></div>
</div>

<div class="sheet">
 <div class="head">{{HEAD_LOGO}}<span>标志包使用说明 · v1.0 · 2026-09</span></div>
 <section>
  <h2><i>02</i>按场景选文件</h2>
  <div class="scene">
   <div class="k">网页、App 界面</div><div><code>svg/</code><small>矢量，任意缩放不失真。前端直接引用 SVG。</small></div>
   <div class="k">印刷：名片、海报、易拉宝</div><div><code>pdf/</code><small>矢量 PDF，直接交给印厂。印厂要 CMYK 数值时见下方标准色，印前请打样。</small></div>
   <div class="k">Word、PPT、微信文章</div><div><code>png/ …_1200.png</code> 或 <code>…_2400.png</code><small>透明底 PNG，数字是像素宽度，屏幕投影选 2400。</small></div>
   <div class="k">深色或蓝色背景</div><div><code>…_white</code><small>白色版。不要把蓝色版直接放在深色背景上。</small></div>
   <div class="k">单色印刷、盖章、传真</div><div><code>…_black</code><small>纯黑单色版。</small></div>
   <div class="k">社交头像</div><div><code>04_Square/png/…_1024.png</code><small>平台会自动裁成圆形或圆角，图形已按视觉重心居中，不会被切到。</small></div>
   <div class="k">iOS / Android 图标</div><div><code>05_App-Icon/png/…_1024.png</code><small>上传 1024 的方图，圆角由系统生成。</small></div>
   <div class="k">网站图标</div><div><code>06_Favicon/favicon.ico</code> + <code>favicon.svg</code><small>&lt;link rel="icon" href="/favicon.svg"&gt;，同时保留 /favicon.ico 给旧浏览器。</small></div>
  </div>
 </section>
 <section>
  <h2><i>03</i>文件命名</h2>
  <div class="naming"><span class="c1">teamwith-si<em>品牌</em></span><span class="c2">_logotype<em>版本</em></span><span class="c3">_white<em>颜色</em></span><span class="c4">_1200<em>宽度 px</em></span><span>.png<em>格式</em></span></div>
  <p class="notes">版本：无后缀为主标志，_logotype 简标，_mark 握手图形，_square-handshake / _square-si 方形标志，_app-icon App 图标。颜色：无后缀为皇家蓝，_white 白色，_black 黑色，_white-bg 白底，_transparent 透明底。</p>
 </section>
 <section>
  <h2><i>04</i>标准色</h2>
  <div class="sw">
   <div><i style="background:#123E8C"></i><p><b>皇家蓝</b>#123E8C<br>RGB 18 62 140<br>CMYK 87 56 0 45<br>≈ PMS 7687 C</p></div>
   <div><i style="background:#0B2554"></i><p><b>深夜蓝</b>#0B2554<br>RGB 11 37 84<br>CMYK 87 56 0 67<br>深色底</p></div>
   <div><i style="background:#E8EEF8"></i><p><b>雾蓝</b>#E8EEF8<br>RGB 232 238 248<br>CMYK 6 4 0 3<br>浅色底</p></div>
   <div><i style="background:#FFFFFF;border-bottom:.3mm solid #DCE2EC"></i><p><b>纸白</b>#FFFFFF<br>RGB 255 255 255<br>CMYK 0 0 0 0<br>主背景</p></div>
   <div><i style="background:#111A2E"></i><p><b>墨色</b>#111A2E<br>RGB 17 26 46<br>CMYK 63 43 0 82<br>正文</p></div>
  </div>
  <p class="notes">皇家蓝是唯一的品牌主色。CMYK 为直接换算值，不同纸张和印厂会有偏差，批量印刷前请打样校色。</p>
 </section>
 <div class="foot"><span>teamwith.si</span><span>2 / 4</span></div>
</div>

<div class="sheet">
 <div class="head">{{HEAD_LOGO}}<span>标志包使用说明 · v1.0 · 2026-09</span></div>
 <section>
  <h2><i>05</i>安全空间与最小尺寸</h2>
  <div class="two">
   <div class="clear">{{CLEAR}}</div>
   <div>
    <p style="font-size:8.9pt;margin-bottom:2.5mm">标志四周至少留出 <b>1 个 x 高</b>的空白（约等于 team 里字母 e 的高度），其他文字和图形不要进入这个区域。</p>
    <ul class="min">
     <li><b>主标志</b><span>≥ 200 px 宽，印刷 ≥ 45 mm。更小时全称行看不清，改用简标。</span></li>
     <li><b>简标</b><span>≥ 96 px 宽，印刷 ≥ 22 mm。</span></li>
     <li><b>方形标志</b><span>≥ 32 px。</span></li>
     <li><b>favicon</b><span>16 / 32 px 使用 06_Favicon 里的加粗版。</span></li>
    </ul>
   </div>
  </div>
 </section>
 <section>
  <h2><i>06</i>放在什么背景上</h2>
  <div class="bgs">
   <figure><div class="tile" style="background:#FFFFFF;color:#123E8C">{{BG_WHITE}}</div><figcaption>白色、浅色底：皇家蓝版</figcaption></figure>
   <figure><div class="tile" style="background:#E8EEF8;color:#123E8C">{{BG_MIST}}</div><figcaption>雾蓝底：皇家蓝版</figcaption></figure>
   <figure><div class="tile" style="background:#123E8C;color:#FFFFFF;border-color:#123E8C">{{BG_BLUE}}</div><figcaption>皇家蓝底：白色版</figcaption></figure>
   <figure><div class="tile" style="background:#0B2554;color:#FFFFFF;border-color:#0B2554">{{BG_NAVY}}</div><figcaption>深色、照片暗部：白色版</figcaption></figure>
   <figure><div class="tile" style="background:#FFFFFF;color:#000000">{{BG_BLACK}}</div><figcaption>单色场景：黑色版</figcaption></figure>
  </div>
 </section>
 <section>
  <h2><i>07</i>不要这样用</h2>
  <div class="donts">
   <div class="dont"><div class="st">{{D_STRETCH}}</div><p><b>不要拉伸或压扁。</b>缩放时锁定比例。</p></div>
   <div class="dont"><div class="st">{{D_COLOR}}</div><p><b>不要换颜色。</b>只用皇家蓝、白、黑。</p></div>
   <div class="dont"><div class="st">{{D_DOT}}</div><p><b>不要把握手换回句点。</b></p></div>
   <div class="dont"><div class="st">{{D_ROT}}</div><p><b>不要旋转或倾斜。</b></p></div>
   <div class="dont"><div class="st">{{D_FX}}</div><p><b>不要加阴影、描边、渐变。</b></p></div>
   <div class="dont"><div class="st"><div class="d-font">team with{{D_MARK}}si</div></div><p><b>不要用字体重新打字。</b>标志字是定制的。</p></div>
  </div>
 </section>
 <div class="foot"><span>teamwith.si</span><span>3 / 4</span></div>
</div>

<div class="sheet tight">
 <div class="head">{{HEAD_LOGO}}<span>标志包使用说明 · v1.0 · 2026-09</span></div>
 <section>
  <h2><i>08</i>子品牌扩展</h2>
  <div class="fm-box"><p class="domain">filemaster<b>.</b>teamwith<b>.</b>si</p>{{FM}}<p class="fm-note">三行组合（标准）</p>{{FM_H}}<p class="fm-note">横版（网站页头、横幅等宽幅场景）</p></div>
  <ol style="margin-top:3mm">
   <li>产品名只是前缀：标准用三行组合，第一行产品名小写、不加图案，字高与全称相同；下面是主标志与全称，整块不动。</li>
   <li>宽幅场景用横版：子域名里的点换成产品图标，图标用同一支笔画，高度是握手的 0.9 倍。</li>
   <li>新增产品时请联系设计方按此规则出图，不要自行拼接。</li>
  </ol>
 </section>
 <section>
  <h2><i>09</i>字体</h2>
  <div class="kv">
   <div class="k">标志字</div><div>定制单线圆头字，没有对应字库。任何场合都直接用标志文件，不要打字代替。</div>
   <div class="k">英文 · Nunito</div><div>标题与正文，fonts.google.com/specimen/Nunito（SIL OFL，免费商用）</div>
   <div class="k">中文 · 思源黑体</div><div>Noto Sans SC，标题用 Black / Bold，正文用 Regular（SIL OFL，免费商用）</div>
   <div class="k">数据 · IBM Plex Mono</div><div>数字、代码、网址（SIL OFL，免费商用）</div>
  </div>
 </section>
 <section>
  <h2><i>10</i>授权与来源</h2>
  <div class="kv">
   <div class="k">握手图形</div><div>改自 Google Material Symbols「handshake」，Apache License 2.0，可商用。请随文件保留 licenses 文件夹里的许可证。</div>
   <div class="k">字母与组合</div><div>本项目定制绘制，不含任何字库字体。</div>
   <div class="k">商标注册</div><div>如需注册商标，建议先将握手图形重绘为原创造型，以获得完整的独占性。</div>
  </div>
 </section>
 <section>
  <h2><i>11</i>版本与源文件</h2>
  <div class="kv" style="margin-bottom:3mm">
   <div class="k">版本</div><div>v1.0 · 2026-09-26</div>
   <div class="k">源文件</div><div>GitHub 仓库 daishuge/fakegpt_with_history 的 brand/ 目录，所有文件由同一份脚本生成。</div>
  </div>
  <div class="cmd">cd brand/source
pip install -r requirements.txt
python build.py      # 重新生成全部标志文件
python package.py    # 重新生成本压缩包（需要 Node.js 与 Playwright 渲染 PDF）</div>
 </section>
 <div class="foot"><span>teamwith.si</span><span>4 / 4</span></div>
</div>
"""


if __name__ == '__main__':
    out = ROOT / 'guidelines' / 'usage-guide.html'
    export.write(out, page())
    print('wrote', out)
