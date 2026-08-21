# anything-roadmap

English | [中文](./README.md)

An agent skill that generates a systematic learning roadmap for any domain: it researches **real prior learning paths** as the skeleton, then searches and **opens and verifies every source link one by one** (official docs / blogs / videos / sites), and delivers Markdown + a self-contained interactive HTML "knowledge star chart".

## Install

```bash
npx skills add simba1949/anything-roadmap
```

Or manually: copy `SKILL.md` and `references/` from the repo root into your agent's skills directory (e.g. `~/.claude/skills/anything-roadmap/` for Claude Code).

## What it does

Invoke `/anything-roadmap <domain> [one-line background]` (defaults to zero-basics when background is omitted) and get, in one run:

1. **Prior-path research**: official learning paths, university syllabi, awesome lists, high-signal personal roadmaps, and community consensus, ranked by a credibility ladder; if fewer than 2 credible paths exist for a niche domain, it degrades to an official-docs-structure backbone and declares so explicitly.
2. **Four-level outline**: module → topic → chapter → knowledge point, split by knowledge cohesion, with a global map and inter-module relations.
3. **Verified sources**: at most 3 sources per knowledge point, ~40 per roadmap; English authorities as the backbone, Chinese tutorials as scaffolding; every included link is actually opened and must pass three checks (alive / on-topic / authoritative) — zero tolerance for dead or hallucinated links, with a verification summary at the end.
4. **Dual-format output**: `syllabus.md` + a single-file self-contained `index.html` (dark knowledge star chart: modules as stars, relations as lines, four-level collapsible drill-down, media-type filtering, zero CDN, works offline).
5. **Methodology export**: `references/playbook.md` can be pasted whole into tool-less AIs such as ChatGPT or claude.ai (with an explicit verification-degradation notice).

## Design principles

- Run to completion: no mid-run questions; corrections come after the deliverable
- Correction = full re-run: never patches the old draft
- One-shot snapshot: no incremental refresh; regenerate when sources age

## Dependencies

None required. The search layer reuses any installed search skill (e.g. agent-reach) first and falls back to built-in WebSearch/WebFetch; link verification chains three readers (Jina Reader → web_reader → WebFetch) — any one being available is enough.

## License

[MIT](./LICENSE)
