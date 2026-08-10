"""Generate images/one-system-{dark,light}.svg — the profile's only graphic.

The SVGs are GENERATED OUTPUT; hand-edits get overwritten. Change this script and
rebuild both variants in the same commit:

    uv run python scripts/build_map.py

Fonts: Geist + Geist Mono (latin woff2, Google Fonts, OFL) are downloaded at build
time and embedded as base64 ``@font-face`` data URIs. GitHub serves README images
through a proxy that blocks *external* fetches, but inline data URIs render fine —
that is the whole trick that makes a real webfont work here.

Motion: beams carry light packets (CSS stroke-dashoffset), the junction pulses,
the kicker dot blinks. Fully off under ``prefers-reduced-motion: reduce``.

Palette follows the portfolio site (paper ground, ink, oxide) rather than the
old Vercel blue/purple — so the profile graphic and sanlee.me share one face.

If the pinned repo set changes, update PINS below in the same sitting. Repo
names are labels, not claims — see CLAUDE.md's no-performance-claims rule.
"""
from __future__ import annotations

import base64
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "images"
FONTS = {
    "GEIST": "https://fonts.gstatic.com/s/geist/v5/gyByhwUxId8gMEwcGFU.woff2",
    "MONO": "https://fonts.gstatic.com/s/geistmono/v6/or3yQ6H-1_WfwkMZI_qYPLs1a-t7PU0AbeE9KK5U5Ck.woff2",
}

# Current GitHub pins (2026-08). Order is visual, not rank.
# Each: (label, column, row) where column in {"L","R"} and row in {0,1}.
PINS = [
    ("defense-news-classifier", "L", 0),
    ("telltale", "R", 0),
    ("agent-ops", "L", 1),
    ("netops-lab", "R", 1),
]

# Chip geometry
CHIP_H = 48
CHIP_RX = 4  # squared — matches portfolio --radius-sm, not app-pill
ROW_Y = (318, 418)
LEFT_X = 96
RIGHT_EDGE = 1184  # right chips right-align to this
JUNCTION = (640, 368)
CTA_Y = 560


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
    core="#1e1c1b",
    pill_fill="#1e1c1b",
    pill_text="#fafaf9",
    glow_op="0.06",
    badge_fill="#f3f1ee",
    badge_stroke="#d4d0cb",
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
    core="#fafaf9",
    pill_fill="#fafaf9",
    pill_text="#1e1c1b",
    glow_op="0.10",
    badge_fill="#262322",
    badge_stroke="#423f3c",
)


def chip_width(label: str) -> int:
    # Mono ~9.6px per char at 15px + 36px horizontal padding.
    return max(120, int(len(label) * 9.6 + 36))


def chip_boxes() -> list[tuple[str, float, float, float, float]]:
    """Return (label, x, y, w, h) for each pin."""
    boxes = []
    for label, col, row in PINS:
        w = chip_width(label)
        cy = ROW_Y[row]
        y = cy - CHIP_H / 2
        if col == "L":
            x = LEFT_X
        else:
            x = RIGHT_EDGE - w
        boxes.append((label, x, y, w, CHIP_H))
    return boxes


def beams_for(boxes: list[tuple[str, float, float, float, float]]) -> list[tuple[str, str, str]]:
    """Cubic beams from each chip's inner edge to the junction."""
    jx, jy = JUNCTION
    out = []
    delays = ["0s", "-0.7s", "-1.4s", "-2.1s"]
    for i, (label, x, y, w, h) in enumerate(boxes):
        cy = y + h / 2
        # left chips exit right edge; right chips exit left edge
        if x < jx:
            sx = x + w
            mid = sx + (jx - sx) * 0.55
            d = f"M {sx:.0f} {cy:.0f} C {mid:.0f} {cy:.0f} {mid:.0f} {jy} {jx - 14} {jy}"
            grad = "beamL"
        else:
            sx = x
            mid = sx - (sx - jx) * 0.55
            d = f"M {sx:.0f} {cy:.0f} C {mid:.0f} {cy:.0f} {mid:.0f} {jy} {jx + 14} {jy}"
            grad = "beamR"
        out.append((d, grad, delays[i % len(delays)]))
    return out


def chips_svg(p: dict, boxes: list) -> str:
    parts = []
    for label, x, y, w, h in boxes:
        parts.append(
            f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'rx="{CHIP_RX}" fill="{p["chip_fill"]}" stroke="{p["chip_stroke"]}" stroke-width="1.5"/>'
        )
        parts.append(
            f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + 5.5:.1f}" '
            f'font-family="\'Geist Mono\',Consolas,monospace" font-size="15" '
            f'text-anchor="middle" fill="{p["chip_text"]}">{label}</text>'
        )
    return "\n  ".join(parts)


def beams_svg(p: dict, beam_paths: list) -> str:
    base = [
        f'<path d="{d}" fill="none" stroke="url(#{g})" stroke-width="1.5"/>'
        for d, g, _ in beam_paths
    ]
    streaks = [
        f'<path class="flow" d="{d}" fill="none" stroke="{p["packet"]}" '
        f'stroke-width="1.8" stroke-linecap="round" style="animation-delay:{delay}"/>'
        for d, _, delay in beam_paths
    ]
    return "\n  ".join(base + streaks)


def svg(p: dict) -> str:
    boxes = chip_boxes()
    beam_paths = beams_for(boxes)
    labels = ", ".join(lab for lab, *_ in boxes)
    jx, jy = JUNCTION

    return f'''<svg viewBox="0 0 1280 680" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="mapTitle mapDesc">
  <title id="mapTitle">See it as one system — sanlee.me</title>
  <desc id="mapDesc">Four repository chips — {labels} — connect by beams into a single node that points down to a sanlee.me button under the heading "See it as one system." A small circuit trace rises through net ops, software, and product in the top right corner.</desc>
  <defs>
    <style>
      @font-face {{ font-family: 'Geist'; font-style: normal; font-weight: 100 900; src: url(data:font/woff2;base64,{b64["GEIST"]}) format('woff2'); }}
      @font-face {{ font-family: 'Geist Mono'; font-style: normal; font-weight: 400; src: url(data:font/woff2;base64,{b64["MONO"]}) format('woff2'); }}
      .flow {{ stroke-dasharray: 6 122; stroke-dashoffset: 0; opacity: 0.85; animation: flow 3.2s linear infinite; }}
      .flowv {{ stroke-dasharray: 6 112; stroke-dashoffset: 0; opacity: 0.85; animation: flowv 2.2s linear infinite; }}
      .pulse {{ animation: pulse 2.6s cubic-bezier(0.22, 0.61, 0.36, 1) infinite; }}
      .dotb {{ animation: blink 2.6s ease-in-out infinite; }}
      @keyframes flow {{ to {{ stroke-dashoffset: -128; }} }}
      @keyframes flowv {{ to {{ stroke-dashoffset: -118; }} }}
      @keyframes pulse {{ 0% {{ opacity: 0.45; }} 70% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
      @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.35; }} }}
      @media (prefers-reduced-motion: reduce) {{
        .flow, .flowv, .pulse, .dotb {{ animation: none !important; }}
        .flow, .flowv, .pulse {{ opacity: 0; }}
      }}
    </style>
    <!-- hairline grid: portfolio plates, not Vercel plus marks -->
    <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M 48 0 L 0 0 0 48" fill="none" stroke="{p["grid"]}" stroke-width="1"/>
    </pattern>
    <radialGradient id="glow" cx="50%" cy="40%" r="55%">
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
    <rect x="0" y="0" width="1280" height="680" fill="url(#grid)"/>
    <ellipse cx="640" cy="300" rx="520" ry="280" fill="url(#glow)"/>
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
  <rect x="88" y="72" width="248" height="30" rx="4" fill="{p["badge_fill"]}" stroke="{p["badge_stroke"]}" stroke-width="1.5"/>
  <circle class="dotb" cx="108" cy="87" r="3.5" fill="{p["oxide"]}"/>
  <text x="122" y="91.5" font-family="'Geist Mono',Consolas,monospace" font-size="11" letter-spacing="2.2" fill="{p["meta"]}">THE REPOS ARE THE PARTS</text>
  <!-- heading -->
  <text x="86" y="168" font-family="'Geist','Segoe UI',sans-serif" font-size="56" font-weight="700" letter-spacing="-2"><tspan fill="url(#tgrad)">See it as </tspan><tspan fill="url(#hgrad)">one system</tspan></text>
  <text x="90" y="206" font-family="'Geist','Segoe UI',sans-serif" font-size="17" font-weight="400" fill="{p["argument"]}">decisions recorded, reversals included — how the parts fit together</text>
  <!-- rule under standfirst -->
  <line x1="90" y1="228" x2="340" y2="228" stroke="{p["rule"]}" stroke-width="2"/>
  <!-- beams + chips -->
  {beams_svg(p, beam_paths)}
  {chips_svg(p, boxes)}
  <!-- junction -->
  <circle class="pulse" cx="{jx}" cy="{jy}" r="22" fill="none" stroke="{p["oxide"]}" stroke-width="2"/>
  <circle cx="{jx}" cy="{jy}" r="11" fill="none" stroke="{p["oxide"]}" stroke-width="2.5"/>
  <circle cx="{jx}" cy="{jy}" r="3.5" fill="{p["core"]}"/>
  <!-- stem + CTA -->
  <path d="M {jx} {jy + 14} V {CTA_Y - 28}" fill="none" stroke="{p["oxide"]}" stroke-width="2.5"/>
  <path class="flowv" d="M {jx} {jy + 14} V {CTA_Y - 28}" fill="none" stroke="{p["packet"]}" stroke-width="2" stroke-linecap="round"/>
  <polygon points="{jx - 7},{CTA_Y - 28} {jx + 7},{CTA_Y - 28} {jx},{CTA_Y - 16}" fill="{p["oxide"]}"/>
  <rect x="520" y="{CTA_Y}" width="240" height="54" rx="4" fill="{p["pill_fill"]}" filter="url(#pillshadow)"/>
  <text x="618" y="{CTA_Y + 34}" font-family="'Geist','Segoe UI',sans-serif" font-size="20" font-weight="600" text-anchor="middle" fill="{p["pill_text"]}">sanlee.me</text>
  <g stroke="{p["pill_text"]}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M 684 {CTA_Y + 27} H 704 M 697 {CTA_Y + 20} L 704 {CTA_Y + 27} L 697 {CTA_Y + 34}"/>
  </g>
  <rect x="1" y="1" width="1278" height="678" rx="3" fill="none" stroke="{p["border"]}" stroke-width="1.5"/>
</svg>
'''


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "one-system-dark.svg").write_text(svg(DARK), encoding="utf-8")
    (OUT / "one-system-light.svg").write_text(svg(LIGHT), encoding="utf-8")
    print("dark:", (OUT / "one-system-dark.svg").stat().st_size, "bytes")
    print("light:", (OUT / "one-system-light.svg").stat().st_size, "bytes")
    print("pins:", ", ".join(lab for lab, _, _ in PINS))


if __name__ == "__main__":
    main()
