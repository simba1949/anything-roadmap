# anything: a systematic learning pipeline

English | [中文](./README.md)

This project is human-centered and uses AI to strengthen human capability. It separates trustworthy research, a public domain map, a personal learning path, and actual tutoring into four independently usable skills with shared contracts:

```text
/anything-research <question>          evidence, sources, disputes, boundaries
        ↓
/anything-domain-map <domain>          a public end-to-end knowledge map
        ↓
/anything-roadmap <learning goal>      a transparent capability path and self-study course
        ↓
/anything-tutor <start|resume|review>  teaching, assessment, remediation, transfer, review
```

## Install

```bash
npx skills add simba1949/anything-roadmap
```

The repository contains four skills; the command above discovers them and opens the selection flow. To install all four skills into Codex:

```bash
npx skills add simba1949/anything-roadmap --global --all --agent codex
```

To install only the personal-path skill into Codex:

```bash
npx skills add simba1949/anything-roadmap --skill anything-roadmap --global --yes --agent codex
```

When working from a local checkout (for development or verification):

```bash
npx skills add . --skill anything-roadmap --global --copy --yes --agent codex
```

`--global` installs to the user-level skill directory; omit it for a project-local installation. For manual installation, copy the required directories under `skills/` into your agent's skill directory.

To remove the single skill installed into Codex:

```bash
npx skills remove anything-roadmap --global --yes --agent codex
```

To remove all four skills installed from this repository (list the names explicitly so skills from other repositories are preserved):

```bash
npx skills remove anything-research anything-domain-map anything-roadmap anything-tutor --global --yes --agent codex
```

Do not treat `--skill '*'` as a repository filter; it matches every skill in the selected scope. Use it only when you intentionally want to remove all global skills from Codex:

```bash
npx skills remove --skill '*' --global --yes --agent codex
```

To update a skill installed from GitHub:

```bash
npx skills update anything-roadmap --global --yes
```

To update all global skills:

```bash
npx skills update --global --yes
```

If the skill was copied from a local checkout, remove the old version first and rerun the local installation command above.

## The four layers

### anything-research

Runs iterative deep research. Later rounds are driven by full-text reading from earlier rounds; important claims are cross-validated; contradictions remain visible; every formal URL is opened and checked. Its domain-cartography mode prepares evidence about boundaries, structure, dependencies, applications, and frontiers.

### anything-domain-map

Builds a learner-independent public map:

```text
module → [topic] → [chapter] → knowledge point
```

Modules and knowledge points are required. Topics and chapters appear only when they form meaningful groups. It outputs:

```text
domain-map.json       machine source of truth
domain-map.md         reviewable end-to-end outline
domain-map.html       offline knowledge observatory
validation.md         source, coverage, and structure checks
```

### anything-roadmap

Shows the public map first, then derives personal capabilities from a graduation task, background, and constraints:

```text
graduation task → success conditions → subtasks → observable capabilities
→ required knowledge → prerequisite capabilities
```

Capabilities are classified as core, support, on-demand branches, or explicitly deferred. One learning-contract checkpoint precedes expensive generation. The result includes modular course content, `self-study.md`, and a `roadmap.html` that overlays the personal path on the complete map.

### anything-tutor

Executes the course and maintains private learning state. Learners can choose attempt-first or instruction-first teaching. Mastery progresses through evidence:

```text
unassessed → recognition → recall → near transfer → far transfer → retained
```

Feedback distinguishes knowledge gaps, misconceptions, procedural failures, omitted conditions, transfer failures, and flawed tasks or grading. Stronger hints produce weaker evidence. A course defect is never recorded as a learner failure.

## Data and privacy

The public map and personal path remain separate sources of truth while appearing in one interface:

```text
domain-map.json + learning-path.json → roadmap.html
```

Private learning state lives in a separate workspace:

```text
learner-state.json
evidence.jsonl
progress.md
```

Only structured evidence summaries are retained by default, not complete conversations.

## Deterministic tooling

The skills include repeatable validators, offline renderers, and a learner-state tool. See each `SKILL.md` for commands and [CONSENSUS.md](./CONSENSUS.md) for the complete design rationale and acceptance criteria.

## License

MIT
