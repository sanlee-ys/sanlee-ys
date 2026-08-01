"""Generate images/one-system-{dark,light}.svg — the profile's only graphic.

The SVGs are GENERATED OUTPUT; hand-edits get overwritten. Change this script and
rebuild both variants in the same commit:

    uv run python scripts/build_map.py

Fonts: Geist + Geist Mono (latin woff2, Google Fonts, OFL) are downloaded at build
time and embedded as base64 ``@font-face`` data URIs. GitHub serves README images
through a proxy that blocks *external* fetches, but inline data URIs render fine —
that is the whole trick that makes a real webfont work here. ~59 KB per SVG.

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
    bg="#0a0a0a", dot="#1e1e22", border="#26262a", glow="#5c9eff", glow_op="0.10",
    kicker="#71717a", grad_a="#fafafa", grad_b="#9ca0a8", sub="#a1a1aa",
    chip_fill="#131316", chip_stroke="#26262a", chip_text="#d4d4d8",
    beam_far="#2e2e33", accent="#5c9eff", core="#fafafa",
    pill="#fafafa", pill_text="#0a0a0a", trace="#26262a", trace_label="#71717a",
)
LIGHT = dict(
    bg="#ffffff", dot="#e8e8ec", border="#e4e4e7", glow="#2563eb", glow_op="0.05",
    kicker="#71717a", grad_a="#09090b", grad_b="#52525b", sub="#52525b",
    chip_fill="#fafafa", chip_stroke="#e4e4e7", chip_text="#3f3f46",
    beam_far="#e4e4e7", accent="#2563eb", core="#09090b",
    pill="#0a0a0a", pill_text="#fafafa", trace="#e4e4e7", trace_label="#71717a",
)

# The six pinned repos: (label, chip x, chip width, row center y).
# Left column chips end at x=508; right column chips start at x=772.
LEFT = [("defense-news-classifier", 251, 257, 302), ("claude-ops", 376, 132, 380), ("kb-agent", 395, 113, 458)]
RIGHT = [("faithfulness-judge", 772, 209, 302), ("architecture", 772, 151, 380), ("learning-notes", 772, 170, 458)]

def chips(p):
    out = []
    for label, x, w, cy in LEFT + RIGHT:
        out.append(f'<rect x="{x}" y="{cy-22}" width="{w}" height="44" rx="10" fill="{p["chip_fill"]}" stroke="{p["chip_stroke"]}" stroke-width="1.5"/>')
        out.append(f'<text x="{x + w/2}" y="{cy+5.5}" font-family="\'Geist Mono\',Consolas,monospace" font-size="16" text-anchor="middle" fill="{p["chip_text"]}">{label}</text>')
    return "\n  ".join(out)

def svg(p):
    return f'''<svg viewBox="0 0 1280 660" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="mapTitle mapDesc">
  <title id="mapTitle">See it as one system - sanlee.me</title>
  <desc id="mapDesc">Six repository chips - defense-news-classifier, claude-ops, kb-agent on the left; faithfulness-judge, architecture, learning-notes on the right - connect by beams into a single node, which points down to a sanlee.me button under the heading "See it as one system." A small circuit trace rises through net ops, software, and product in the top right corner.</desc>
  <defs>
    <style>
      @font-face {{ font-family: 'Geist'; font-style: normal; font-weight: 100 900; src: url(data:font/woff2;base64,{b64["GEIST"]}) format('woff2'); }}
      @font-face {{ font-family: 'Geist Mono'; font-style: normal; font-weight: 400; src: url(data:font/woff2;base64,{b64["MONO"]}) format('woff2'); }}
    </style>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="1.2" cy="1.2" r="1.2" fill="{p["dot"]}"/>
    </pattern>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{p["glow"]}" stop-opacity="{p["glow_op"]}"/>
      <stop offset="100%" stop-color="{p["glow"]}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="tgrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{p["grad_a"]}"/>
      <stop offset="100%" stop-color="{p["grad_b"]}"/>
    </linearGradient>
    <linearGradient id="beamL" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p["beam_far"]}"/>
      <stop offset="100%" stop-color="{p["accent"]}"/>
    </linearGradient>
    <linearGradient id="beamR" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0%" stop-color="{p["beam_far"]}"/>
      <stop offset="100%" stop-color="{p["accent"]}"/>
    </linearGradient>
    <clipPath id="frame"><rect x="0" y="0" width="1280" height="660" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect x="0" y="0" width="1280" height="660" fill="{p["bg"]}"/>
    <rect x="0" y="0" width="1280" height="660" fill="url(#dots)"/>
    <ellipse cx="640" cy="40" rx="560" ry="280" fill="url(#glow)"/>
  </g>
  <!-- the arc, corner signature -->
  <g clip-path="url(#frame)">
    <path d="M 920 150 H 1000 L 1025 130 H 1105 L 1130 110 H 1195" fill="none" stroke="{p["trace"]}" stroke-width="2"/>
    <rect x="914" y="144" width="12" height="12" rx="2.5" fill="none" stroke="{p["accent"]}" stroke-width="2"/>
    <circle cx="1065" cy="130" r="5.5" fill="none" stroke="{p["accent"]}" stroke-width="2"/>
    <rect x="1195" y="104" width="12" height="12" rx="2.5" transform="rotate(45 1201 110)" fill="{p["accent"]}"/>
    <g font-family="'Geist Mono',Consolas,monospace" font-size="10" letter-spacing="2" fill="{p["trace_label"]}">
      <text x="920" y="174" text-anchor="middle">NET&#160;OPS</text>
      <text x="1065" y="154" text-anchor="middle">SOFTWARE</text>
      <text x="1201" y="134" text-anchor="middle">PRODUCT</text>
    </g>
  </g>
  <!-- heading -->
  <rect x="90" y="87" width="6" height="6" fill="{p["accent"]}"/>
  <text x="106" y="95" font-family="'Geist Mono',Consolas,monospace" font-size="12" letter-spacing="3" fill="{p["kicker"]}">THE REPOS ARE THE PARTS</text>
  <text x="88" y="162" font-family="'Geist','Segoe UI',sans-serif" font-size="56" font-weight="600" letter-spacing="-1.7" fill="url(#tgrad)">See it as one system</text>
  <text x="90" y="202" font-family="'Geist','Segoe UI',sans-serif" font-size="18" font-weight="400" fill="{p["sub"]}">the decisions behind each call, and how it all fits together</text>
  <!-- beams -->
  <g fill="none" stroke-width="1.5">
    <path d="M 508 302 C 566 302 588 378 626 380" stroke="url(#beamL)"/>
    <path d="M 508 380 C 560 380 590 380 626 380" stroke="url(#beamL)"/>
    <path d="M 508 458 C 566 458 588 382 626 380" stroke="url(#beamL)"/>
    <path d="M 772 302 C 714 302 692 378 654 380" stroke="url(#beamR)"/>
    <path d="M 772 380 C 720 380 690 380 654 380" stroke="url(#beamR)"/>
    <path d="M 772 458 C 714 458 692 382 654 380" stroke="url(#beamR)"/>
  </g>
  <!-- repo chips -->
  {chips(p)}
  <!-- junction -->
  <circle cx="640" cy="380" r="18" fill="none" stroke="{p["accent"]}" stroke-opacity="0.25" stroke-width="2"/>
  <circle cx="640" cy="380" r="10" fill="none" stroke="{p["accent"]}" stroke-width="2.5"/>
  <circle cx="640" cy="380" r="3.5" fill="{p["core"]}"/>
  <!-- stem + CTA -->
  <path d="M 640 398 V 512" fill="none" stroke="{p["accent"]}" stroke-width="2.5"/>
  <polygon points="633,512 647,512 640,524" fill="{p["accent"]}"/>
  <rect x="522" y="536" width="236" height="56" rx="28" fill="{p["pill"]}"/>
  <text x="624" y="572" font-family="'Geist','Segoe UI',sans-serif" font-size="21" font-weight="600" text-anchor="middle" fill="{p["pill_text"]}">sanlee.me</text>
  <g stroke="{p["pill_text"]}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M 690 564 H 710 M 703 557 L 710 564 L 703 571"/>
  </g>
  <rect x="1" y="1" width="1278" height="658" rx="15" fill="none" stroke="{p["border"]}" stroke-width="1.5"/>
</svg>
'''

(OUT / "one-system-dark.svg").write_text(svg(DARK), encoding="utf-8")
(OUT / "one-system-light.svg").write_text(svg(LIGHT), encoding="utf-8")
print("dark:", (OUT / "one-system-dark.svg").stat().st_size, "bytes")
print("light:", (OUT / "one-system-light.svg").stat().st_size, "bytes")
