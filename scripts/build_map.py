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
accent blue) so the graphic sits on the profile page instead of reading as a
warm plate on top of it.

The chip set is the **portfolio system** (six public parts that converge on
sanlee.me) — NOT the GitHub profile pins. Repo names are labels, not claims.
"""
from __future__ import annotations

import base64
import math
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "images"
# Filename stem is versioned so GitHub's camo cache cannot serve a stale SVG
# after a redesign (relative-path camo URLs key on the path).
STEM = "one-system-v7"
FONTS = {
    "GEIST": "https://fonts.gstatic.com/s/geist/v5/gyByhwUxId8gMEwcGFU.woff2",
    "MONO": "https://fonts.gstatic.com/s/geistmono/v6/or3yQ6H-1_WfwkMZI_qYPLs1a-t7PU0AbeE9KK5U5Ck.woff2",
}

# Flattened hex (no north/south vertices) so the heading and CTA keep the
# vertical band. Angle 0 = east, counter-clockwise, y-up.
# Each: (label, angle_deg)
SYSTEM_REPOS = [
    ("defense-news-classifier", 155),
    ("faithfulness-judge", 25),
    ("agent-ops", 180),
    ("architecture", 0),
    ("kb-agent", 205),
    ("learning-notes", 335),
]

W, H = 1280, 680
CX, CY = 640, 392
NODE_R = 248
RING_R = 54
CTA_Y = 604


def fetch_b64(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 - fixed https URLs
        data = r.read()
    print(f"{url.rsplit('/', 1)[-1]}: {len(data)} bytes")
    return base64.b64encode(data).decode()


b64 = {k: fetch_b64(u) for k, u in FONTS.items()}

# GitHub Primer tokens — dark matches the profile canvas, light matches
# prefers-color-scheme: light. Accent is Primer accent-fg, not portfolio oxide.
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
    node_fill="#ffffff",
    core="#1f2328",
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
    node_fill="#0d1117",
    core="#f0f6fc",
    button_fill="#21262d",
    button_stroke="#3d444d",
    button_text="#4493f8",
    glow_op="0.16",
    scan_op="0.07",
)


def polar(angle_deg: float, radius: float) -> tuple[float, float]:
    a = math.radians(angle_deg)
    return CX + radius * math.cos(a), CY - radius * math.sin(a)


def nodes() -> list[tuple[str, float, float, float]]:
    """Return (label, angle, x, y) for each system repo."""
    return [(label, ang, *polar(ang, NODE_R)) for label, ang in SYSTEM_REPOS]


def hex_d(cx: float, cy: float, r: float, rot: float = 0.0) -> str:
    pts = []
    for i in range(6):
        a = math.radians(60 * i - 30 + rot)
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return "M " + " L ".join(pts) + " Z"


def constellation_d(pts: list[tuple[float, float]]) -> str:
    ordered = sorted(pts, key=lambda p: math.atan2(CY - p[1], p[0] - CX))
    body = " L ".join(f"{x:.1f},{y:.1f}" for x, y in ordered)
    return f"M {body} Z"


def spoke_d(nx: float, ny: float) -> str:
    dx, dy = nx - CX, ny - CY
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    sx, sy = nx - ux * 14, ny - uy * 14
    ex, ey = CX + ux * RING_R, CY + uy * RING_R
    return f"M {sx:.1f} {sy:.1f} L {ex:.1f} {ey:.1f}"


def nodes_svg(p: dict, repo_nodes: list) -> str:
    parts = []
    for i, (label, _ang, x, y) in enumerate(repo_nodes):
        left = x < CX
        anchor = "end" if left else "start"
        tx = x - 16 if left else x + 16
        parts.append(
            f'<circle class="pip pip{i}" cx="{x:.1f}" cy="{y:.1f}" '
            f'r="5.2" fill="{p["accent"]}"/>'
        )
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9.5" fill="none" '
            f'stroke="{p["border"]}" stroke-width="1.2"/>'
        )
        parts.append(
            f'<text x="{tx:.1f}" y="{y + 4.5:.1f}" '
            f'font-family="\'Geist Mono\',Consolas,monospace" font-size="13" '
            f'letter-spacing="0.4" text-anchor="{anchor}" '
            f'fill="{p["ink"]}">{label}</text>'
        )
    return "\n  ".join(parts)


def spokes_svg(p: dict, repo_nodes: list) -> str:
    delays = ["0s", "-0.45s", "-0.9s", "-1.35s", "-1.8s", "-2.25s"]
    base = []
    carriers = []
    streaks = []
    for i, (_label, _ang, x, y) in enumerate(repo_nodes):
        d = spoke_d(x, y)
        delay = delays[i]
        base.append(
            f'<path d="{d}" fill="none" stroke="{p["hairline"]}" stroke-width="1.15"/>'
        )
        carriers.append(
            f'<path class="carrier" d="{d}" fill="none" stroke="{p["packet_soft"]}" '
            f'stroke-width="1.6" stroke-linecap="round" style="animation-delay:{delay}"/>'
        )
        streaks.append(
            f'<path class="flow" d="{d}" fill="none" stroke="{p["packet"]}" '
            f'stroke-width="2.2" stroke-linecap="round" style="animation-delay:{delay}"/>'
        )
    return "\n  ".join(base + carriers + streaks)


def hub_svg(p: dict) -> str:
    return f'''<!-- hub -->
  <path class="orbit" d="{hex_d(CX, CY, RING_R + 10)}" fill="none" stroke="{p["border"]}" stroke-width="1.1"/>
  <circle cx="{CX}" cy="{CY}" r="{RING_R}" fill="none" stroke="{p["hairline"]}" stroke-width="1"/>
  <circle class="pulse" cx="{CX}" cy="{CY}" r="26" fill="none" stroke="{p["accent"]}" stroke-width="1.4"/>
  <circle class="pulse2" cx="{CX}" cy="{CY}" r="16" fill="none" stroke="{p["accent_soft"]}" stroke-width="1.2"/>
  <path d="{hex_d(CX, CY, 9)}" fill="none" stroke="{p["accent"]}" stroke-width="1.8"/>
  <circle class="core-breathe" cx="{CX}" cy="{CY}" r="3.2" fill="{p["core"]}"/>'''


def career_arc_svg(p: dict) -> str:
    return f'''<!-- career arc -->
  <path d="M 928 128 H 1006 L 1030 110 H 1108 L 1132 92 H 1194" fill="none" stroke="{p["hairline"]}" stroke-width="1.4"/>
  <rect x="922" y="122" width="12" height="12" rx="1.5" fill="none" stroke="{p["accent"]}" stroke-width="1.5"/>
  <circle cx="1069" cy="110" r="5" fill="none" stroke="{p["accent"]}" stroke-width="1.5"/>
  <rect x="1194" y="86" width="12" height="12" rx="1.5" transform="rotate(45 1200 92)" fill="{p["accent"]}"/>
  <g font-family="'Geist Mono',Consolas,monospace" font-size="10" letter-spacing="2" fill="{p["meta"]}">
    <text x="928" y="152" text-anchor="middle">NET&#160;OPS</text>
    <text x="1069" y="134" text-anchor="middle">SOFTWARE</text>
    <text x="1200" y="116" text-anchor="middle">PRODUCT</text>
  </g>'''


def css_motion() -> str:
    return """
      .flow {
        stroke-dasharray: 14 70;
        stroke-dashoffset: 0;
        opacity: 0.95;
        animation: flow 1.8s linear infinite;
      }
      .carrier {
        stroke-dasharray: 5 50;
        stroke-dashoffset: 0;
        opacity: 0.45;
        animation: flow 3.2s linear infinite reverse;
      }
      .flowv {
        stroke-dasharray: 12 42;
        stroke-dashoffset: 0;
        opacity: 0.95;
        animation: flowv 1.6s linear infinite;
      }
      .orbit {
        stroke-dasharray: 5 13;
        stroke-dashoffset: 0;
        animation: orbit 16s linear infinite;
      }
      .constellation {
        stroke-dasharray: 3 11;
        stroke-dashoffset: 0;
        opacity: 0.7;
        animation: orbit 28s linear infinite reverse;
      }
      .pulse {
        opacity: 0.7;
        animation: pulse 2.4s cubic-bezier(0.22, 0.61, 0.36, 1) infinite;
      }
      .pulse2 {
        opacity: 0.5;
        animation: pulse 2.4s cubic-bezier(0.22, 0.61, 0.36, 1) infinite;
        animation-delay: 0.6s;
      }
      .core-breathe {
        animation: breathe 2.8s ease-in-out infinite;
      }
      .glow-breathe {
        animation: glowbreathe 5s ease-in-out infinite;
      }
      .scan {
        animation: scan 11s linear infinite;
      }
      .pip { opacity: 0.4; animation: pip 3.6s ease-in-out infinite; }
      .pip0 { animation-delay: 0s; }
      .pip1 { animation-delay: 0.6s; }
      .pip2 { animation-delay: 1.2s; }
      .pip3 { animation-delay: 1.8s; }
      .pip4 { animation-delay: 2.4s; }
      .pip5 { animation-delay: 3.0s; }
      @keyframes flow { to { stroke-dashoffset: -84; } }
      @keyframes flowv { to { stroke-dashoffset: -54; } }
      @keyframes orbit { to { stroke-dashoffset: -108; } }
      @keyframes pulse {
        0% { opacity: 0.7; }
        55% { opacity: 0; }
        100% { opacity: 0; }
      }
      @keyframes breathe {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
      }
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
        .flow, .carrier, .flowv, .orbit, .constellation, .pulse, .pulse2,
        .core-breathe, .glow-breathe, .scan, .pip { animation: none !important; }
        .flow, .carrier, .flowv, .pulse, .pulse2, .scan { opacity: 0; }
        .pip { opacity: 0.85; }
        .core-breathe, .glow-breathe, .constellation { opacity: 1; }
      }
"""


def svg(p: dict) -> str:
    repo_nodes = nodes()
    labels = ", ".join(lab for lab, *_ in repo_nodes)
    hex_pts = [(x, y) for _lab, _ang, x, y in repo_nodes]
    stem_top = CY + RING_R + 12
    stem_bot = CTA_Y - 22

    return f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="mapTitle mapDesc">
  <title id="mapTitle">See it as one system — sanlee.me</title>
  <desc id="mapDesc">Six repository nodes — {labels} — sit on a hex constellation and send traces into a central core that points down to a sanlee.me button under the heading "See it as one system." A small circuit trace rises through net ops, software, and product in the top right corner.</desc>
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
  <ellipse class="glow-breathe" cx="{CX}" cy="{CY}" rx="380" ry="200" fill="url(#glow)"/>
  <g class="scan">
    <rect x="0" y="0" width="{W}" height="110" fill="url(#scanGrad)"/>
  </g>
  <path class="constellation" d="{constellation_d(hex_pts)}" fill="none" stroke="{p["border"]}" stroke-width="1"/>
  {career_arc_svg(p)}
  <text x="72" y="86" font-family="'Geist','Segoe UI',sans-serif" font-size="46" font-weight="600" letter-spacing="-1.4"><tspan fill="{p["ink"]}">See it as </tspan><tspan fill="{p["accent"]}">one system</tspan></text>
  <text x="74" y="120" font-family="'Geist','Segoe UI',sans-serif" font-size="15" font-weight="400" fill="{p["argument"]}">six public parts converge — decisions recorded, reversals included</text>
  {spokes_svg(p, repo_nodes)}
  {nodes_svg(p, repo_nodes)}
  {hub_svg(p)}
  <path d="M {CX} {stem_top} V {stem_bot}" fill="none" stroke="{p["accent"]}" stroke-width="1.6"/>
  <path class="flowv" d="M {CX} {stem_top} V {stem_bot}" fill="none" stroke="{p["packet"]}" stroke-width="2" stroke-linecap="round"/>
  <polygon points="{CX - 5},{stem_bot} {CX + 5},{stem_bot} {CX},{stem_bot + 9}" fill="{p["accent"]}"/>
  <rect x="540" y="{CTA_Y}" width="200" height="44" rx="6" fill="{p["button_fill"]}" stroke="{p["button_stroke"]}" stroke-width="1"/>
  <text x="{CX - 8}" y="{CTA_Y + 28}" font-family="'Geist','Segoe UI',sans-serif" font-size="16" font-weight="600" text-anchor="middle" fill="{p["button_text"]}">sanlee.me</text>
  <g stroke="{p["button_text"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M {CX + 46} {CTA_Y + 22} H {CX + 62} M {CX + 56} {CTA_Y + 16} L {CX + 62} {CTA_Y + 22} L {CX + 56} {CTA_Y + 28}"/>
  </g>
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
    print("system:", ", ".join(lab for lab, _ in SYSTEM_REPOS))


if __name__ == "__main__":
    main()
