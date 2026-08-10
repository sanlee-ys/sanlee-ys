"""Generate images/one-system-{dark,light}.svg — the profile's only graphic.

The SVGs are GENERATED OUTPUT; hand-edits get overwritten. Change this script and
rebuild both variants in the same commit:

    uv run python scripts/build_map.py

Fonts: Geist + Geist Mono (latin woff2, Google Fonts, OFL) are downloaded at build
time and embedded as base64 ``@font-face`` data URIs. GitHub serves README images
through a proxy that blocks *external* fetches, but inline data URIs render fine —
that is the whole trick that makes a real webfont work here.

Motion: CSS ``@keyframes`` only — that is what runs when GitHub embeds the SVG as
``<img>`` on the profile. SMIL is a no-op in that path. Fully off under
``prefers-reduced-motion: reduce``. Never put raw angle-bracket tags inside the
SVG style comment (XML parse error).

Palette follows the portfolio site (paper ground, ink, oxide) rather than the
old Vercel blue/purple — so the profile graphic and sanlee.me share one face.

The chip set is the **portfolio system** (six public parts that converge on
sanlee.me) — NOT the GitHub profile pins. Pins can change for showcase reasons;
this map tracks the system story. If the portfolio's system set changes, update
SYSTEM_REPOS below. Repo names are labels, not claims — see CLAUDE.md.
"""
from __future__ import annotations

import base64
import math
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "images"
# Filename stem is versioned so GitHub's camo cache cannot serve a stale SVG
# after a redesign (relative-path camo URLs key on the path).
STEM = "one-system-v6"
FONTS = {
    "GEIST": "https://fonts.gstatic.com/s/geist/v5/gyByhwUxId8gMEwcGFU.woff2",
    "MONO": "https://fonts.gstatic.com/s/geistmono/v6/or3yQ6H-1_WfwkMZI_qYPLs1a-t7PU0AbeE9KK5U5Ck.woff2",
}

# Portfolio system parts (the six that form "one system" on sanlee.me).
# Independent of which repos are currently *pinned* on the GitHub profile.
# Each: (label, column, row) where column in {"L","R"} and row in {0,1,2}.
SYSTEM_REPOS = [
    ("defense-news-classifier", "L", 0),
    ("faithfulness-judge", "R", 0),
    ("agent-ops", "L", 1),
    ("architecture", "R", 1),
    ("kb-agent", "L", 2),
    ("learning-notes", "R", 2),
]

# Chip geometry — three rows, two columns around a central instrument hub.
CHIP_H = 42
CHIP_RX = 4  # squared — matches portfolio --radius-sm
ROW_Y = (292, 390, 488)
LEFT_X = 72
RIGHT_EDGE = 1208
JUNCTION = (640, 390)
CTA_Y = 600
ORBIT_R = 78
COLLECTOR_INSET = 28  # horizontal run from chip edge before the curve


def fetch_b64(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 - fixed https URLs
        data = r.read()
    print(f"{url.rsplit('/', 1)[-1]}: {len(data)} bytes")
    return base64.b64encode(data).decode()


b64 = {k: fetch_b64(u) for k, u in FONTS.items()}

# Portfolio tokens (light = paper theme; dark = ink theme).
# Oxide is the accent — the same mark the portfolio uses for reversed decisions.
LIGHT = dict(
    bg="#fafaf9",
    grid="#e8e6e3",
    border="#d4d0cb",
    rule="#423f3c",
    ink="#1e1c1b",
    argument="#383533",
    meta="#5f5c58",
    oxide="#5e1f0d",
    chip_fill="#fafaf9",
    chip_stroke="#d4d0cb",
    chip_text="#1e1c1b",
    beam_far="#d4d0cb",
    beam_near="#5e1f0d",
    packet="#5e1f0d",
    packet_soft="#a86a52",
    core="#1e1c1b",
    pill_fill="#1e1c1b",
    pill_text="#fafaf9",
    glow_op="0.07",
    badge_fill="#f3f1ee",
    badge_stroke="#d4d0cb",
    orbit="#d4d0cb",
    reticle="#a39e98",
    dot="#d4d0cb",
)
DARK = dict(
    bg="#1e1c1b",
    grid="#2e2b29",
    border="#423f3c",
    rule="#a39e98",
    ink="#fafaf9",
    argument="#e8e4df",
    meta="#a39e98",
    oxide="#c45a3a",
    chip_fill="#262322",
    chip_stroke="#423f3c",
    chip_text="#f0ebe6",
    beam_far="#423f3c",
    beam_near="#c45a3a",
    packet="#e08a6a",
    packet_soft="#a35a42",
    core="#fafaf9",
    pill_fill="#fafaf9",
    pill_text="#1e1c1b",
    glow_op="0.12",
    badge_fill="#262322",
    badge_stroke="#423f3c",
    orbit="#423f3c",
    reticle="#6b6560",
    dot="#2e2b29",
)


def chip_width(label: str) -> int:
    # Mono ~9.4px per char at 14px + 32px horizontal padding.
    return max(118, int(len(label) * 9.4 + 32))


def chip_boxes() -> list[tuple[str, float, float, float, float]]:
    """Return (label, x, y, w, h) for each system repo chip."""
    boxes = []
    for label, col, row in SYSTEM_REPOS:
        w = chip_width(label)
        cy = ROW_Y[row]
        y = cy - CHIP_H / 2
        if col == "L":
            x = LEFT_X
        else:
            x = RIGHT_EDGE - w
        boxes.append((label, x, y, w, CHIP_H))
    return boxes


def spoke_path(sx: float, sy: float, jx: float, jy: float, side: str) -> str:
    """Elbowed spoke: short horizontal run, then cubic into the hub ring."""
    if side == "L":
        mx = sx + COLLECTOR_INSET
        # Aim at the left rim of the orbit so spokes don't stack into one point.
        ex = jx - ORBIT_R + 6
        d = (
            f"M {sx:.0f} {sy:.0f} "
            f"H {mx:.0f} "
            f"C {mx + 90:.0f} {sy:.0f}, {ex - 40:.0f} {jy:.0f}, {ex:.0f} {jy:.0f}"
        )
    else:
        mx = sx - COLLECTOR_INSET
        ex = jx + ORBIT_R - 6
        d = (
            f"M {sx:.0f} {sy:.0f} "
            f"H {mx:.0f} "
            f"C {mx - 90:.0f} {sy:.0f}, {ex + 40:.0f} {jy:.0f}, {ex:.0f} {jy:.0f}"
        )
    return d


def beams_for(boxes: list[tuple[str, float, float, float, float]]) -> list[tuple[str, str, str, str]]:
    """Return (d, grad, delay, side) for each chip spoke."""
    jx, jy = JUNCTION
    out = []
    delays = ["0s", "-0.4s", "-0.8s", "-1.2s", "-1.6s", "-2.0s"]
    for i, (label, x, y, w, h) in enumerate(boxes):
        cy = y + h / 2
        if x < jx:
            sx = x + w
            side = "L"
            grad = "beamL"
        else:
            sx = x
            side = "R"
            grad = "beamR"
        d = spoke_path(sx, cy, jx, jy, side)
        out.append((d, grad, delays[i % len(delays)], side))
    return out


def chips_svg(p: dict, boxes: list) -> str:
    parts = []
    for i, (label, x, y, w, h) in enumerate(boxes):
        # Plate
        parts.append(
            f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'rx="{CHIP_RX}" fill="{p["chip_fill"]}" stroke="{p["chip_stroke"]}" stroke-width="1.5"/>'
        )
        # Sequential oxide LED — reads as "alive" without being noisy
        led_x = x + 14 if x < JUNCTION[0] else x + w - 14
        parts.append(
            f'<circle class="led led{i}" cx="{led_x:.0f}" cy="{y + h / 2:.1f}" '
            f'r="3.2" fill="{p["oxide"]}"/>'
        )
        # Label offset away from the LED
        if x < JUNCTION[0]:
            tx = x + (w + 10) / 2 + 4
        else:
            tx = x + (w - 10) / 2 - 4
        parts.append(
            f'<text x="{tx:.1f}" y="{y + h / 2 + 5:.1f}" '
            f'font-family="\'Geist Mono\',Consolas,monospace" font-size="14" '
            f'text-anchor="middle" fill="{p["chip_text"]}">{label}</text>'
        )
    return "\n  ".join(parts)


def beams_svg(p: dict, beam_paths: list) -> str:
    # Dual cadence: a soft slow carrier + a bright fast packet on each spoke.
    base = [
        f'<path d="{d}" fill="none" stroke="url(#{g})" stroke-width="1.6"/>'
        for d, g, _, _ in beam_paths
    ]
    carriers = [
        f'<path class="carrier" d="{d}" fill="none" stroke="{p["packet_soft"]}" '
        f'stroke-width="1.8" stroke-linecap="round" style="animation-delay:{delay}"/>'
        for d, _, delay, _ in beam_paths
    ]
    streaks = [
        f'<path class="flow" d="{d}" fill="none" stroke="{p["packet"]}" '
        f'stroke-width="2.6" stroke-linecap="round" style="animation-delay:{delay}"/>'
        for d, _, delay, _ in beam_paths
    ]
    return "\n  ".join(base + carriers + streaks)


def hub_svg(p: dict) -> str:
    jx, jy = JUNCTION
    # Instrument reticle: outer orbit (dash-chased), mid ring, pulse ring, core.
    return f'''<!-- hub instrument -->
  <circle class="orbit" cx="{jx}" cy="{jy}" r="{ORBIT_R}" fill="none" stroke="{p["orbit"]}" stroke-width="1.2"/>
  <circle class="orbit-slow" cx="{jx}" cy="{jy}" r="{ORBIT_R - 14}" fill="none" stroke="{p["orbit"]}" stroke-width="1"/>
  <line x1="{jx - ORBIT_R - 10}" y1="{jy}" x2="{jx - ORBIT_R + 8}" y2="{jy}" stroke="{p["reticle"]}" stroke-width="1.5"/>
  <line x1="{jx + ORBIT_R - 8}" y1="{jy}" x2="{jx + ORBIT_R + 10}" y2="{jy}" stroke="{p["reticle"]}" stroke-width="1.5"/>
  <line x1="{jx}" y1="{jy - ORBIT_R - 10}" x2="{jx}" y2="{jy - ORBIT_R + 8}" stroke="{p["reticle"]}" stroke-width="1.5"/>
  <line x1="{jx}" y1="{jy + ORBIT_R - 8}" x2="{jx}" y2="{jy + ORBIT_R + 10}" stroke="{p["reticle"]}" stroke-width="1.5"/>
  <circle class="pulse" cx="{jx}" cy="{jy}" r="28" fill="none" stroke="{p["oxide"]}" stroke-width="1.8"/>
  <circle class="pulse2" cx="{jx}" cy="{jy}" r="18" fill="none" stroke="{p["oxide"]}" stroke-width="1.5"/>
  <circle cx="{jx}" cy="{jy}" r="9" fill="none" stroke="{p["oxide"]}" stroke-width="2.4"/>
  <circle class="core-breathe" cx="{jx}" cy="{jy}" r="3.8" fill="{p["core"]}"/>'''


def dots_svg(p: dict) -> str:
    """Sparse instrument-field dots instead of a hairline grid."""
    parts = []
    # Keep the header and CTA zones relatively clear.
    for y in range(250, 560, 28):
        for x in range(48, 1232, 28):
            # Hole out the hub so dots don't fight the reticle.
            if math.hypot(x - JUNCTION[0], y - JUNCTION[1]) < ORBIT_R + 36:
                continue
            # Thin the field: every other column on alternating rows.
            if ((x // 28) + (y // 28)) % 2 == 0:
                continue
            parts.append(f'<circle cx="{x}" cy="{y}" r="1.1" fill="{p["dot"]}"/>')
    return "\n  ".join(parts)


def svg(p: dict) -> str:
    boxes = chip_boxes()
    beam_paths = beams_for(boxes)
    labels = ", ".join(lab for lab, *_ in boxes)
    jx, jy = JUNCTION
    stem_top = jy + ORBIT_R + 10
    stem_bot = CTA_Y - 28

    return f'''<svg viewBox="0 0 1280 680" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="mapTitle mapDesc">
  <title id="mapTitle">See it as one system — sanlee.me</title>
  <desc id="mapDesc">Six repository chips — {labels} — feed spoke lines into a central instrument hub that points down to a sanlee.me button under the heading "See it as one system." A small circuit trace rises through net ops, software, and product in the top right corner.</desc>
  <defs>
    <style>
      @font-face {{ font-family: 'Geist'; font-style: normal; font-weight: 100 900; src: url(data:font/woff2;base64,{b64["GEIST"]}) format('woff2'); }}
      @font-face {{ font-family: 'Geist Mono'; font-style: normal; font-weight: 400; src: url(data:font/woff2;base64,{b64["MONO"]}) format('woff2'); }}
      /* CSS motion for GitHub profile img embed. No angle-bracket tags here. */
      .flow {{
        stroke-dasharray: 18 72;
        stroke-dashoffset: 0;
        opacity: 0.95;
        animation: flow 1.9s linear infinite;
      }}
      .carrier {{
        stroke-dasharray: 6 54;
        stroke-dashoffset: 0;
        opacity: 0.55;
        animation: flow 3.4s linear infinite reverse;
      }}
      .flowv {{
        stroke-dasharray: 14 48;
        stroke-dashoffset: 0;
        opacity: 0.95;
        animation: flowv 1.5s linear infinite;
      }}
      .orbit {{
        stroke-dasharray: 6 14;
        stroke-dashoffset: 0;
        animation: orbit 7s linear infinite;
      }}
      .orbit-slow {{
        stroke-dasharray: 2 18;
        stroke-dashoffset: 0;
        opacity: 0.7;
        animation: orbit 14s linear infinite reverse;
      }}
      .pulse {{
        opacity: 0.7;
        animation: pulse 2.2s cubic-bezier(0.22, 0.61, 0.36, 1) infinite;
      }}
      .pulse2 {{
        opacity: 0.55;
        animation: pulse 2.2s cubic-bezier(0.22, 0.61, 0.36, 1) infinite;
        animation-delay: 0.55s;
      }}
      .core-breathe {{
        animation: breathe 2.6s ease-in-out infinite;
      }}
      .glow-breathe {{
        animation: glowbreathe 4.5s ease-in-out infinite;
      }}
      .dotb {{
        animation: blink 2.2s ease-in-out infinite;
      }}
      .led {{ opacity: 0.35; animation: led 3.6s ease-in-out infinite; }}
      .led0 {{ animation-delay: 0s; }}
      .led1 {{ animation-delay: 0.6s; }}
      .led2 {{ animation-delay: 1.2s; }}
      .led3 {{ animation-delay: 1.8s; }}
      .led4 {{ animation-delay: 2.4s; }}
      .led5 {{ animation-delay: 3.0s; }}
      @keyframes flow {{ to {{ stroke-dashoffset: -90; }} }}
      @keyframes flowv {{ to {{ stroke-dashoffset: -62; }} }}
      @keyframes orbit {{ to {{ stroke-dashoffset: -120; }} }}
      @keyframes pulse {{
        0% {{ opacity: 0.75; }}
        55% {{ opacity: 0; }}
        100% {{ opacity: 0; }}
      }}
      @keyframes breathe {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.45; }}
      }}
      @keyframes glowbreathe {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.55; }}
      }}
      @keyframes blink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.2; }}
      }}
      @keyframes led {{
        0%, 100% {{ opacity: 0.3; }}
        12% {{ opacity: 1; }}
        28% {{ opacity: 0.35; }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        .flow, .carrier, .flowv, .orbit, .orbit-slow, .pulse, .pulse2,
        .core-breathe, .glow-breathe, .dotb, .led {{ animation: none !important; }}
        .flow, .carrier, .flowv, .pulse, .pulse2 {{ opacity: 0; }}
        .led {{ opacity: 0.7; }}
        .core-breathe, .glow-breathe {{ opacity: 1; }}
      }}
    </style>
    <radialGradient id="glow" cx="50%" cy="48%" r="52%">
      <stop offset="0%" stop-color="{p["oxide"]}" stop-opacity="{p["glow_op"]}"/>
      <stop offset="100%" stop-color="{p["oxide"]}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="tgrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{p["ink"]}"/>
      <stop offset="100%" stop-color="{p["argument"]}"/>
    </linearGradient>
    <linearGradient id="hgrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p["oxide"]}"/>
      <stop offset="100%" stop-color="{p["ink"]}"/>
    </linearGradient>
    <linearGradient id="beamL" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p["beam_far"]}"/>
      <stop offset="100%" stop-color="{p["beam_near"]}"/>
    </linearGradient>
    <linearGradient id="beamR" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0%" stop-color="{p["beam_far"]}"/>
      <stop offset="100%" stop-color="{p["beam_near"]}"/>
    </linearGradient>
    <filter id="pillshadow" x="-40%" y="-60%" width="180%" height="260%">
      <feDropShadow dx="0" dy="8" stdDeviation="14" flood-color="{p["oxide"]}" flood-opacity="0.22"/>
    </filter>
    <clipPath id="frame"><rect x="0" y="0" width="1280" height="680" rx="4"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect x="0" y="0" width="1280" height="680" fill="{p["bg"]}"/>
    {dots_svg(p)}
    <ellipse class="glow-breathe" cx="640" cy="360" rx="420" ry="220" fill="url(#glow)"/>
  </g>
  <!-- career arc: the one permitted echo of the portfolio tagline -->
  <g clip-path="url(#frame)">
    <path d="M 920 148 H 1000 L 1025 128 H 1105 L 1130 108 H 1195" fill="none" stroke="{p["border"]}" stroke-width="2"/>
    <rect x="914" y="142" width="12" height="12" rx="2" fill="none" stroke="{p["oxide"]}" stroke-width="2"/>
    <circle cx="1065" cy="128" r="5.5" fill="none" stroke="{p["oxide"]}" stroke-width="2"/>
    <rect x="1195" y="102" width="12" height="12" rx="2" transform="rotate(45 1201 108)" fill="{p["oxide"]}"/>
    <g font-family="'Geist Mono',Consolas,monospace" font-size="10" letter-spacing="2" fill="{p["meta"]}">
      <text x="920" y="172" text-anchor="middle">NET&#160;OPS</text>
      <text x="1065" y="152" text-anchor="middle">SOFTWARE</text>
      <text x="1201" y="132" text-anchor="middle">PRODUCT</text>
    </g>
  </g>
  <!-- kicker -->
  <rect x="72" y="56" width="248" height="30" rx="4" fill="{p["badge_fill"]}" stroke="{p["badge_stroke"]}" stroke-width="1.5"/>
  <circle class="dotb" cx="92" cy="71" r="3.5" fill="{p["oxide"]}"/>
  <text x="106" y="75.5" font-family="'Geist Mono',Consolas,monospace" font-size="11" letter-spacing="2.2" fill="{p["meta"]}">THE REPOS ARE THE PARTS</text>
  <!-- heading -->
  <text x="70" y="148" font-family="'Geist','Segoe UI',sans-serif" font-size="52" font-weight="700" letter-spacing="-2"><tspan fill="url(#tgrad)">See it as </tspan><tspan fill="url(#hgrad)">one system</tspan></text>
  <text x="74" y="184" font-family="'Geist','Segoe UI',sans-serif" font-size="16" font-weight="400" fill="{p["argument"]}">six public parts converge — decisions recorded, reversals included</text>
  <line x1="74" y1="204" x2="300" y2="204" stroke="{p["rule"]}" stroke-width="2"/>
  <!-- spokes + chips + hub -->
  {beams_svg(p, beam_paths)}
  {chips_svg(p, boxes)}
  {hub_svg(p)}
  <!-- stem + CTA -->
  <path d="M {jx} {stem_top} V {stem_bot}" fill="none" stroke="{p["oxide"]}" stroke-width="2.5"/>
  <path class="flowv" d="M {jx} {stem_top} V {stem_bot}" fill="none" stroke="{p["packet"]}" stroke-width="2.4" stroke-linecap="round"/>
  <polygon points="{jx - 7},{stem_bot} {jx + 7},{stem_bot} {jx},{stem_bot + 12}" fill="{p["oxide"]}"/>
  <rect x="520" y="{CTA_Y}" width="240" height="50" rx="4" fill="{p["pill_fill"]}" filter="url(#pillshadow)"/>
  <text x="618" y="{CTA_Y + 32}" font-family="'Geist','Segoe UI',sans-serif" font-size="20" font-weight="600" text-anchor="middle" fill="{p["pill_text"]}">sanlee.me</text>
  <g stroke="{p["pill_text"]}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M 684 {CTA_Y + 25} H 704 M 697 {CTA_Y + 18} L 704 {CTA_Y + 25} L 697 {CTA_Y + 32}"/>
  </g>
  <rect x="1" y="1" width="1278" height="678" rx="3" fill="none" stroke="{p["border"]}" stroke-width="1.5"/>
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
    print("system:", ", ".join(lab for lab, _, _ in SYSTEM_REPOS))


if __name__ == "__main__":
    main()
