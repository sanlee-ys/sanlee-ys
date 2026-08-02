"""Generate images/one-system-{dark,light}.svg — the profile's only graphic.

The SVGs are GENERATED OUTPUT; hand-edits get overwritten. Change this script and
rebuild both variants in the same commit:

    uv run python scripts/build_map.py

Fonts: Geist + Geist Mono (latin woff2, Google Fonts, OFL) are downloaded at build
time and embedded as base64 ``@font-face`` data URIs. GitHub serves README images
through a proxy that blocks *external* fetches, but inline data URIs render fine —
that is the whole trick that makes a real webfont work here. ~60 KB per SVG.

Motion: the beams carry light packets (CSS stroke-dashoffset animation), the junction
pulses, the kicker dot blinks. CSS animations run inside GitHub's proxied ``<img>``;
everything is switched off (and the streak overlays hidden) under
``prefers-reduced-motion: reduce``. No SMIL, no JS.

If the pinned repo set changes, update LEFT/RIGHT below in the same sitting (chip
widths are sized per label). Repo names are labels, not claims — see CLAUDE.md's
no-performance-claims rule for what must never appear in this graphic's text.
"""
import base64
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "images"
FONTS = {
    "GEIST": "https://fonts.gstatic.com/s/geist/v5/gyByhwUxId8gMEwcGFU.woff2",
    "MONO": "https://fonts.gstatic.com/s/geistmono/v6/or3yQ6H-1_WfwkMZI_qYPLs1a-t7PU0AbeE9KK5U5Ck.woff2",
}

def fetch_b64(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 - fixed https URLs
        data = r.read()
    print(f"{url.rsplit('/', 1)[-1]}: {len(data)} bytes")
    return base64.b64encode(data).decode()

b64 = {k: fetch_b64(u) for k, u in FONTS.items()}

DARK = dict(
    bg="#09090b", plus="#232329", border="#26262a",
    glow_a="#5c9eff", glow_a_op="0.12", glow_b="#a78bfa", glow_b_op="0.09",
    badge_fill="#111113", badge_stroke="#27272a", kicker="#71717a",
    grad_a="#fafafa", grad_b="#8b8f98", hgrad_a="#7cb1ff", hgrad_b="#b79cff",
    sub="#a1a1aa",
    chip_fill="#111113", chip_stroke="#27272a", chip_text="#e4e4e7",
    beam_far="#2e2e33", accent="#5c9eff", packet="#9cc4ff", core="#fafafa",
    pill="#fafafa", pill_text="#09090b", pill_glow="#5c9eff",
    trace="#26262a", trace_label="#71717a",
)
LIGHT = dict(
    bg="#ffffff", plus="#dcdce2", border="#e4e4e7",
    glow_a="#2563eb", glow_a_op="0.07", glow_b="#7c3aed", glow_b_op="0.05",
    badge_fill="#fafafa", badge_stroke="#e4e4e7", kicker="#71717a",
    grad_a="#09090b", grad_b="#44444b", hgrad_a="#2563eb", hgrad_b="#7c3aed",
    sub="#52525b",
    chip_fill="#fafafa", chip_stroke="#e4e4e7", chip_text="#27272a",
    beam_far="#e4e4e7", accent="#2563eb", packet="#2563eb", core="#09090b",
    pill="#09090b", pill_text="#fafafa", pill_glow="#2563eb",
    trace="#e4e4e7", trace_label="#71717a",
)

# The six pinned repos: (label, chip x, chip width, row center y).
# Left column chips end at x=508; right column chips start at x=772.
LEFT = [("defense-news-classifier", 251, 257, 310), ("agent-ops", 386, 122, 390), ("kb-agent", 395, 113, 470)]
RIGHT = [("faithfulness-judge", 772, 209, 310), ("architecture", 772, 151, 390), ("learning-notes", 772, 170, 470)]

# Beam geometry, chip edge -> junction (640,390). Streak overlays reuse these.
BEAMS = [
    ("M 508 310 C 566 310 588 388 626 390", "beamL", "0s"),
    ("M 508 390 C 560 390 590 390 626 390", "beamL", "-0.9s"),
    ("M 508 470 C 566 470 588 392 626 390", "beamL", "-1.8s"),
    ("M 772 310 C 714 310 692 388 654 390", "beamR", "-0.5s"),
    ("M 772 390 C 720 390 690 390 654 390", "beamR", "-1.4s"),
    ("M 772 470 C 714 470 692 392 654 390", "beamR", "-2.2s"),
]

def chips(p):
    out = []
    for label, x, w, cy in LEFT + RIGHT:
        out.append(f'<rect x="{x}" y="{cy-22}" width="{w}" height="44" rx="10" fill="{p["chip_fill"]}" stroke="{p["chip_stroke"]}" stroke-width="1.5"/>')
        out.append(f'<text x="{x + w/2}" y="{cy+5.5}" font-family="\'Geist Mono\',Consolas,monospace" font-size="16" text-anchor="middle" fill="{p["chip_text"]}">{label}</text>')
    return "\n  ".join(out)

def beams(p):
    base = [f'<path d="{d}" fill="none" stroke="url(#{grad})" stroke-width="1.5"/>' for d, grad, _ in BEAMS]
    streaks = [
        f'<path class="flow" d="{d}" fill="none" stroke="{p["packet"]}" stroke-width="1.8" stroke-linecap="round" style="animation-delay:{delay}"/>'
        for d, _, delay in BEAMS
    ]
    return "\n  ".join(base + streaks)

def svg(p):
    return f'''<svg viewBox="0 0 1280 680" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="mapTitle mapDesc">
  <title id="mapTitle">See it as one system - sanlee.me</title>
  <desc id="mapDesc">Six repository chips - defense-news-classifier, agent-ops, kb-agent on the left; faithfulness-judge, architecture, learning-notes on the right - connect by beams into a single pulsing node, which points down to a sanlee.me button under the heading "See it as one system." A small circuit trace rises through net ops, software, and product in the top right corner.</desc>
  <defs>
    <style>
      @font-face {{ font-family: 'Geist'; font-style: normal; font-weight: 100 900; src: url(data:font/woff2;base64,{b64["GEIST"]}) format('woff2'); }}
      @font-face {{ font-family: 'Geist Mono'; font-style: normal; font-weight: 400; src: url(data:font/woff2;base64,{b64["MONO"]}) format('woff2'); }}
      .flow {{ stroke-dasharray: 6 122; stroke-dashoffset: 0; opacity: 0.9; animation: flow 3.2s linear infinite; }}
      .flowv {{ stroke-dasharray: 6 112; stroke-dashoffset: 0; opacity: 0.9; animation: flowv 2.2s linear infinite; }}
      .pulse {{ animation: pulse 2.6s cubic-bezier(0.22, 0.61, 0.36, 1) infinite; }}
      .dotb {{ animation: blink 2.6s ease-in-out infinite; }}
      @keyframes flow {{ to {{ stroke-dashoffset: -128; }} }}
      @keyframes flowv {{ to {{ stroke-dashoffset: -118; }} }}
      @keyframes pulse {{ 0% {{ opacity: 0.4; }} 70% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
      @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
      @media (prefers-reduced-motion: reduce) {{
        .flow, .flowv, .pulse, .dotb {{ animation: none !important; }}
        .flow, .flowv, .pulse {{ opacity: 0; }}
      }}
    </style>
    <pattern id="plus" width="160" height="160" patternUnits="userSpaceOnUse">
      <path d="M 80 74 V 86 M 74 80 H 86" stroke="{p["plus"]}" stroke-width="1.2"/>
    </pattern>
    <radialGradient id="glowA" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{p["glow_a"]}" stop-opacity="{p["glow_a_op"]}"/>
      <stop offset="100%" stop-color="{p["glow_a"]}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{p["glow_b"]}" stop-opacity="{p["glow_b_op"]}"/>
      <stop offset="100%" stop-color="{p["glow_b"]}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="tgrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{p["grad_a"]}"/>
      <stop offset="100%" stop-color="{p["grad_b"]}"/>
    </linearGradient>
    <linearGradient id="hgrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p["hgrad_a"]}"/>
      <stop offset="100%" stop-color="{p["hgrad_b"]}"/>
    </linearGradient>
    <linearGradient id="beamL" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p["beam_far"]}"/>
      <stop offset="100%" stop-color="{p["accent"]}"/>
    </linearGradient>
    <linearGradient id="beamR" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0%" stop-color="{p["beam_far"]}"/>
      <stop offset="100%" stop-color="{p["accent"]}"/>
    </linearGradient>
    <filter id="pillshadow" x="-40%" y="-60%" width="180%" height="260%">
      <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="{p["pill_glow"]}" flood-opacity="0.28"/>
    </filter>
    <clipPath id="frame"><rect x="0" y="0" width="1280" height="680" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect x="0" y="0" width="1280" height="680" fill="{p["bg"]}"/>
    <rect x="0" y="0" width="1280" height="680" fill="url(#plus)"/>
    <ellipse cx="380" cy="60" rx="560" ry="300" fill="url(#glowA)"/>
    <ellipse cx="960" cy="640" rx="560" ry="300" fill="url(#glowB)"/>
  </g>
  <!-- the arc, corner signature -->
  <g clip-path="url(#frame)">
    <path d="M 920 160 H 1000 L 1025 140 H 1105 L 1130 120 H 1195" fill="none" stroke="{p["trace"]}" stroke-width="2"/>
    <rect x="914" y="154" width="12" height="12" rx="2.5" fill="none" stroke="{p["accent"]}" stroke-width="2"/>
    <circle cx="1065" cy="140" r="5.5" fill="none" stroke="{p["accent"]}" stroke-width="2"/>
    <rect x="1195" y="114" width="12" height="12" rx="2.5" transform="rotate(45 1201 120)" fill="{p["accent"]}"/>
    <g font-family="'Geist Mono',Consolas,monospace" font-size="10" letter-spacing="2" fill="{p["trace_label"]}">
      <text x="920" y="184" text-anchor="middle">NET&#160;OPS</text>
      <text x="1065" y="164" text-anchor="middle">SOFTWARE</text>
      <text x="1201" y="144" text-anchor="middle">PRODUCT</text>
    </g>
  </g>
  <!-- kicker badge -->
  <rect x="88" y="74" width="256" height="32" rx="16" fill="{p["badge_fill"]}" stroke="{p["badge_stroke"]}" stroke-width="1.5"/>
  <circle class="dotb" cx="108" cy="90" r="3.5" fill="{p["accent"]}"/>
  <text x="122" y="94.5" font-family="'Geist Mono',Consolas,monospace" font-size="11" letter-spacing="2.4" fill="{p["kicker"]}">THE REPOS ARE THE PARTS</text>
  <!-- heading -->
  <text x="86" y="188" font-family="'Geist','Segoe UI',sans-serif" font-size="60" font-weight="600" letter-spacing="-2"><tspan fill="url(#tgrad)">See it as </tspan><tspan fill="url(#hgrad)">one system</tspan></text>
  <text x="90" y="228" font-family="'Geist','Segoe UI',sans-serif" font-size="18" font-weight="400" fill="{p["sub"]}">the decisions behind each call, and how it all fits together</text>
  <!-- beams + packet streaks -->
  {beams(p)}
  <!-- repo chips -->
  {chips(p)}
  <!-- junction -->
  <circle class="pulse" cx="640" cy="390" r="20" fill="none" stroke="{p["accent"]}" stroke-width="2"/>
  <circle cx="640" cy="390" r="10" fill="none" stroke="{p["accent"]}" stroke-width="2.5"/>
  <circle cx="640" cy="390" r="3.5" fill="{p["core"]}"/>
  <!-- stem + CTA -->
  <path d="M 640 402 V 520" fill="none" stroke="{p["accent"]}" stroke-width="2.5"/>
  <path class="flowv" d="M 640 402 V 520" fill="none" stroke="{p["packet"]}" stroke-width="2" stroke-linecap="round"/>
  <polygon points="633,520 647,520 640,532" fill="{p["accent"]}"/>
  <rect x="520" y="546" width="240" height="58" rx="29" fill="{p["pill"]}" filter="url(#pillshadow)"/>
  <text x="624" y="583" font-family="'Geist','Segoe UI',sans-serif" font-size="21" font-weight="600" text-anchor="middle" fill="{p["pill_text"]}">sanlee.me</text>
  <g stroke="{p["pill_text"]}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M 690 575 H 710 M 703 568 L 710 575 L 703 582"/>
  </g>
  <rect x="1" y="1" width="1278" height="678" rx="15" fill="none" stroke="{p["border"]}" stroke-width="1.5"/>
</svg>
'''

(OUT / "one-system-dark.svg").write_text(svg(DARK), encoding="utf-8")
(OUT / "one-system-light.svg").write_text(svg(LIGHT), encoding="utf-8")
print("dark:", (OUT / "one-system-dark.svg").stat().st_size, "bytes")
print("light:", (OUT / "one-system-light.svg").stat().st_size, "bytes")
