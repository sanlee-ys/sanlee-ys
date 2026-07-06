<picture>
  <source media="(prefers-color-scheme: dark)" srcset="images/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="images/banner-light.svg">
  <img alt="San Lee · From the wires up: network operations to software engineering to product" src="images/banner-dark.svg">
</picture>

Network operations to software engineering to product. I'm a Senior Product Associate at
JPMorganChase now, building AI tools on the side to stay hands-on.

What started as a way to dust off years of accumulated engineering rust turned into something 
more. A way to build on what I've picked up over the years and turn it into work I can actually 
stand behind technically, while pushing me into the domains I'm trying to explore.

It's also my disclaimer: Claude's helping me move a lot faster. Even the little things like 
setting up boilerplate or working in a `.venv` without tripping over it took real time to 
learn. Now I'm orchestrating tightly scoped sessions and letting Claude do most of the rest.

I'm having fun while I'm (re)learning on-the-go. If you couldn't tell by now, I've had 
something of an odd career path. That's another story, but the bet I'm hedging *with* (and not 
against) is AI.

**See it as one system → [sanlee.me](https://sanlee.me).** The repos below are the parts. The site is how they fit together, the decisions behind each call, and an honest note on how it was built.

## What I'm building

**[kb-agent](https://github.com/sanlee-ys/kb-agent)** — 
Personal, living knowledge base over your projects and their dependencies. A local 
Claude RAG + tool-use agent you can ask questions, or point at your projects' own 
running services to have it call them directly.

**[defense-news-classifier](https://github.com/sanlee-ys/defense-news-classifier)** — 
LLM classifier for public defense news snippets. Assigns category and operational domain 
using structured JSON output via the Anthropic API. Built a real eval harness, measured on 
real, human-labeled public text: 88.9% accuracy on both category and operational domain 
(macro-F1 0.906 and 0.894), with per-label F1 and a full misclassification log. v2 added a 
BM25 retrieval layer and measured it: the lift was marginal, so I shipped the negative 
result instead of reaching for embeddings.

**[learning-notes](https://github.com/sanlee-ys/learning-notes)** — 
Plain-language notes on the concepts behind these projects — tool use, RAG, evals, 
embeddings, model routing, and how I steer AI agents. Four ways to read them: a searchable 
page, a MkDocs site, an interactive D3 concept map that links each idea to the ones it 
builds on, and kb-agent chat that answers from the notes with citations.

**[claude-ops](https://github.com/sanlee-ys/claude-ops)** — 
The operating layer for the Claude-assisted workflow the rest of this page describes: a 
credential-guard hook hardened across four documented leak incidents in one week, blameless 
postmortems with the failures left in, a pre-commit redline guard, and the working 
agreements that scope each session.

**[architecture](https://github.com/sanlee-ys/architecture)** — 
System-level architecture decisions (ADRs) that span more than one project, plus the system 
portal: a generated MkDocs site that pulls every repo's docs and a roadmap dashboard into 
one place on GitHub Pages.

**[notes-api](https://github.com/sanlee-ys/notes-api)** — 
Python/FastAPI notes REST API with SQLAlchemy; async tag enrichment via BackgroundTasks seam to the defense-news-classifier.

## Day job
In Employee Platforms, responsible for the product lifecycle, migration, and automation of 
enterprise collaboration platforms (SharePoint Online & OneDrive) across all lines of business.

## Stack
**Now:** Python · Anthropic API · AWS · Jira · Microsoft 365  
**Earlier (SWE):** Python · Java · Kafka · event-driven microservices · CockroachDB · Cassandra · MySQL · Kubernetes · Docker · OpenTelemetry

## Background
Seoul National University MBA · B.A. Information Technology, Rutgers–New Brunswick · AWS Certified Cloud Practitioner · U.S. Army National Guard veteran (Qatar, OEF)

Outside work: photography, hiking, and supervised by a Scottish Fold named Sango.

<p align="center"><a href="https://www.linkedin.com/in/leesan/">LinkedIn</a> · <a href="https://www.instagram.com/sanleeeee/">Instagram</a> · <a href="https://vsco.co/sanlee">VSCO</a> · <a href="https://sanlee.me">Portfolio</a></p>

<p align="center">
  <img src="images/sango-boop.jpeg" alt="Sango, a Scottish Fold, asleep" width="240" height="240" />
</p>

<p align="center"><em>Sango, Chief Nap Officer.</em></p>
