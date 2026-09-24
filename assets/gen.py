#!/usr/bin/env python3
"""Generate banner-*.svg and boot-*.svg for light and dark themes."""
from html import escape
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "light": dict(bg1="#FFF8F0", bg2="#DDEFE6", trace="#E3D3C3", pulse="#F0A45C", pad="#D9C4AF",
                  title="#2E2A28", sub="#D9853E", muted="#7A6E66",
                  term_bg="#FFFDF9", term_bar="#F3E9DF", term_border="#E8D8C8", text="#2E2A28",
                  ok="#3F8F6E", info="#D9853E", dim="#A3968C", prompt="#3F8F6E"),
    "dark": dict(bg1="#171A1F", bg2="#1C2A25", trace="#2F3A38", pulse="#F0A45C", pad="#3C4946",
                 title="#F5EDE4", sub="#F0A45C", muted="#A3968C",
                 term_bg="#1B1917", term_bar="#26221F", term_border="#3A332E", text="#EDE3D9",
                 ok="#7FBFA4", info="#F0A45C", dim="#6F665F", prompt="#7FBFA4"),
}

# ---------------------------------------------------------------- banner
CHIP_X, CHIP_Y, CHIP_S = 810, 175, 190  # chip top-left and size

def traces():
    """Right-angle circuit traces leaving the chip, as (path, end_x, end_y)."""
    cx0, cy0, s = CHIP_X, CHIP_Y, CHIP_S
    out = []
    for i, y in enumerate([cy0 + 35, cy0 + 75, cy0 + 115, cy0 + 155]):   # left side
        x2 = cx0 - 60 - i * 25
        ey = [70, 150, 330, 385][i]
        ex = [610, 540, 520, 640][i]
        out.append((f"M{cx0} {y} H{x2} V{ey} H{ex}", ex, ey))
    for i, y in enumerate([cy0 + 35, cy0 + 95, cy0 + 155]):              # right side
        x2 = cx0 + s + 40 + i * 30
        ey = [60, 200, 380][i]
        out.append((f"M{cx0 + s} {y} H{x2} V{ey} H1200", 1200, ey))
    for i, x in enumerate([cx0 + 45, cx0 + 145]):                         # bottom
        ex = [720, 1110][i]
        out.append((f"M{x} {cy0 + s} V{cy0 + s + 60 - i * 20} H{ex} V400", ex, 400))
    return out

def banner(t):
    c = THEMES[t]
    p = []
    p.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="400" viewBox="0 0 1200 400">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c['bg1']}"/><stop offset="1" stop-color="{c['bg2']}"/>
  </linearGradient>
  <clipPath id="frame"><rect width="1200" height="400" rx="24"/></clipPath>
</defs>
<style>
  .pulse {{ fill:none; stroke:{c['pulse']}; stroke-width:4; stroke-linecap:round;
           stroke-dasharray:36 900; animation: flow 4.5s linear infinite; }}
  @keyframes flow {{ from {{ stroke-dashoffset: 936; }} to {{ stroke-dashoffset: 0; }} }}
  .led {{ animation: blink 1.6s ease-in-out infinite; }}
  @keyframes blink {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:.25; }} }}
  .cat {{ animation: bob 3.2s ease-in-out infinite; transform-origin: 905px 170px; }}
  @keyframes bob {{ 0%,100% {{ transform: rotate(-2deg); }} 50% {{ transform: rotate(2deg); }} }}
  .tail {{ animation: wag 2.4s ease-in-out infinite; transform-origin: 1000px 185px; }}
  @keyframes wag {{ 0%,100% {{ transform: rotate(0deg); }} 50% {{ transform: rotate(14deg); }} }}
  .eyes {{ animation: shut 5s ease-in-out infinite; transform-origin: 905px 118px; }}
  @keyframes shut {{ 0%,92%,100% {{ transform: scaleY(1); }} 96% {{ transform: scaleY(.2); }} }}
</style>
<g clip-path="url(#frame)">
<rect width="1200" height="400" fill="url(#bg)"/>''')
    # traces
    for i, (d, ex, ey) in enumerate(traces()):
        p.append(f'<path d="{d}" fill="none" stroke="{c["trace"]}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
        if ex < 1200 and ey < 400:
            p.append(f'<circle cx="{ex}" cy="{ey}" r="8" fill="{c["bg1"]}" stroke="{c["pad"]}" stroke-width="4"/>')
        p.append(f'<path class="pulse" d="{d}" style="animation-delay:-{i * 0.7:.1f}s"/>')
    # chip
    x, y, s = CHIP_X, CHIP_Y, CHIP_S
    for k in range(6):
        o = 22 + k * 29
        p.append(f'<rect x="{x - 14}" y="{y + o}" width="14" height="10" rx="2" fill="#B8A898"/>')
        p.append(f'<rect x="{x + s}" y="{y + o}" width="14" height="10" rx="2" fill="#B8A898"/>')
        p.append(f'<rect x="{x + o}" y="{y + s}" width="10" height="14" rx="2" fill="#B8A898"/>')
    p.append(f'''<rect x="{x}" y="{y + 6}" width="{s}" height="{s}" rx="20" fill="#000" opacity=".15"/>
<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="20" fill="#2E2A28"/>
<rect x="{x + 22}" y="{y + 22}" width="{s - 44}" height="{s - 44}" rx="12" fill="none" stroke="#4A423C" stroke-width="3"/>
<text x="{x + s / 2}" y="{y + 108}" text-anchor="middle" font-family="{MONO}" font-size="30" font-weight="700" fill="#F0A45C">NPU</text>
<text x="{x + s / 2}" y="{y + 138}" text-anchor="middle" font-family="{MONO}" font-size="15" fill="#A3968C">INT8 · 3.2ms</text>
<circle class="led" cx="{x + 36}" cy="{y + 158}" r="7" fill="#7FBFA4"/>''')
    # cat (sits on the chip)
    p.append('''<g class="tail"><path d="M985 190 q70 -10 60 -80 q-6 -30 -28 -26" fill="none" stroke="#F0A45C" stroke-width="22" stroke-linecap="round"/></g>
<g class="cat">
  <ellipse cx="905" cy="182" rx="80" ry="30" fill="#E8964F"/>
  <path d="M835 110 L845 35 L890 72z" fill="#F0A45C"/><path d="M975 110 L965 35 L920 72z" fill="#F0A45C"/>
  <path d="M848 52 L853 88 L876 76z" fill="#F7C9B6"/><path d="M962 52 L957 88 L934 76z" fill="#F7C9B6"/>
  <ellipse cx="905" cy="120" rx="88" ry="72" fill="#F0A45C"/>
  <path d="M893 52 q12 16 24 0 q-3 20 -12 26 q-9 -6 -12 -26z" fill="#D9853E"/>
  <ellipse cx="905" cy="148" rx="46" ry="32" fill="#FFF3E6"/>
  <g class="eyes" fill="none" stroke="#2E2A28" stroke-width="6" stroke-linecap="round">
    <path d="M862 118 q12 -12 24 0"/><path d="M924 118 q12 -12 24 0"/>
  </g>
  <path d="M899 138 h12 l-6 7z" fill="#E0707A"/>
  <path d="M905 145 q-6 11 -15 6 M905 145 q6 11 15 6" fill="none" stroke="#2E2A28" stroke-width="4" stroke-linecap="round"/>
  <ellipse cx="850" cy="140" rx="12" ry="7" fill="#F28B7A" opacity=".55"/>
  <ellipse cx="960" cy="140" rx="12" ry="7" fill="#F28B7A" opacity=".55"/>
  <ellipse cx="872" cy="192" rx="20" ry="12" fill="#FFF3E6"/><ellipse cx="938" cy="192" rx="20" ry="12" fill="#FFF3E6"/>
</g>''')
    # text
    p.append(f'''<text x="70" y="165" font-family="{SANS}" font-size="58" font-weight="800" fill="{c['title']}">Hi, I'm SungJun</text>
<text x="72" y="215" font-family="{SANS}" font-size="28" font-weight="700" fill="{c['sub']}">Embedded AI Engineer</text>
<text x="72" y="262" font-family="{MONO}" font-size="18" fill="{c['muted']}">C / C++ · on-device inference · NPU</text>
<text x="72" y="290" font-family="{MONO}" font-size="18" fill="{c['muted']}">making models run on tiny hardware</text>
</g>
</svg>''')
    return "\n".join(p)

# ---------------------------------------------------------------- boot log
LINES = [  # (kind, segments) ; segment = (color_key, text)
    ("log", [("dim", "[    0.000000] "), ("text", "Booting Linux on ARM Cortex-A ...")]),
    ("log", [("dim", "[    0.412331] "), ("text", "npu: driver loaded, 3 cores online")]),
    ("log", [("ok", "[  OK  ] "), ("text", "Loaded model      "), ("info", "detector.onnx"), ("dim", "  fp32 · 24.1 MB")]),
    ("log", [("ok", "[  OK  ] "), ("text", "Quantized         "), ("info", "INT8"), ("dim", "           6.2 MB · -74%")]),
    ("log", [("ok", "[  OK  ] "), ("text", "Compiled graph    "), ("info", "142 ops fused"), ("dim", "  → NPU")]),
    ("log", [("info", "[ INFO ] "), ("text", "inference: "), ("ok", "3.2 ms/frame"), ("text", " @ "), ("ok", "312 FPS")]),
    ("gap", []),
    ("cmd", [("prompt", "$ "), ("text", "whoami")]),
    ("log", [("text", "SungJun · Embedded AI Engineer, porting AI models to edge devices")]),
    ("cmd", [("prompt", "$ "), ("text", "cat stack.txt")]),
    ("log", [("text", "C/C++ · ONNX Runtime · TFLite · TensorRT · Jetson · NPU SDKs")]),
    ("cmd", [("prompt", "$ "), ("text", "cat side_projects.txt")]),
    ("log", [("text", "tooling for AI coding agents · Claude Code · Codex")]),
    ("cursor", [("prompt", "$ ")]),
]

def boot(t):
    c = THEMES[t]
    W, top, lh, left, fs = 900, 62, 26, 28, 15
    H = top + lh * len(LINES) + 24
    cycle = 18.0
    p = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  text {{ font-family:{MONO}; font-size:{fs}px; white-space:pre; }}
  .cur {{ animation: cur 1s steps(1) infinite; }}
  @keyframes cur {{ 50% {{ opacity:0; }} }}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{c['term_bg']}" stroke="{c['term_border']}" stroke-width="2"/>
<path d="M1 15 a14 14 0 0 1 14 -14 H{W - 15} a14 14 0 0 1 14 14 V38 H1z" fill="{c['term_bar']}"/>
<circle cx="26" cy="20" r="6.5" fill="#FF5F57"/><circle cx="48" cy="20" r="6.5" fill="#FEBC2E"/><circle cx="70" cy="20" r="6.5" fill="#28C840"/>
<text x="{W / 2}" y="25" text-anchor="middle" fill="{c['dim']}" style="font-size:13px">sungjun@edge-board: ~</text>''']
    styles, t0 = [], 0.4
    for i, (kind, segs) in enumerate(LINES):
        y = top + i * lh
        if kind == "gap":
            t0 += 0.5
            continue
        start = t0
        chars = sum(len(s) for _, s in segs)
        typing = 0.07 * (chars - 2) if kind == "cmd" else 0
        a, b = start / cycle * 100, (start + 0.01) / cycle * 100
        styles.append(f"@keyframes l{i} {{ 0%,{a:.2f}% {{ opacity:0; }} {b:.2f}%,94% {{ opacity:1; }} 98%,100% {{ opacity:0; }} }}"
                      f" .l{i} {{ animation: l{i} {cycle}s linear infinite; }}")
        tsp = "".join(f'<tspan fill="{c[k]}">{escape(s)}</tspan>' for k, s in segs)
        p.append(f'<g class="l{i}"><text x="{left}" y="{y}">{tsp}</text>')
        if kind == "cmd":
            # a mask that slides right one character at a time → typing effect
            cw = fs * 0.602
            n = chars - 2
            x0 = left + 2 * cw
            ta, tb = (start / cycle * 100), ((start + typing) / cycle * 100)
            styles.append(f"@keyframes m{i} {{ 0%,{ta:.2f}% {{ transform:translateX(0); }} {tb:.2f}%,100% {{ transform:translateX({n * cw + 4:.1f}px); }} }}"
                          f" .m{i} {{ animation: m{i} {cycle}s steps(1) infinite; }}")
            # steps(1) per keyframe gives a jump; emulate per-char steps with many keyframes
            frames = []
            for k in range(n + 1):
                pct = (start + typing * k / max(n, 1)) / cycle * 100
                frames.append(f"{pct:.2f}% {{ transform:translateX({k * cw:.1f}px); }}")
            styles[-1] = (f"@keyframes m{i} {{ 0% {{ transform:translateX(0); }} {' '.join(frames)} 100% {{ transform:translateX({n * cw + 4:.1f}px); }} }}"
                          f" .m{i} {{ animation: m{i} {cycle}s steps(1,end) infinite; }}")
            p.append(f'<rect class="m{i}" x="{x0:.1f}" y="{y - fs}" width="{n * cw + 12:.1f}" height="{lh}" fill="{c["term_bg"]}"/>')
        if kind == "cursor":
            p.append(f'<rect class="cur" x="{left + 2 * fs * 0.602:.1f}" y="{y - fs + 2}" width="9" height="{fs + 2}" fill="{c["prompt"]}"/>')
        p.append('</g>')
        t0 = start + typing + (0.35 if kind == "cmd" else 0.55)
    p.insert(1, "<style>" + "\n".join(styles) + "</style>")
    p.append("</svg>")
    return "\n".join(p)

if __name__ == "__main__":
    for t in THEMES:
        open(os.path.join(HERE, f"banner-{t}.svg"), "w").write(banner(t))
        open(os.path.join(HERE, f"boot-{t}.svg"), "w").write(boot(t))
