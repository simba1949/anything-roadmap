# anything-research + anything-roadmap

English | [中文](./README.md)

A **two-stage pipeline** from deep research to a systematic learning roadmap — two independently usable agent skills, installed together:

```
/anything-research <question>        ← deep-research engine
      ↓ research.md (research dossier)
/anything-roadmap <domain> [background]  ← systematic teaching syllabus
      ↓ roadmap.md + roadmap.html (+ research.md)
(future stage 3: a systematic-teaching skill)
```

## Install

```bash
npx skills add simba1949/anything-roadmap
```

Installs both skills at once (multi-skill repo layout). Or manually: copy the `skills/anything-research/` and `skills/anything-roadmap/` folders into your agent's skills directory (e.g. `~/.claude/skills/` for Claude Code).

## anything-research — deep-research engine

Runs multi-round iterative research on any question (technology selection, market research, due diligence, fact-checking, background checks) and produces an evidence-chained dossier `research.md`. Four depth standards:

1. **Iterative** — each later round is driven by new leads surfaced by reading the previous round; every round is logged in an iteration trace;
2. **Cross-validated** — key claims need ≥2 independent sources; single-source claims are explicitly flagged;
3. **Full-text reading** — conclusions come from opened full documents, never from search snippets;
4. **Contradiction-preserving** — conflicting information is never smoothed over; a "Disagreements & Contradictions" section pits each view against its strongest evidence.

Layered architecture: process engine (this skill: when to search, what to ask, when to stop) → probe-and-reuse installed search skills (e.g. agent-reach) → fall back to built-in WebSearch/WebFetch. Three stop gates: round cap + diminishing-returns stop + source budget; three depth presets (light 2 rounds / medium 4 / deep 6) plus `rounds=N` custom.

The dossier contains: key findings (claim | confidence | evidence table), disagreements & contradictions, information gaps, iteration trace, tiered source list, and five teaching-oriented fields.

## anything-roadmap — systematic learning-roadmap generator

Invoke `/anything-roadmap <domain> [one-line background]` (defaults to zero-basics) to generate a four-level outline (module → topic → chapter → knowledge point):

1. **Dossier detection**: reuses a same-domain research.md from the last 7 days if present; otherwise invokes anything-research in teaching-five-questions mode (the dossier becomes the third artifact); falls back to self-conducted prior-path research when neither is available.
2. **Outline rules**: prior learning paths as the backbone (credibility ladder), split by knowledge cohesion, global map + inter-module relations, exercises per module; no timetables, no assessment gates.
3. **Verified sources**: ≤3 sources per knowledge point, ~40 per roadmap; English authorities as backbone, Chinese tutorials as scaffolding; every included link is actually opened and verified (alive / on-topic / authoritative) — zero hallucinated links, with a verification summary.
4. **Artifacts**: `roadmap.md` + self-contained interactive `roadmap.html` (dark territory-map: modules as lands, relations as routes, four-level drill-down, media filtering, anchor jumps, zero CDN, works offline).
5. **Methodology export**: `skills/anything-roadmap/references/playbook.md` can be pasted into tool-less AIs (with an explicit verification-degradation notice).

## Shared design principles

- Run to completion: no mid-run questions; corrections = full re-run, never patches.
- One-shot snapshot: no incremental refresh; regenerate when sources age.
- Soft dependencies: anything-research / agent-reach / web_reader are all probe-then-use — auto-degrade when absent, never brick.
- Honest delivery: verification stats, information gaps, and contradictions are all surfaced explicitly.

## License

MIT
