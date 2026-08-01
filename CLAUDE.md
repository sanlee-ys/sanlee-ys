# CLAUDE.md

Guidance for AI agents working in this repo (the GitHub profile README).

## What this page is (decided 2026-07-31, the redesign)

An identity surface, nothing else: banner, a two-paragraph intro (who I am, how I work),
a clickable system-map graphic pointing to [sanlee.me](https://sanlee.me), and a short
footer. The **pinned repos** are the project showcase (their descriptions carry the
numbers), and the **portfolio site** is the story of how the parts fit together.

This replaced the 2026-07 "shipped-facts blurbs" design (one measured paragraph per
project, SYS-019 metric markers asserted by the `architecture` repo's checker). The
blurbs kept absorbing repo-README density and the numbers needed cross-repo guarding;
the redesign deletes the claims instead of guarding them harder.

## No performance claims on this surface (hard rule)

No eval numbers, no version strings, no benchmark or coverage figures — not in prose,
not in image text. A number here is an outward claim that goes stale silently: this repo
has no workflow, and since 2026-07-31 (architecture PR #80) **no external checker reads
this file either**. There is no guard to catch drift; the rule is that there is nothing
to drift.

Where a claim belongs instead: the owning repo's README/description (it sits next to the
measurement), or the portfolio (guarded by the portfolio's own checks).

If a number ever deliberately returns to this README, the same change must re-add this
surface to `REMOTE_SCANNED` in `architecture/scripts/check_program_metrics.py` (the
mechanism and its tests were kept for exactly that) and update this section.

## Length bar (hard rule)

- **Intro: at most 2 paragraphs** between the banner and the system-map graphic.
- **No per-project sections or blurbs.** The pins are the project list. If a repo needs
  more said about it here than its pin shows, that prose belongs in the repo or on the
  site, not on this page.
- Footer: background line, outside-work line, links, Sango. Nothing that needs updating
  on a release.

## images/ — the four SVGs

`banner-{dark,light}.svg` (1280×300): name, tagline, and a circuit trace rising through
NET OPS → SOFTWARE → PRODUCT. `system-map-{dark,light}.svg` (1280×420): the six pinned
repo names converging into one node that points at sanlee.me; the README wraps it in a
link to the site (SVGs rendered through `<img>` cannot carry live links themselves).

- Palette. Dark: bg `#0f1115`, text `#e7eaf0`, muted `#9aa3b2`, accent `#6ea8fe`,
  lines `#232a35`/`#2a3342`. Light: bg `#ffffff`, text `#1f2328`, muted `#59636e`,
  accent `#2563eb`, lines `#d1d9e0`.
- Text must use system font stacks only — GitHub serves README images through a proxy
  that blocks external fetches, so a webfont reference would silently fall back anyway.
- **If the pinned set changes, the system-map labels must change in the same sitting.**
  Nothing checks this; it is the one piece of repo state this page still mirrors.
- Repo names in the graphic are labels, not claims — adding one is fine under the
  no-claims rule.

## Why this repo still has no workflow

Previously: the metric markers were checked remotely rather than by a first workflow
here. Now there are no metrics at all, so there is nothing to check — the no-workflow
stance stands with less machinery behind it. If this repo ever does grow a workflow,
the Dependabot rule below still applies.

## No Dependabot config until this repo has a workflow (hard rule)

A `github-actions` block does **not** sit inert on a repo with nothing to scan — with
no `action.yml` and no `.github/workflows/*.yml` it fails the update run every week
with `dependency_file_not_found`. The block goes in **the same PR as the first
workflow**, never ahead of it. A watcher pointed at nothing isn't caution, it's a
standing false alarm that teaches you to ignore a red `main` — which is what it did,
weekly, until [#29](https://github.com/sanlee-ys/sanlee-ys/pull/29) removed it on
2026-07-25.

## Voice

Same bar as the portfolio (see `portfolio` repo conventions): survives a skeptical
senior engineer, owns the solo scale and the AI assist, right-sized claims, no hype.

The AI assist is stated as **method, not confession** (decided 2026-07-11; canonical
framing = the portfolio colophon): San sets the direction, the contracts, and the bar;
Claude does most of the typing; the evals and postmortems are the proof. No apologetic
framing ("full disclosure", "disclaimer") and no self-labels ("agentic orchestration")
— describe the practice, name Claude plainly.
