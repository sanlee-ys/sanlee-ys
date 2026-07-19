<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="images/banner-light.svg">
  <img alt="San Lee · From the wires up: network operations to software engineering to product" src="images/banner-dark.svg">
</picture>

Network operations to software engineering to product. I'm a Senior Product Associate at
JPMorganChase now, building AI tools on the side to stay hands-on.

These projects started as a way to dust off years of accumulated engineering rust and turned 
into work I can actually stand behind technically. 

They're built by directing Claude: I set the direction, the contracts, and the bar; it 
does most of the typing; the evals and postmortems are the proof. 

**See it as one system → [sanlee.me](https://sanlee.me).** The repos below are the parts. The site is how they fit together, the decisions behind each call, and an honest note on how it was built.

## What I'm building

**[defense-news-classifier](https://github.com/sanlee-ys/defense-news-classifier)** — 
LLM classifier for public defense news snippets: category, operational domain, and region 
via structured tool-use output, graded against a human-labeled eval whose accuracy floors 
block every PR (the live model run is weekly, not per-PR), and served as a containerized 
FastAPI endpoint that two other repos here call. `v3.0.0` scores 92.6% 
category / 92.6% domain / 87.0% region on a 54-snippet human answer key; a 300-snippet 
judge-graded run corroborates category and domain at 93.3% [89.9, 95.6] and 90.3% 
[86.5, 93.2]. Two escalations have been measured and declined: BM25 grounding was retired 
once it stopped beating the ungrounded classifier, and tiered routing moved +0 rows on both 
axes at ~1.97x the cost.

**[claude-ops](https://github.com/sanlee-ys/claude-ops)** — 
The operating layer for the Claude-assisted workflow this page describes: a `PreToolUse` 
credential-guard hook rebuilt into a path-based default-deny after four credential-exposure 
events in one week, three of them the same token leaking through a different tool shape. 
Six blameless postmortems keep the failures in, and a 63-test suite gates CI, 28 of them 
pinned red-team findings from five adversarial rounds. A separate test class asserts the 
shapes the guard deliberately does *not* block, so the control's own boundary fails the 
build if a later fix quietly widens it.

**[kb-agent](https://github.com/sanlee-ys/kb-agent)** — 
A knowledge base over my projects and their dependencies, served from one tool 
implementation across two transports: a Claude tool-use agent and an MCP server any host can 
mount, sharing the same functions and the same descriptions. The cross-repo HTTP seams that 
let it drive my running services are deliberately kept off the MCP surface, since a server 
that quietly needs two background processes is a bad install. Retrieval is graded against a 
hand-labeled 27-query gold set (recall@5 0.926, MRR 0.781), and the harness aborts on any 
non-success observation rather than scoring an unindexed KB as zero recall.

**[faithfulness-judge](https://github.com/sanlee-ys/faithfulness-judge)** — 
Measures whether an LLM judge can be trusted to catch unsupported claims, scored against 191 
human-labeled claims on public defense text. Both tiers land in substantial agreement (Opus 
κ 0.742, Sonnet κ 0.696) with overlapping confidence intervals, so the cheap tier is good 
enough and the escalation is not evidenced. A `max_tokens=10` truncation had silently 
corrupted 20% of Sonnet's verdicts and manufactured a false tier gap, caught by reading the 
misjudgment log one commit before publishing.

Also public: **[architecture](https://github.com/sanlee-ys/architecture)** (cross-repo ADRs 
and the system portal), **[notes-api](https://github.com/sanlee-ys/notes-api)** (FastAPI 
service with an async enrichment seam to the classifier), and 
**[learning-notes](https://github.com/sanlee-ys/learning-notes)** (plain-language notes on 
the concepts behind all of it).

## Day job
In Employee Platforms, I run product for SharePoint Online and OneDrive — the collaboration 
platforms every JPMorganChase line of business works in. The work: lifecycle, migration, and 
automating the operations around both.

## Stack
**Now:** Python · FastAPI · Anthropic API (tool use, MCP, evals) · GitHub Actions · vanilla JS + D3 · Microsoft 365 · Jira  
**Earlier (SWE):** Python · Java · Kafka · event-driven microservices · CockroachDB · Cassandra · MySQL · Kubernetes · Docker · OpenTelemetry

## Background
Seoul National University MBA · B.A. Information Technology, Rutgers–New Brunswick · AWS Certified Cloud Practitioner · U.S. Army National Guard veteran (Qatar, OEF)

Outside work: photography, hiking, and supervised by a Scottish Fold named Sango.

<p align="center"><a href="https://www.linkedin.com/in/leesan/">LinkedIn</a> · <a href="https://www.instagram.com/sanleeeee/">Instagram</a> · <a href="https://vsco.co/sanlee">VSCO</a> · <a href="https://sanlee.me">Portfolio</a></p>

<p align="center">
  <img src="images/sango-boop.jpeg" alt="Sango, a Scottish Fold, asleep" width="240" height="240" />
</p>

<p align="center"><em>Sango, Chief Nap Officer.</em></p>
