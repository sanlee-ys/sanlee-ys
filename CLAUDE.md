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

- **Each project blurb: at most 60 words.** What it is, the headline
  number(s) if any, one distinctive finding. Detailed figures (per-label F1,
  macro-F1 pairs, gate architecture, mechanism) live in the repo's own README
  — the blurb links, it does not restate.

  This was a 3-sentence cap until 2026-07-26. Sentence-counting does not bind:
  every blurb stayed compliant while growing to 80–105 words, because the
  sentences got longer instead of more numerous, which reproduced exactly the
  repo-README density the rule was written to prevent. Count words.
- **Intro: at most 2 paragraphs** before "What I'm building".
- **Adding a shipped fact means compressing, not appending.** New facts
  displace old detail; the blurb's length stays at the bar. If the new fact
  can't fit without losing the old headline, the repo's README is the right
  home for one of them.

## The classifier claims carry SYS-019 markers — do not strip them (hard rule)

Decided 2026-07-26, after the blurb was found still advertising `v3.0.0` a day
after v3.1.0 shipped. The numbers happened to be unchanged, so only the label
was stale — and nothing mechanical would have caught it.

The classifier version and its three accuracies are wrapped in HTML-comment
markers and asserted in CI **by `architecture/scripts/check_program_metrics.py`**,
which fetches this README raw from `main` and compares each marked value against
the classifier's `evals/metrics.json`:

    <!-- version:classifier -->v3.1.0 scores <!-- metric:category_accuracy -->92.6% category

Consequences for anyone editing that blurb:

- **The markers are invisible in rendered Markdown.** They cost no words against
  the length bar above, and deleting one is not a cosmetic change — it removes a
  guarantee. The checker fails on zero markers, so a strip surfaces as a red
  build in `architecture`, not here.
- **Never wrap a marked value in backticks.** The checker strips code spans
  before scanning, so `` `v3.1.0` `` matches nothing and the check silently
  verifies nothing. That is why the version lost its backticks; leave it plain.
- **The marker goes immediately before the value**, and the metric key must
  exist in the artifact's `gold` object. A typo'd key fails rather than passing
  forever.

**The kb-agent and faithfulness-judge numbers are deliberately NOT marked.**
Neither repo publishes a machine-readable artifact — kb-agent's figures live in
its README prose, the judge's in `evals/results.md` — so there is nothing to
assert against. They are counted against an allowance in the checker that may
only shrink. If either repo ever publishes an artifact, mark them and drop the
allowance.

## Why this repo still has no workflow

Guarding the above was evaluated as a workflow *here* and deliberately declined.
It would have been this repo's first workflow (dragging in the Dependabot block
below, plus a Python toolchain for one script in a six-file repo), and it would
have been the **fifth** SYS-019 checker — which is the exact condition that ADR
names as its own revisit trigger, where "the duplication argument flips."
Extending the existing fourth checker to fetch this file reaches the same claims
without any of that.

The accepted tradeoff is that this is **detection, not prevention**: a bad edit
here merges green and reddens `architecture` afterward. If that lag ever bites,
the answer is a workflow here, not a second checker.

## No Dependabot config until this repo has a workflow (hard rule)

A `github-actions` block does **not** sit inert on a repo with nothing to scan — with
no `action.yml` and no `.github/workflows/*.yml` it fails the update run every week
with `dependency_file_not_found` ("/action.yml or /.github/workflows/<anything>.yml
not found"). That is why the old config was removed rather than repaired: no version
of it is both present and green here.

So the block goes in **the same PR as the first workflow**, never ahead of it. A
watcher pointed at nothing isn't caution, it's a standing false alarm that teaches you
to ignore a red `main` — which is what it did, weekly, from at least 2026-07-11 until
[#29](https://github.com/sanlee-ys/sanlee-ys/pull/29) removed it on 2026-07-25.

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
