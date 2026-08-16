"""Generate images/one-system-{dark,light}.svg — the profile's only graphic.

The SVGs are GENERATED OUTPUT; hand-edits get overwritten. Change this script and
rebuild both variants in the same commit:

    uv run python scripts/build_map.py

Fonts: Geist + Geist Mono (latin woff2, Google Fonts, OFL) are downloaded at build
time and embedded as base64 ``@font-face`` data URIs. GitHub serves README images
through a proxy that blocks *external* fetches, but inline data URIs render fine.

Motion: CSS ``@keyframes`` only — that is what runs when GitHub embeds the SVG as
``<img>`` on the profile. SMIL is a no-op in that path. Fully off under
``prefers-reduced-motion: reduce``. Never put raw angle-bracket tags inside the
SVG style comment (XML parse error).

Palette is GitHub Primer (dark canvas ``#0d1117``, light canvas ``#ffffff``,
accent blue) so the graphic sits on the profile page.

The map is a left-to-right sentence: classifier → faithfulness-judge → sanlee.me.
telltale and agent-ops are sibling repos, each in its own box: telltale observes
from above; agent-ops is the operating layer under the flow. Not six equal nodes,
and not the career-arc signature — that claim already lives in the GitHub bio.
"""
from __future__ import annotations

import base64
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "images"
# Filename stem is versioned so GitHub's camo cache cannot serve a stale SVG
# after a redesign (relative-path camo URLs key on the path).
STEM = "one-system-v9"
FONTS = {
    "GEIST": "https://fonts.gstatic.com/s/geist/v5/gyByhwUxId8gMEwcGFU.woff2",
    "MONO": "https://fonts.gstatic.com/s/geistmono/v6/or3yQ6H-1_WfwkMZI_qYPLs1a-t7PU0AbeE9KK5U5Ck.woff2",
}

W, H = 1280, 920


def fetch_b64(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 - fixed https URLs
        data = r.read()
    print(f"{url.rsplit('/', 1)[-1]}: {len(data)} bytes")
    return base64.b64encode(data).decode()


b64 = {k: fetch_b64(u) for k, u in FONTS.items()}

LIGHT = dict(
    bg="#ffffff",
    elevated="#f6f8fa",
    inset="#ffffff",
    border="#8c959f",
    hairline="#d0d7de",
    ink="#1f2328",
    argument="#424a53",
    meta="#59636e",
    accent="#0969da",
    accent_soft="#218bff",
    packet="#0969da",
    packet_soft="#54aeff",
    button_fill="#f6f8fa",
    button_stroke="#d0d7de",
    button_text="#0969da",
    glow_op="0.08",
    scan_op="0.06",
)
DARK = dict(
    bg="#0d1117",
    elevated="#151b23",
    inset="#0d1117",
    border="#3d444d",
    hairline="#21262d",
    ink="#f0f6fc",
    argument="#c8d1da",
    meta="#9198a1",
    accent="#4493f8",
    accent_soft="#79c0ff",
    packet="#79c0ff",
    packet_soft="#388bfd",
    button_fill="#21262d",
    button_stroke="#3d444d",
    button_text="#4493f8",
    glow_op="0.16",
    scan_op="0.07",
)


def css_motion() -> str:
    return """
      .flow {
        stroke-dasharray: 14 64;
        stroke-dashoffset: 0;
        opacity: 0.95;
        animation: flow 1.8s linear infinite;
      }
      .carrier {
        stroke-dasharray: 5 46;
        stroke-dashoffset: 0;
        opacity: 0.45;
        animation: flow 3.2s linear infinite reverse;
      }
      .ribbon {
        stroke-dasharray: 8 18;
        stroke-dashoffset: 0;
        animation: flow 7s linear infinite;
      }
      .glow-breathe {
        animation: glowbreathe 5s ease-in-out infinite;
      }
      .scan {
        animation: scan 12s linear infinite;
      }
      .pip { opacity: 0.4; animation: pip 3.6s ease-in-out infinite; }
      .pip1 { animation-delay: 1.2s; }
      .pip2 { animation-delay: 2.4s; }
      @keyframes flow { to { stroke-dashoffset: -78; } }
      @keyframes glowbreathe {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.55; }
      }
      @keyframes scan {
        from { transform: translate(0px, -120px); }
        to { transform: translate(0px, 980px); }
      }
      @keyframes pip {
        0%, 100% { opacity: 0.35; }
        14% { opacity: 1; }
        32% { opacity: 0.4; }
      }
      @media (prefers-reduced-motion: reduce) {
        .flow, .carrier, .ribbon, .glow-breathe, .scan, .pip {
          animation: none !important;
        }
        .flow, .carrier, .scan { opacity: 0; }
        .pip { opacity: 0.85; }
        .ribbon, .glow-breathe { opacity: 1; }
      }
"""


def connector(p: dict, x1: int, x2: int, y: int, delay: str) -> str:
    return f'''  <path d="M {x1} {y} H {x2}" fill="none" stroke="{p["hairline"]}" stroke-width="1.2"/>
  <path class="carrier" d="M {x1} {y} H {x2}" fill="none" stroke="{p["packet_soft"]}" stroke-width="1.6" stroke-linecap="round" style="animation-delay:{delay}"/>
  <path class="flow" d="M {x1} {y} H {x2}" fill="none" stroke="{p["packet"]}" stroke-width="2.2" stroke-linecap="round" style="animation-delay:{delay}"/>
  <polygon points="{x2},{y - 6} {x2 + 14},{y} {x2},{y + 6}" fill="{p["accent"]}"/>'''


def drop(p: dict, x: int, y1: int, y2: int, kind: str, delay: str) -> str:
    cls = "ribbon" if kind == "observe" else "flow"
    stroke = p["accent"] if kind == "observe" else p["packet"]
    return f'''  <path class="{cls}" d="M {x} {y1} V {y2}" fill="none" stroke="{stroke}" stroke-width="1.5" stroke-linecap="round" style="animation-delay:{delay}"/>'''


def cell(p: dict, x: int, y: int, w: int, h: int, title: str, sub: str) -> str:
    return f'''  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{p["inset"]}" stroke="{p["hairline"]}" stroke-width="1"/>
  <text x="{x + 16}" y="{y + 28}" font-family="'Geist Mono',Consolas,monospace" font-size="13" fill="{p["ink"]}">{title}</text>
  <text x="{x + 16}" y="{y + 50}" font-family="'Geist','Segoe UI',sans-serif" font-size="13" fill="{p["argument"]}">{sub}</text>'''


def repo_tab(p: dict, x: int, y: int) -> str:
    return f'''  <path d="M {x} {y + 18} V {y + 8} Q {x} {y} {x + 8} {y} H {x + 108} Q {x + 116} {y} {x + 116} {y + 8} V {y + 18} Z" fill="{p["elevated"]}" stroke="{p["accent"]}" stroke-width="1.4"/>
  <circle class="pip" cx="{x + 20}" cy="{y + 9}" r="3.4" fill="{p["accent"]}"/>
  <text x="{x + 32}" y="{y + 13}" font-family="'Geist Mono',Consolas,monospace" font-size="11" letter-spacing="1.6" fill="{p["accent"]}">REPO</text>'''


def svg(p: dict) -> str:
    # Shared horizontal inset.
    x0 = 56
    inner = 1168

    # Telltale repo box
    tt_y = 124
    tt_h = 176
    # Flow band
    fl_y = 368
    fl_h = 168
    # agent-ops repo box
    ao_y = 612
    ao_h = 236

    c1_x, c1_w = 56, 348
    c2_x, c2_w = 468, 372
    site_x, site_w = 904, 320
    mid_y = fl_y + fl_h // 2

    tt_cells = [
        (76, "council", "dispatch room"),
        (456, "hud", "cross-vendor gauges"),
        (836, "statusline", "measured numbers only"),
    ]
    ao_cells = [
        (76, "guards", "fence at tool time"),
        (364, "incidents", "blameless postmortems"),
        (652, "conventions", "working agreements"),
        (940, "decisions", "ADRs · fleet routing"),
    ]

    tt_cell_svg = "\n".join(cell(p, cx, tt_y + 96, 368, 64, title, sub) for cx, title, sub in tt_cells)
    ao_cell_svg = "\n".join(cell(p, cx, ao_y + 148, 264, 64, title, sub) for cx, title, sub in ao_cells)

    return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="mapTitle mapDesc">
  <title id="mapTitle">See it as one system — sanlee.me</title>
  <desc id="mapDesc">Two sibling repos around a product flow. telltale observes from its own box. classifier flows through faithfulness-judge to sanlee.me. agent-ops is the operating-layer box under the flow.</desc>
  <defs>
    <style>
      @font-face {{ font-family: 'Geist'; font-style: normal; font-weight: 100 900; src: url(data:font/woff2;base64,{b64["GEIST"]}) format('woff2'); }}
      @font-face {{ font-family: 'Geist Mono'; font-style: normal; font-weight: 400; src: url(data:font/woff2;base64,{b64["MONO"]}) format('woff2'); }}
      /* CSS motion for GitHub profile img embed. No angle-bracket tags here. */
      {css_motion()}
    </style>
    <radialGradient id="glow" cx="50%" cy="52%" r="46%">
      <stop offset="0%" stop-color="{p["accent"]}" stop-opacity="{p["glow_op"]}"/>
      <stop offset="100%" stop-color="{p["accent"]}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{p["accent"]}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{p["accent"]}" stop-opacity="{p["scan_op"]}"/>
      <stop offset="100%" stop-color="{p["accent"]}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="{W}" height="{H}" fill="{p["bg"]}"/>
  <ellipse class="glow-breathe" cx="640" cy="470" rx="460" ry="260" fill="url(#glow)"/>
  <g class="scan">
    <rect x="0" y="0" width="{W}" height="110" fill="url(#scanGrad)"/>
  </g>
  <text x="56" y="58" font-family="'Geist','Segoe UI',sans-serif" font-size="42" font-weight="600" letter-spacing="-1.3"><tspan fill="{p["ink"]}">See it as </tspan><tspan fill="{p["accent"]}">one system</tspan></text>
  <text x="58" y="90" font-family="'Geist','Segoe UI',sans-serif" font-size="15" font-weight="400" fill="{p["argument"]}">two repos around the work, and the site they ship to</text>

{repo_tab(p, 72, tt_y)}
  <rect x="{x0}" y="{tt_y + 16}" width="{inner}" height="{tt_h}" rx="10" fill="{p["elevated"]}" stroke="{p["accent"]}" stroke-width="1.4"/>
  <text x="80" y="{tt_y + 54}" font-family="'Geist','Segoe UI',sans-serif" font-size="26" font-weight="600" fill="{p["ink"]}">telltale</text>
  <text x="214" y="{tt_y + 54}" font-family="'Geist Mono',Consolas,monospace" font-size="13" fill="{p["meta"]}">sanlee-ys/telltale</text>
  <text x="80" y="{tt_y + 80}" font-family="'Geist','Segoe UI',sans-serif" font-size="14" fill="{p["accent"]}">observes only · never routes</text>
{tt_cell_svg}
{drop(p, 260, tt_y + 16 + tt_h, fl_y, "observe", "0s")}
{drop(p, 654, tt_y + 16 + tt_h, fl_y, "observe", "-2.2s")}
{drop(p, 1064, tt_y + 16 + tt_h, fl_y, "observe", "-4.4s")}

  <rect x="{c1_x}" y="{fl_y}" width="{c1_w}" height="{fl_h}" rx="10" fill="{p["elevated"]}" stroke="{p["border"]}" stroke-width="1"/>
  <text x="{c1_x + 24}" y="{fl_y + 52}" font-family="'Geist','Segoe UI',sans-serif" font-size="26" font-weight="600" fill="{p["ink"]}">classifier</text>
  <text x="{c1_x + 24}" y="{fl_y + 86}" font-family="'Geist','Segoe UI',sans-serif" font-size="15" fill="{p["argument"]}">the product that has to be right</text>
  <text x="{c1_x + 24}" y="{fl_y + 112}" font-family="'Geist Mono',Consolas,monospace" font-size="12" fill="{p["meta"]}">sanlee-ys/classifier</text>
{connector(p, c1_x + c1_w, c2_x - 14, mid_y, "0s")}
  <rect x="{c2_x}" y="{fl_y}" width="{c2_w}" height="{fl_h}" rx="10" fill="{p["elevated"]}" stroke="{p["border"]}" stroke-width="1"/>
  <text x="{c2_x + 24}" y="{fl_y + 52}" font-family="'Geist','Segoe UI',sans-serif" font-size="24" font-weight="600" fill="{p["ink"]}">faithfulness-judge</text>
  <text x="{c2_x + 24}" y="{fl_y + 86}" font-family="'Geist','Segoe UI',sans-serif" font-size="15" fill="{p["argument"]}">checks the claims before they land</text>
  <text x="{c2_x + 24}" y="{fl_y + 112}" font-family="'Geist Mono',Consolas,monospace" font-size="12" fill="{p["meta"]}">sanlee-ys/faithfulness-judge</text>
{connector(p, c2_x + c2_w, site_x - 14, mid_y, "-0.8s")}
  <rect x="{site_x}" y="{fl_y + 24}" width="{site_w}" height="{fl_h - 48}" rx="10" fill="{p["button_fill"]}" stroke="{p["button_stroke"]}" stroke-width="1"/>
  <text x="{site_x + site_w // 2}" y="{fl_y + 86}" font-family="'Geist','Segoe UI',sans-serif" font-size="24" font-weight="600" text-anchor="middle" fill="{p["button_text"]}">sanlee.me</text>
  <text x="{site_x + site_w // 2}" y="{fl_y + 114}" font-family="'Geist','Segoe UI',sans-serif" font-size="13" text-anchor="middle" fill="{p["meta"]}">the public face</text>

{drop(p, 260, fl_y + fl_h, ao_y + 16, "wire", "0s")}
{drop(p, 654, fl_y + fl_h, ao_y + 16, "wire", "-0.9s")}
{repo_tab(p, 72, ao_y)}
  <rect x="{x0}" y="{ao_y + 16}" width="{inner}" height="{ao_h}" rx="10" fill="{p["elevated"]}" stroke="{p["accent"]}" stroke-width="1.4"/>
  <text x="80" y="{ao_y + 54}" font-family="'Geist','Segoe UI',sans-serif" font-size="26" font-weight="600" fill="{p["ink"]}">agent-ops</text>
  <text x="232" y="{ao_y + 54}" font-family="'Geist Mono',Consolas,monospace" font-size="13" fill="{p["meta"]}">sanlee-ys/agent-ops</text>
  <text x="80" y="{ao_y + 80}" font-family="'Geist','Segoe UI',sans-serif" font-size="14" fill="{p["accent"]}">operating layer · wires the fence</text>
  <text x="80" y="{ao_y + 122}" font-family="'Geist','Segoe UI',sans-serif" font-size="14" fill="{p["argument"]}">the contracts, the guards, and the postmortems under the work</text>
{ao_cell_svg}
</svg>
'''


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dark = OUT / f"{STEM}-dark.svg"
    light = OUT / f"{STEM}-light.svg"
    dark.write_text(svg(DARK), encoding="utf-8")
    light.write_text(svg(LIGHT), encoding="utf-8")
    print("dark:", dark.stat().st_size, "bytes →", dark.name)
    print("light:", light.stat().st_size, "bytes →", light.name)
    print("system: classifier, telltale, faithfulness-judge, agent-ops")


if __name__ == "__main__":
    main()
