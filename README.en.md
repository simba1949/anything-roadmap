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
npx skills add simba1949/anything-roadmap --global --all --agent codex
```

Update the four skills from this repository (other skills are not affected):

```bash
npx skills update anything-research anything-domain-map anything-roadmap anything-tutor --global --yes
```

Remove the four skills from this repository:

```bash
npx skills remove anything-research anything-domain-map anything-roadmap anything-tutor --global --yes --agent codex
```

All commands above target only the four skills in this repository. They do not use wildcards and do not affect other skills.

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

One learning project uses one top-level directory. Each skill owns a clearly named subdirectory:

```text
<project-slug>-learning/
├─ anything-research/      research dossier and report
├─ anything-domain-map/    public knowledge map
├─ anything-roadmap/       personal path and course package
└─ anything-tutor/         private learner state
```

The public map and personal path remain separate sources of truth and are combined in `anything-roadmap/roadmap.html`. `anything-tutor/` shares the project tree but remains a separate privacy boundary. Treat the project root as private by default and exclude the tutor directory from public exports. Only structured evidence summaries are retained, not complete conversations.

## Deterministic tooling

The skills include repeatable validators, offline renderers, and a learner-state tool. See each `SKILL.md` for commands and [CONSENSUS.md](./CONSENSUS.md) for the complete design rationale and acceptance criteria.

## License

MIT
