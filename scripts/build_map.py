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
telltale observes from above. agent-ops sits as the floor. Not six equal nodes,
and not the career-arc signature — that claim already lives in the GitHub bio.
"""
from __future__ import annotations

import base64
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "images"
# Filename stem is versioned so GitHub's camo cache cannot serve a stale SVG
# after a redesign (relative-path camo URLs key on the path).
STEM = "one-system-v8"
FONTS = {
    "GEIST": "https://fonts.gstatic.com/s/geist/v5/gyByhwUxId8gMEwcGFU.woff2",
    "MONO": "https://fonts.gstatic.com/s/geistmono/v6/or3yQ6H-1_WfwkMZI_qYPLs1a-t7PU0AbeE9KK5U5Ck.woff2",
}

W, H = 1280, 680


def fetch_b64(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 - fixed https URLs
        data = r.read()
    print(f"{url.rsplit('/', 1)[-1]}: {len(data)} bytes")
    return base64.b64encode(data).decode()


b64 = {k: fetch_b64(u) for k, u in FONTS.items()}

# GitHub Primer tokens — dark matches the profile canvas, light matches
# prefers-color-scheme: light.
LIGHT = dict(
    bg="#ffffff",
    elevated="#f6f8fa",
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
        animation: scan 11s linear infinite;
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
        to { transform: translate(0px, 720px); }
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


def svg(p: dict) -> str:
    return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="mapTitle mapDesc">
  <title id="mapTitle">See it as one system — sanlee.me</title>
  <desc id="mapDesc">A left-to-right flow from classifier through faithfulness-judge to sanlee.me. A telltale ribbon observes from above. agent-ops sits as the floor under the heading "See it as one system."</desc>
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
  <ellipse class="glow-breathe" cx="640" cy="360" rx="420" ry="200" fill="url(#glow)"/>
  <g class="scan">
    <rect x="0" y="0" width="{W}" height="110" fill="url(#scanGrad)"/>
  </g>
  <text x="72" y="78" font-family="'Geist','Segoe UI',sans-serif" font-size="46" font-weight="600" letter-spacing="-1.4"><tspan fill="{p["ink"]}">See it as </tspan><tspan fill="{p["accent"]}">one system</tspan></text>
  <text x="74" y="112" font-family="'Geist','Segoe UI',sans-serif" font-size="15" font-weight="400" fill="{p["argument"]}">the public work, and the gauge that watches it</text>
  <text x="72" y="168" font-family="'Geist Mono',Consolas,monospace" font-size="11" letter-spacing="2.4" fill="{p["meta"]}">OBSERVES</text>
  <circle class="pip" cx="96" cy="200" r="4.5" fill="{p["accent"]}"/>
  <text x="116" y="206" font-family="'Geist','Segoe UI',sans-serif" font-size="22" font-weight="600" fill="{p["ink"]}">telltale</text>
  <path class="ribbon" d="M 240 200 H 1208" fill="none" stroke="{p["accent"]}" stroke-width="1.5"/>
  <rect x="72" y="292" width="320" height="132" rx="10" fill="{p["elevated"]}" stroke="{p["border"]}" stroke-width="1"/>
  <text x="96" y="340" font-family="'Geist','Segoe UI',sans-serif" font-size="28" font-weight="600" fill="{p["ink"]}">classifier</text>
  <text x="96" y="376" font-family="'Geist','Segoe UI',sans-serif" font-size="14" fill="{p["argument"]}">the product that has to be right</text>
{connector(p, 392, 496, 358, "0s")}
  <rect x="510" y="292" width="320" height="132" rx="10" fill="{p["elevated"]}" stroke="{p["border"]}" stroke-width="1"/>
  <text x="534" y="340" font-family="'Geist','Segoe UI',sans-serif" font-size="24" font-weight="600" fill="{p["ink"]}">faithfulness-judge</text>
  <text x="534" y="376" font-family="'Geist','Segoe UI',sans-serif" font-size="14" fill="{p["argument"]}">checks the claims before they land</text>
{connector(p, 830, 934, 358, "-0.8s")}
  <rect x="948" y="308" width="232" height="100" rx="10" fill="{p["button_fill"]}" stroke="{p["button_stroke"]}" stroke-width="1"/>
  <text x="1064" y="366" font-family="'Geist','Segoe UI',sans-serif" font-size="22" font-weight="600" text-anchor="middle" fill="{p["button_text"]}">sanlee.me</text>
  <circle class="pip pip2" cx="86" cy="512" r="3.8" fill="{p["accent"]}"/>
  <text x="104" y="518" font-family="'Geist Mono',Consolas,monospace" font-size="14" fill="{p["ink"]}">agent-ops</text>
  <text x="104" y="542" font-family="'Geist','Segoe UI',sans-serif" font-size="13" fill="{p["meta"]}">the operating layer under the work</text>
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
