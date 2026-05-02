# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a reference and learning repository for building **Claude Skills** — Anthropic's framework for packaging modular, reusable AI expertise. It contains no executable code, build pipeline, or tests. The two markdown guides are the primary artifacts.

## Content Overview

| File               | Description                                                                                                              |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| `claude-skills.md` | Narrative expert guide: skill lifecycle, patterns, MCP integration, deployment, troubleshooting (~825 lines)             |
| `Skills Guide.md`  | Structured 6-chapter reference: planning, testing, distribution, patterns, resources, YAML frontmatter spec (~862 lines) |

These are complementary documents — `claude-skills.md` provides depth and real-world context; `Skills Guide.md` provides structured prescriptive guidance with checklists.

## Skill Architecture (Key Reference)

A Claude Skill lives in a named folder with a `SKILL.md` file:

```tree
my-skill/
├── SKILL.md          # Required: YAML frontmatter + markdown body
├── examples/         # Optional: usage examples
└── tools/            # Optional: tool definitions
```

**SKILL.md frontmatter fields** (from `Skills Guide.md`):

- `name`, `description`, `version`, `author`
- `trigger` — when the skill activates
- `tools` — MCP tools or built-ins it uses
- `dependencies` — other skills it composes

## Skiller — Project Skill

A meta-agent skill lives at `.agents/skills/skiller/` (shared path, discovered by both Claude Code and Codex CLI). `.claude/skills/skiller` is a symlink to the same location for backwards compatibility. It orchestrates multi-step jobs end-to-end: breaks requirements into tasks, finds or builds a skill per task, executes the pipeline, writes output, and logs feedback.

```
.agents/skills/skiller/          # canonical location (symlinked from .claude/skills/skiller)
├── SKILL.md                          # Main orchestrator — 8-phase workflow
├── agents/
│   ├── task-planner.md               # Decomposes requirement into 1–12 tasks
│   ├── skill-researcher.md           # Finds skills: local → skills.sh → web
│   ├── feedback-collector.md         # Generates ≤5 post-job feedback questions
│   └── openai.yaml                   # Codex UI hints (display name, trigger, icon)
├── references/
│   ├── safety-criteria.md            # 5 mandatory checks before installing a skill
│   └── skill-creator-brief-template.md  # Spec template for commissioning new skills
└── templates/
    ├── wip-task-brief.md             # Per-task handoff file format (wip/ folder)
    └── changelog-entry.md            # Session log format (logs/ folder)
```

**Runtime folders** (created in cwd at invocation):
- `outbox/` — drop files here for Skiller to read; Skiller reads **only** from this folder
- `inbox/` — Skiller writes all final deliverables here for you to read
- `wip/` — inter-task state (do not edit during a session)
- `logs/` — session changelogs

**Dependencies**: requires `find-skills` and `skill-creator` to be installed globally.

**Trigger**: describe a multi-step job — e.g. *"orchestrate a workflow to…"*, *"help me do X end to end"*.

## Permissions

`.claude/settings.local.json` allows `WebFetch` to `skills.sh` domain only — used for referencing the public skills registry.

## Key Concepts Covered

- Skills vs. prompts vs. MCP tools (when to use each)
- Progressive disclosure, modularity, determinism, portability principles
- Multi-step workflows, state management, composable skill dependencies
- Deployment targets: Claude.ai, Claude Code (`~/.claude/skills/`), Anthropic API (`/v1/skills`)
- Distribution via `npx skills add <owner/repo@skill>`
