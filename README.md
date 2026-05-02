# learn-ai

A reference and learning repository for building **Claude Skills** — Anthropic's framework for packaging modular, reusable AI expertise into portable, self-contained skill folders.

## Docs

| File | Description |
|------|-------------|
| [Juan's Playbook to Skills](docs/Juan's%20Playbook%20to%20Skills.md) | Narrative expert guide covering the full skill lifecycle: why skills exist, how they work, how to build and test them, and ready-made templates. Written as an opinionated playbook with real-world context and practical patterns (~825 lines). |
| [Skills - Notes from Official Guide](docs/Skills%20-%20Notes%20from%20Official%20Guide.md) | Structured 6-chapter reference distilled from official Anthropic documentation. Covers fundamentals, planning, testing, distribution, patterns & troubleshooting, and a resources index. Includes YAML frontmatter spec and development checklists (~862 lines). |

## Skills Included

| Skill | Description |
|-------|-------------|
| [`skill-creator`](.agents/skills/skill-creator/) | Interactive guide that helps you build new skills — runs evals, benchmarks, and packages the result. |
| [`skiller`](.agents/skills/skiller/) | Meta-agent that orchestrates multi-step jobs end-to-end: breaks requirements into tasks, finds or builds a skill per task, and executes the pipeline. |

## Repo Layout

```
docs/               # Learning guides (see table above)
.agents/skills/     # Installed skills (canonical location)
.claude/skills/     # Symlinks → .agents/skills/ (Claude Code discovery)
skills-lock.json    # Installed skill registry
```

## License

[MIT](LICENSE)
