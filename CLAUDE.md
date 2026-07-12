# CLAUDE.md

Guidance for AI agents working in this repo (the GitHub profile README).

## Content policy: shipped facts only, link the evolving story (hard rule)

Decided 2026-07-05, recorded system-wide in `architecture/SYS-009` (the
"volatility rule for outward surfaces" amendment).

This README restates **only shipped, immutable facts**: released versions,
measured eval numbers, what a repo *is* and *did*. It does **not** restate
plans, roadmaps, or organizing framings (e.g. the autonomy ladder,
`classifier/ADR-006`) — those move with every ADR, and every surface that
restates one becomes a standing sweep obligation. The evolving system story
lives at [sanlee.me](https://sanlee.me) and the architecture portal; this
README links there ("See it as one system") and stops.

Concretely, when updating a project blurb:

- **Add** a fact once it has shipped (a tagged release, a merged measured
  result). Past-tense, specific, with the number if there is one.
- **Do not add** upcoming levels, planned versions, or the current framing of
  where the portfolio is headed, even when an ADR has accepted it. Accurate
  restatements of a framing go stale the moment the framing evolves — that is
  the drift this policy exists to prevent (the pre-ladder classifier blurb
  was the motivating instance).
- When a decision elsewhere changes what a blurb *means* (not just what is
  true), the deciding PR's "Downstream surfaces" list should name this README;
  if you are that session, sweep it here.

## Length bar: this is a skim surface (hard rule)

Decided 2026-07-11 after the shipped-facts refresh made the classifier blurb
absorb repo-README density (four decimal numbers + CI architecture in one
blurb).

- **Each project blurb: at most 3 sentences.** What it is, the headline
  number(s) if any, one distinctive finding. Detailed figures (per-label F1,
  macro-F1 pairs, gate architecture, mechanism) live in the repo's own README
  — the blurb links, it does not restate.
- **Intro: at most 2 paragraphs** before "What I'm building".
- **Adding a shipped fact means compressing, not appending.** New facts
  displace old detail; the blurb's length stays at the bar. If the new fact
  can't fit without losing the old headline, the repo's README is the right
  home for one of them.

## Voice

Same bar as the portfolio (see `portfolio` repo conventions): survives a
skeptical senior engineer, owns the solo scale and the AI assist, right-sized
claims, no hype. Negative results are stated as such ("the lift was marginal,
so I shipped the negative result").

The AI assist is stated as **method, not confession** (decided 2026-07-11;
canonical framing = the portfolio colophon): San sets the direction, the
contracts, and the bar; Claude does most of the typing; the evals and
postmortems are the proof. No apologetic framing ("full disclosure",
"disclaimer") and no self-labels ("agentic orchestration") — describe the
practice, name Claude plainly.
