# The Claude Skills Playbook

> 🛑 Stop re-prompting. Package your domain expertise into a skill once, and Claude applies it consistently every time - without setup, without reminders.

**Claude Skills** are modular, self-contained packages that give Claude persistent, structured expertise through a simple folder format. A skill is a set of instructions that tells Claude how to handle specific tasks or workflows. The architecture loads only what's needed, when it's needed, minimizing context overhead. For MCP builders, skills provide the workflow layer that transforms tool access into reliable outcomes.

> 🥋 Think of Skills the app The Matrix' Neo downloaded to his brain to learn Kung Fu (whoa!). Skills are the Kung Fu of AI agents. They give Claude the ability to perform specific tasks with precision and reliability, without needing to re-teach it every time.

## Table of Contents

1. [Part 1 - The Case for Skills](#part-1---the-case-for-skills)
2. [Part 2 - How Skills Work](#part-2---how-skills-work)
3. [Part 3 - Building a Skill](#part-3---building-a-skill)
4. [Part 4 - Testing & Shipping](#part-4---testing--shipping)
5. [Part 5 - Ready-Made Resources](#part-5---ready-made-resources)

**Appendices:** [A: Development Checklist](#a-development-checklist) - [B: YAML Frontmatter Reference](#b-yaml-frontmatter-reference) - [C: Key Takeaways](#c-key-takeaways) - [D: Resources](#d-resources) - [E: Starter Templates by Persona](#e-starter-templates-by-persona)

---

## Part 1 - The Case for Skills

### 1. Why Skills Exist

Traditional prompt engineering breaks down at scale. Four specific problems:

1. **Duplication** - The same instructions must be pasted across multiple agents, chats, or API calls. Any update requires manual propagation.
2. **Context waste** - System prompts load everything, even instructions for tasks the user never requests, burning Claude's context window.
3. **Maintenance** - As prompts grow to hundreds of lines they become hard to version, test, and update. Conflicts between instructions are common.
4. **No code integration** - Traditional prompts can't include executable scripts, so Claude must "imagine" deterministic tasks rather than running reliable code.

> The cost is measurable: community estimates suggest the average Claude user spends **10-15 minutes per day** just re-establishing context - over an hour a week telling the AI things it should already know. Skills eliminate that tax entirely.

Skills solve all four by structuring AI expertise into modular, version-controlled, on-demand packages.

| Aspect        | Traditional Prompts | Claude Skills    |
| ------------- | ------------------- | ---------------- |
| Structure     | Flat text           | Organized folder |
| Loading       | Always loaded       | On-demand        |
| Code          | No execution        | Scripts included |
| Sharing       | Copy-paste          | Share folder     |
| Versioning    | Manual              | Git-friendly     |
| Testing       | Ad-hoc              | Systematic       |
| Composability | Difficult           | Built-in         |

### 2. Skills in Practice

What skills genuinely solve, from the community on [r/ClaudeAI](https://www.reddit.com/r/ClaudeAI/), [r/ChatGPTCoding](https://www.reddit.com/r/ChatGPTCoding/), [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/), and [r/ExperiencedDevs](https://www.reddit.com/r/ExperiencedDevs/):

- **Procedure reuse.** A tested recipe in a `SKILL.md` beats copy-pasting prompts across chats.
- **Scoped context loading.** Loading only the reference files needed for a task keeps context windows under control. [Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) amplifies the win.
- **Team standardization.** Shared skills turn tribal knowledge into version-controlled assets.
- **Testability.** A skill can be tested the way code is tested - with tools like [promptfoo](https://www.promptfoo.dev/), [Braintrust](https://www.braintrust.dev/), and [Langfuse](https://langfuse.com/).

Common gotchas:

- **Skills are not magic.** A badly written skill is a badly written prompt with extra ceremony.
- **Discovery is underrated.** If Claude doesn't know which skill to invoke, the skill is dead weight. Clear names, clear descriptions, explicit triggers.
- **Versioning discipline.** Skills drift. Without versioning, teams end up debugging "which skill did that" weeks later.
- **Over-abstraction hurts.** Build five working skills before extracting patterns.
- **Security matters.** Skills that load external references are a prompt injection surface. See [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

What practitioners actually do:

- Start with 3-5 high-value, already-prompt-stable tasks; convert those first.
- Treat `SKILL.md` like a README - if a teammate can't read it and understand when to use it, rewrite it.
- Version-control skills alongside code; they follow the same review process.
- Log when skills are used and what outputs they produce - [LangSmith](https://www.langchain.com/langsmith) and [Helicone](https://www.helicone.ai/) make this tractable.
- Graduate skills to [sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents) when the workflow needs tool access beyond plain prompting.

---

## Part 2 - How Skills Work

### 1. Architecture

Every skill is a named folder with one required file and optional subdirectories:

```tree
📁 skill-name/
├── `SKILL.md`                  ← Required: YAML frontmatter + Markdown instructions
├── scripts/                    ← Optional: Executable code (Python, Bash, etc.)
│   ├── process_data.py
│   └── validate.sh
├── references/                 ← Optional: Docs, guides, examples  -  loaded on demand
│   ├── api-guide.md
│   └── examples/
└── assets/                     ← Optional: Templates, fonts, icons
    └── report-template.md
```

| Component     | Purpose                              | When Loaded             | Required |
| ------------- | ------------------------------------ | ----------------------- | -------- |
| `SKILL.md`    | Core instructions + trigger metadata | When skill is activated | Yes      |
| `scripts/`    | Executable Python/Bash code          | Called during execution | No       |
| `references/` | Documentation & guidelines           | On-demand when needed   | No       |
| `assets/`     | Icons, images, templates             | When referenced         | No       |

**Critical naming rules:**

- Folder: kebab-case only (e.g., `my-skill-name`). No spaces, underscores, or capitals.
- `SKILL.md`: exact case, exact spelling. `SKILL.MD` and `skill.md` both fail.
- No `README.md` inside the skill folder - all docs go in `SKILL.md` or `references/`.

### 2. Core Principles

**Progressive disclosure** reduces token usage by 70-90% compared to loading all instructions in the system prompt. It works in three levels:

1. **YAML frontmatter**: Always in Claude's context. Claude scans descriptions to know when to load a skill.
2. **`SKILL.md` body**: Loads when Claude judges the skill relevant. Contains full instructions.
3. **Linked files**: `references/` and `scripts/` load only on demand during execution.

A project with 20 skills doesn't waste tokens loading all 20; only the relevant ones activate.

To put a concrete number on it: each skill's metadata layer costs roughly **100 tokens** (community estimate). Having 50 skills installed adds only ~5,000 tokens to Claude's context - negligible compared to the workflow overhead it replaces.

**Composability** - skills are designed to work together. Claude automatically identifies and sequences the skills needed:

```text
User: "Create a quarterly report for Q4 with brand formatting and send it to leadership"

Claude activates:
  1. data-analysis skill     → Pulls and analyzes Q4 metrics
  2. brand-writing skill     → Applies brand voice
  3. report-template skill   → Formats as quarterly report
  4. email-composer skill    → Drafts email to leadership
```

**Determinism through scripts** - for tasks requiring 100% reliability, include executable scripts rather than relying on Claude's interpretation:

```python
# scripts/format_currency.py
def format_currency(amount):
    return f"${amount:,.2f}"
```

**Portability** - the same skill works across all Claude surfaces: [Claude.ai](https://claude.ai) Projects, Claude Code (`.claude/skills/`), and the Anthropic API.

### 3. Skills + Model Context Protocol (MCP)

MCP and skills are complementary, not competing:

> MCP = the kitchen (tools, ingredients, equipment). Skills = the recipes.

|          | MCP (Connectivity)                                     | Skills (Knowledge)                                   |
| -------- | ------------------------------------------------------ | ---------------------------------------------------- |
| Purpose  | Connects Claude to services (Notion, Asana, Linear...) | Teaches Claude how to use those services effectively |
| Function | Provides real-time data access and tool invocation     | Captures workflows and best practices                |
| Scope    | What Claude _can_ do                                   | How Claude _should_ do it                            |

**The difference in practice:**

|                             | MCP without Skills                                   | MCP with Skills                                        |
| --------------------------- | ---------------------------------------------------- | ------------------------------------------------------ |
| User experience             | Users have tools but figure out workflows themselves | Guided workflows that automatically leverage MCP tools |
| Outcomes                    | Inconsistent results, frustration, support tickets   | Reliable, consistent outcomes with less user effort    |
| Support burden              | High ("how do I do X with your integration?")        | Low - skill guidance reduces need to ask               |
| Competitive differentiation | Just a connector; easily replicated                  | Unique value layer tied to embedded expertise          |

**Example - capabilities:**

| Capability    | MCP (Model Context Protocol)  | Claude Skills                                       |
| ------------- | ----------------------------- | --------------------------------------------------- |
| Role          | Provides external connections | Provides procedural knowledge                       |
| Database      | Queries, reads, writes        | Decides when/what to query, processes results       |
| APIs          | HTTP calls, authentication    | Knows which API to call, formats requests           |
| File System   | Read/write files              | Determines which files to process, generates output |
| Composability | Plug-and-play tools           | Orchestrates tools into workflows                   |

### 4. Skills vs. Custom Instructions

Custom Instructions and Skills both shape Claude's behavior, but they operate differently:

|             | Custom Instructions                | Claude Skills                                                                       |
| ----------- | ---------------------------------- | ----------------------------------------------------------------------------------- |
| Scope       | Always active - every conversation | Dynamic - activates only when relevant                                              |
| Granularity | Broad preferences for everything   | Task-specific procedures                                                            |
| Example     | "Always respond in bullet points"  | "When reviewing TypeScript, check for type safety, error handling, and performance" |
| Limitation  | One set of rules for all contexts  | Each skill targets its own context                                                  |

**The practical problem Custom Instructions can't solve:** you can't tell Claude "when I'm writing a newsletter, follow these 47 formatting rules - but when I'm reviewing code, switch to a completely different workflow." Custom Instructions are a blunt instrument. Skills give you the precision.

**Use them together:** Custom Instructions handle universal preferences. Skills handle specialized workflows. They don't compete.

**Example - customer support skill with MCP:**

```markdown
## Process

1. Extract customer ID from the ticket
2. [MCP: database] Query customer account: SELECT \* FROM customers WHERE id = {customer_id}
3. [MCP: api] Check order status: GET /api/orders?customer={customer_id}&status=active
4. Analyze against references/common_issues.md
5. Draft response using references/response_templates.md
6. [MCP: email] Send drafted response to customer
```

---

## Part 3 - Building a Skill

### 1. Planning & Design

Good skills are designed, not written. Quality of design determines quality of the skill.

**Workflow:**

1. **Define 2-3 concrete use cases** before writing a single line.

   ```markdown
   Use Case: Project Sprint Planning
   Trigger: User says "help me plan this sprint" / "create sprint tasks"
   Steps:

   1. Fetch current project status from Linear (via MCP)
   2. Analyze team velocity and capacity
   3. Suggest task prioritization
   4. Create tasks in Linear with proper labels and estimates
      Result: Fully planned sprint with tasks created
   ```

2. **Answer four key design questions:**
   - _What does a user want to accomplish?_ → Description
   - _When should it be activated?_ → Description
   - _What inputs and outputs are involved?_ → Workflow
   - _What outputs should it produce?_ → Workflow
   - _What multi-step workflows does this require?_ → Workflow
   - _Are there deterministic steps that should use scripts?_ → Scripts
   - _Which tools are needed (built-in or MCP)?_ → Tools, Scripts, or MCP
   - _What domain knowledge or best practices should be embedded?_ → References

**Three common skill categories:**

1. **Document & asset creation** - Consistent, high-quality output (documents, presentations, code). **Techniques**: embedded style guides, template structures, quality checklists. No external tools required. **Examples**: [frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design), [docx, pptx, xlsx](https://github.com/anthropics/skills/tree/main/skills).

2. **Workflow automation** - Multi-step processes benefiting from consistent methodology. **Techniques**: step-by-step workflow with validation gates, iterative refinement loops. **Example**: [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator).

3. **MCP enhancement** - Guidance layered on top of MCP tool access. **Techniques**: coordinate multiple MCP calls in sequence, embed domain expertise, handle common MCP errors. **Example**: [GitHub PR analysis with Sentry](https://github.com/getsentry/sentry-for-claude/tree/main/skills/sentry-code-review).

**Quick-start alternative:** You don't need to write a `SKILL.md` from scratch. Just describe what you want to Claude directly in conversation:

> "Create a Skill that formats all my code reviews with these sections: Summary, Critical Issues, Suggestions, and Praise. It should focus on readability and always check for error handling. Save it as a `SKILL.md` file."

Claude will generate a properly structured `SKILL.md`, create the folder, and save it - no coding required. Once it exists, review and refine the output before treating it as production-ready.

**Define success criteria upfront:**

**Quantitative**: Skill triggers on 90%+ of relevant queries (test with 10-20); completes workflow in a target number of tool calls; 0 failed API calls per workflow; response under a target time.

**Qualitative**: Users don't need to prompt Claude about next steps; workflows complete without correction; consistent results across sessions; new users succeed on first try.

### 7. Writing `SKILL.md`

#### YAML Frontmatter

The frontmatter is the most critical part - it determines whether Claude loads the skill at all.

```yaml
---
name: skill-name # Required: kebab-case only
description: What it does. Use when... # Required: what + when + trigger phrases
license: MIT # Optional
allowed-tools: "Bash(python:*) WebFetch" # Optional: restricts tool access
metadata: # Optional: custom key-value pairs
  author: Company Name
  version: 1.0.0
  mcp-server: server-name
  category: productivity
  tags: [project-management, automation]
---
```

**Field rules:**

| Field           | Required | Rules                                                                                                                 |
| --------------- | -------- | --------------------------------------------------------------------------------------------------------------------- |
| `name`          | Yes      | <64 chars, kebab-case, no spaces, no capitals, matches folder name, cannot be "claude" or "anthropic"                 |
| `description`   | Yes      | <1024 chars; must include what it does AND when to use it; no XML tags (`<` or `>`); include specific trigger phrases |
| `license`       | No       | e.g., MIT, Apache-2.0                                                                                                 |
| `allowed-tools` | No       | <500 chars; restricts which tools the skill can invoke                                                                |
| `metadata`      | No       | Any custom key-value pair, e.g. author, version, mcp-server                                                           |

**Extended frontmatter fields (Claude Code):**

| Field                      | Purpose                                            | Example                            |
| -------------------------- | -------------------------------------------------- | ---------------------------------- |
| `model`                    | Override the default model for this skill          | `model: opus`                      |
| `effort`                   | Set reasoning depth (low/medium/high/max)          | `effort: high`                     |
| `context: fork`            | Run skill in an isolated subagent context          | `context: fork`                    |
| `user-invocable: false`    | Background-only; removes slash command             | `user-invocable: false`            |
| `paths`                    | Auto-activate when matching file patterns are open | `paths: "**/*.test.ts"`            |
| `disable-model-invocation` | Skill can only be triggered manually, never auto   | `disable-model-invocation: true`   |
| `argument-hint`            | Hint text shown in autocomplete dropdown           | `argument-hint: "Pass the PR URL"` |
| `hooks`                    | Shell scripts that run at lifecycle points         | `hooks: {pre: validate.sh}`        |

> The `paths` field is especially powerful for developer skills: a TypeScript review skill with `paths: "**/*.ts"` auto-activates whenever a TypeScript file is open - no slash command required.

**Security rules:**

- Allowed: standard YAML types (strings, numbers, booleans, lists, objects), custom metadata, long descriptions
- Forbidden: XML angle brackets (`<` or `>`) - frontmatter is injected into Claude's system prompt; code execution in YAML; names prefixed with "claude" or "anthropic"

#### Writing Effective Descriptions

> "Provides enough information for Claude to know when each skill should be used without loading all of it into context." - [Anthropic Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

Structure: **[What it does] + [When to use it] + [Key capabilities]**

Good examples:

```text
Analyzes Figma design files and generates developer handoff documentation. Use when
user uploads .fig files, asks for "design specs", "component documentation", or
"design-to-code handoff".

Manages Linear project workflows including sprint planning, task creation, and status
tracking. Use when user mentions "sprint", "Linear tasks", "project planning", or asks
to "create tickets".
```

Bad examples:

```text
Helps with projects.                                        ← Too vague
Creates sophisticated multi-page documentation systems.     ← Missing triggers
Implements the Project entity model with hierarchical...    ← Too technical
```

#### `SKILL.md` Body Template

```markdown
---
name: your-skill
description: [What it does] + [When to use it] + [Key capabilities]
metadata:
  version: 1.0.0
---

# Your Skill Name

## Instructions

### Step 1: [First Major Step]

Clear explanation of what happens.

Example:
python scripts/fetch_data.py --project-id PROJECT_ID

Expected output: [describe what success looks like]

## Examples

### Example 1: [common scenario]

User says: "Set up a new marketing campaign"
Actions:

1. Fetch existing campaigns via MCP
2. Create new campaign with provided parameters
   Result: Campaign created with confirmation link

## Troubleshooting

Error: [Common error message]
Cause: [Why it happens]
Solution: [How to fix]
```

### 8. Step-by-Step Walkthrough

**Meeting Summarizer** - a complete worked example.

**Step 1 - Define the use case:**

- Task: Summarize meeting transcripts into structured action items, decisions, follow-ups
- Trigger: User provides a meeting transcript, recording summary, or meeting notes
- Inputs: transcript text
- Outputs: executive summary, decisions list, action items table, open questions
- Deterministic parts: topic extraction → use a script

**Step 2 - Create the folder:**

```bash
mkdir -p .claude/skills/meeting-summarizer/{scripts,references}
```

**Step 3 - Write `SKILL.md`:**

```markdown
---
name: meeting-summarizer
description: |
  Summarize meeting transcripts into structured action items, decisions, and
  follow-ups. Use when the user provides a meeting transcript, recording
  summary, or meeting notes.
---

# Meeting Summarizer

## Process

1. Parse the transcript - identify speakers, timestamps, topics
2. Run scripts/extract_topics.py to identify main discussion areas
3. For each topic, extract: key points, decisions (with owners), action items (with owners and deadlines), open questions
4. Format output using references/summary_template.md
5. Highlight any action items without clear owners

## Output Format

- Executive summary (2-3 sentences)
- Decisions list (numbered)
- Action items table (who / what / when)
- Open questions list
- Next meeting suggestions

## Constraints

- Never invent information not in the transcript
- Flag unclear speaker attribution
- If deadlines are mentioned ambiguously, note the ambiguity
```

**Step 4 - Add scripts (optional):**

```python
# scripts/extract_topics.py
"""Extract main topics from a meeting transcript."""
import sys

def extract_topics(transcript):
    topics = []
    paragraphs = transcript.split('\n\n')
    for p in paragraphs:
        if any(kw in p.lower() for kw in
               ['next topic', 'moving on', "let's discuss", 'agenda item', 'regarding']):
            topics.append(p.strip()[:100])
    return topics

if __name__ == "__main__":
    transcript = sys.stdin.read()
    for i, topic in enumerate(extract_topics(transcript), 1):
        print(f"{i}. {topic}")
```

**Step 5 - Add references (optional):**

```markdown
<!-- references/summary_template.md -->

# Meeting Summary: [TITLE]

**Date:** [DATE] | **Duration:** [DURATION] | **Attendees:** [LIST]

## Executive Summary

[2-3 sentence overview]

## Decisions Made

1. [Decision] - Decided by [WHO]

## Action Items

| Owner  | Task   | Deadline | Status  |
| ------ | ------ | -------- | ------- |
| [Name] | [Task] | [Date]   | Pending |

## Open Questions

- [Question]
```

**Step 6 - Test:**

1. Trigger accuracy - does the skill activate for correct requests?
2. No false triggers - does it stay inactive for unrelated requests?
3. No hallucinations - does Claude follow instructions exactly?
4. Script execution - do scripts run correctly?
5. Edge cases - what happens with incomplete or unusual input?

### 9. Advanced Patterns

**Pattern framing - two modes:**

|               | User Says                              | Skill Does                                     |
| ------------- | -------------------------------------- | ---------------------------------------------- |
| Problem-first | "I need to set up a project workspace" | Orchestrates the right MCP calls in sequence   |
| Tool-first    | "I have Notion MCP connected"          | Teaches Claude optimal workflows for that tool |

---

#### Pattern 1: Sequential Workflow Orchestration

Use when users need multi-step processes in a specific order. Key techniques: explicit step ordering, dependencies between steps, validation at each stage, rollback instructions.

```markdown
## Workflow: Onboard New Customer

### Step 1: Create Account

Call MCP tool: create_customer
Parameters: name, email, company

### Step 2: Setup Payment

Call MCP tool: setup_payment_method
Wait for: payment method verification

### Step 3: Create Subscription

Call MCP tool: create_subscription
Parameters: plan_id, customer_id (from Step 1)

### Step 4: Send Welcome Email

Call MCP tool: send_email
Template: welcome_email_template
```

---

#### Pattern 2: Multi-MCP Coordination

Use when workflows span multiple services. Key techniques: clear phase separation, data passing between MCPs, centralized error handling.

```markdown
### Phase 1: Design Export (Figma MCP)

1. Export design assets from Figma
2. Generate design specifications

### Phase 2: Asset Storage (Drive MCP)

1. Create project folder; upload all assets; generate links

### Phase 3: Task Creation (Linear MCP)

1. Create development tasks; attach asset links

### Phase 4: Notification (Slack MCP)

1. Post handoff summary to #engineering
```

---

#### Pattern 3: Iterative Refinement

Use when output quality improves with iteration. Key techniques: explicit quality criteria, validation scripts, defined stopping condition.

```markdown
### Initial Draft

1. Fetch data via MCP; generate first draft; save to temp file

### Quality Check

1. Run scripts/check_report.py
2. Identify: missing sections, formatting issues, data errors

### Refinement Loop

1. Address each issue; regenerate affected sections; re-validate
2. Repeat until quality threshold met
```

---

#### Pattern 4: Context-Aware Tool Selection

Use when the same outcome requires different tools depending on context.

```markdown
### Decision Tree

1. Check file type and size
2. Route:
   - Large files (>10MB): cloud storage MCP
   - Collaborative docs: Notion/Docs MCP
   - Code files: GitHub MCP
   - Temporary: local storage

### Provide Context to User

Explain why that storage was chosen
```

---

#### Pattern 5: Domain-Specific Intelligence

Use when the skill adds specialized knowledge beyond tool access.

```markdown
### Before Processing (Compliance Check)

1. Fetch transaction details via MCP
2. Apply compliance rules: sanctions lists, jurisdiction, risk level
3. Document compliance decision

### Processing

IF compliance passed: call payment MCP, apply fraud checks
ELSE: flag for review, create compliance case

### Audit Trail

Log all compliance checks and processing decisions
```

---

**State management** - for skills that track progress across interactions:

```markdown
## State Tracking

After each interaction, update the status file:
scripts/update_status.py --task "[TASK_ID]" --status "[STATUS]"

Always check current state before proceeding:
scripts/get_status.py --task "[TASK_ID]"
```

**Error handling** - for scripts:

```markdown
## Error Handling

If any script fails:

1. Log the error: scripts/log_error.py --error "[MESSAGE]"
2. Inform the user what went wrong
3. Suggest alternative approaches
4. Never proceed with partial or assumed data
```

**Composable skills with dependencies:**

```markdown
---
name: quarterly-report-generator
description: Generate quarterly business reports.
dependencies:
  - data-analysis
  - brand-writing
  - chart-generator
---

## Step 1: Data Collection

Activate the data-analysis skill to process raw metrics.

## Step 2: Visualization

Use the chart-generator skill to create charts.

## Step 3: Writing

Apply the brand-writing skill to the final report text.
```

---

## Part 4 - Testing & Shipping

### 1. Testing

Choose the testing level that matches your quality requirements:

- **Manual testing in Claude.ai** - Run queries directly and observe behavior. Fast iteration, no setup.
- **Scripted testing in Claude Code** - Automate test cases for repeatable validation.
- **Programmatic testing via Skills API** - Build systematic evaluation suites.

**Pro tip:** Iterate on a single challenging task until Claude succeeds, then extract the winning approach into a skill. Once you have a working foundation, expand to multiple test cases.

**Three testing areas:**

1. **Triggering tests:**
   - ✅ Triggers on obvious tasks ("Help me set up a new ProjectHub workspace")
   - ✅ Triggers on paraphrased requests ("I need to create a project in ProjectHub")
   - ❌ Does NOT trigger on unrelated topics ("What's the weather in San Francisco?")

2. **Functional tests:**
   - Valid outputs generated; API calls succeed; error handling works; edge cases covered
   - Example: _Given_ "Q4 Planning" project with 5 task descriptions, _when_ skill executes, _then_ project created, 5 tasks created with correct properties, no API errors.

3. **Performance comparison:**
   - Without skill: user provides instructions each time, 15 back-and-forth messages, 3 failed API calls, 12,000 tokens
   - With skill: automatic workflow, 2 clarifying questions only, 0 failed API calls, 6,000 tokens

**Debugging checklist:**

1. Does the YAML description clearly match the user's request phrasing?
2. Are there any ambiguous steps Claude might interpret differently?
3. Do scripts run correctly outside of Claude? Test independently.
4. Are all referenced files present and up to date?
5. Does this skill conflict with other active skills?
6. Is Claude adding steps or information not present in the skill?

**Iteration signals:**

| Signal           | Symptoms                                                     | Fix                                                  |
| ---------------- | ------------------------------------------------------------ | ---------------------------------------------------- |
| Undertriggering  | Skill doesn't load; users manually enabling it               | Add more keywords and trigger phrases to description |
| Overtriggering   | Loads for irrelevant queries; users disabling it             | Add negative triggers; be more specific              |
| Execution issues | Inconsistent results; API failures; Claude correcting itself | Improve instructions; add error handling             |

### 2. Deployment

> **Where to start:** If you're new to Skills, begin with project-level Skills - place them in `.claude/skills/` inside your repository. They travel with the codebase, work automatically for every team member who clones the repo, and are version-controlled alongside the code they support.

**[Claude.ai](https://www.claude.ai) Projects:**

1. Create a new Project in [Claude.ai](https://www.claude.ai)
2. Upload the skill folder as a ZIP file to the Project's knowledge base.

   **ZIP structure note:** Files must be inside a named subfolder within the ZIP - not at the ZIP root:

   ```tree
   📁 my-skill.zip
     └── my-skill/
          └── `SKILL.md`    ✓ correct
   ```

   ```tree
   📁 my-skill.zip
     └── `SKILL.md`          ✗ will fail with "Could not find SKILL.md"
   ```

3. The skill activates automatically when matching conversations occur

**Claude Code:**

1. Place the skill folder in `.claude/skills/` in your project directory
2. Claude Code discovers and uses skills automatically
3. Scripts execute directly in your development environment

**Anthropic API:**

```python
import anthropic

client = anthropic.Anthropic()

with open('my-skill/SKILL.md', 'r') as f:
    skill_content = f.read()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    system=f"""You have the following skill available:

{skill_content}

Activate this skill when the user's request matches the skill description.
Follow the instructions exactly.""",
    messages=[{"role": "user", "content": "Please review this code..."}]
)
```

**Production best practices:**

1. Version control skills like code - use Git, same review process as code
2. Write tests - trigger accuracy and output quality
3. Monitor activation - log when skills fire to catch false triggers
4. Iterate based on feedback - continuously refine instructions
5. Security review scripts - audit all executable code
6. Document dependencies - note which MCP tools or external services are required

### 3. Distribution

**Sharing methods:**

| Method          | Best For            | How                                                                |
| --------------- | ------------------- | ------------------------------------------------------------------ |
| Git repository  | Teams, open-source  | Push skill folder to Git; clone to use                             |
| ZIP archive     | Quick sharing       | Zip folder; import into [Claude.ai](https://www.claude.ai) Project |
| API upload      | CI/CD pipelines     | Use `/v1/skills` endpoint                                          |
| npm/pip package | Developer ecosystem | Package with existing tooling                                      |

**Recommended approach for MCP builders:**

1. Host on GitHub - public repo, clear README with install instructions (outside the skill folder), example usage
2. Link from your MCP repo documentation - explain the value of using both together, provide quick-start guide
3. Installation guide: `git clone`, upload to [Claude.ai](https://www.claude.ai) via Settings > Skills, enable and connect MCP server, test

**Versioning:**

- Use semantic versioning (1.0.0 → 1.1.0 → 2.0.0)
- Maintain a `CHANGELOG.md` documenting changes between versions
- Test trigger accuracy after every update - even small wording changes affect activation

**Positioning - outcomes, not features:**

- **Good:** "The ProjectHub skill sets up complete project workspaces in seconds - pages, databases, and templates - instead of 30 minutes of manual setup."
- **Bad:** "The ProjectHub skill is a folder containing YAML frontmatter and Markdown instructions that calls our MCP server tools."

**Organization-level deployment** (since December 2025): Admins can deploy skills workspace-wide with automatic updates and centralized management.

### 4. Skills API

For programmatic skill management, Anthropic provides a REST endpoint:

```python
import requests

BASE = "https://api.anthropic.com/v1/skills"
HEADERS = {"x-api-key": "your-api-key", "anthropic-version": "2026-01-29"}

# Create
response = requests.post(BASE, headers=HEADERS, json={
    "name": "data-analyzer",
    "description": "Analyze CSV datasets and produce summary reports",
    "content": open("SKILL.md").read(),
    "version": "1.0.0"
})

# List
skills = requests.get(BASE, headers=HEADERS)

# Read
skill = requests.get(f"{BASE}/data-analyzer", headers=HEADERS)

# Update
response = requests.put(f"{BASE}/data-analyzer", headers=HEADERS, json={
    "content": open("SKILL_v2.md").read(),
    "version": "2.0.0"
})

# Delete
requests.delete(f"{BASE}/data-analyzer", headers=HEADERS)
```

The API supports Create, List, Read, Update, and Delete. Key notes:

- Skills in the API require the Code Execution Tool beta
- Add skills to Messages API requests via the `container.skills` parameter
- Works with the Claude Agent SDK for building custom agents

**When to use API vs. Claude.ai:**

| Use Case                                   | Best Surface            |
| ------------------------------------------ | ----------------------- |
| End users interacting with skills directly | Claude.ai / Claude Code |
| Manual testing during development          | Claude.ai / Claude Code |
| Applications using skills programmatically | API                     |
| Production deployments at scale            | API                     |
| Automated pipelines and agent systems      | API                     |

---

## Part 5 - Ready-Made Resources

### 1. Pre-Built Skills

Anthropic provides pre-built document skills available on Pro, Max, Team, and Enterprise plans:

| Skill                | What It Does                               |
| -------------------- | ------------------------------------------ |
| Excel Creator        | Generates and edits `.xlsx` spreadsheets   |
| PowerPoint Builder   | Creates `.pptx` presentations with layouts |
| Word Document Editor | Generates and modifies `.docx` files       |
| PDF Form Filler      | Extracts form fields and fills PDF forms   |

These use the Code Execution Tool internally (e.g., the PDF skill runs a small Python script to extract form field definitions). They demonstrate best practices: clean `SKILL.md` structure, targeted script usage, and graceful error handling.

Community and partner skills are available at:

- [github.com/anthropics/skills](https://github.com/anthropics/skills) - Anthropic-created skills
- [claude.com/connectors](https://www.claude.com/connectors) - Partner skills (Asana, Atlassian, Canva, Figma, Sentry, Zapier, and more)
- [agentskills.io](https://agentskills.io) - Open standard registry (portable across platforms). Published in late 2025 as a universal format any AI system can adopt - the Skills equivalent of what MCP did for tool connectivity in 2024. Any skill there works in Claude.ai, Claude Code, and the API without modification.

### 1b. Claude Code Built-In Skills

If you use Claude Code, five slash-command skills are available out of the box with no setup required:

| Skill         | Command       | What It Does                                                                                                                   |
| ------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Batch         | `/batch`      | Spawns 5-30 agents in separate git worktrees for parallel large-scale codebase changes - migrations, refactors, global renames |
| API Reference | `/claude-api` | Loads the complete API reference for your programming language directly into context; replaces doc-searching                   |
| Debug         | `/debug`      | Enables debug logging so you can see exactly what Claude is doing during execution                                             |
| Loop          | `/loop`       | Runs a prompt on a recurring interval - useful for monitoring, polling, or repeated checks                                     |
| Simplify      | `/simplify`   | Runs 3 parallel review agents against your code checking for reuse opportunities, quality issues, and efficiency               |

These are the best examples of production-quality skills to study before writing your own.

### 2. The `skill-creator`

`skill-creator` is a meta-skill for building and iterating on skills. Available as a plugin in the [Claude.ai](https://www.claude.ai) directory and for Claude Code.

**How it works:**

1. Describe what you want your skill to do
2. skill-creator guides you through structuring the `SKILL.md`
3. It suggests folder layout, trigger descriptions, and instruction patterns
4. It helps test trigger behavior with example user requests
5. It iterates with you until trigger accuracy is high

**What it checks:**

- Trigger description quality - is it specific enough to activate correctly?
- Instruction clarity - will Claude follow the steps without ambiguity?
- Hallucination risk - are there gaps where Claude might invent steps?
- Composability - does the skill work well alongside other skills?

**Note:** skill-creator does not execute automated test suites or produce quantitative evaluation results. Use it for generation, review, and iterative improvement.

**Usage:**

| Purpose            | Prompt                                                                                                          |
| ------------------ | --------------------------------------------------------------------------------------------------------------- |
| Create a skill     | "Help me build a skill for [use case]" or "Use the skill-creator skill to help me build a skill for [use case]" |
| Review a skill     | "Review this skill and suggest improvements"                                                                    |
| Improve edge cases | "Use the issues identified in this chat to improve how the skill handles [specific edge case]"                  |

### 3. Troubleshooting

| Problem                  | Error / Symptom                                   | Fix                                                                                      |
| ------------------------ | ------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Won't upload             | "Could not find `SKILL.md`"                       | Rename file exactly `SKILL.md` (case-sensitive)                                          |
| Won't upload (ZIP)       | "Could not find `SKILL.md`" despite file existing | ZIP must have skill in a subfolder: `my-skill.zip/my-skill/SKILL.md`, not at root        |
| Won't upload             | "Invalid frontmatter"                             | Add `---` delimiters; close all quotes                                                   |
| Won't upload             | "Invalid skill name"                              | Use kebab lowercase: `my-cool-skill`                                                     |
| Doesn't trigger          | Skill never loads automatically                   | Add specific trigger phrases to description                                              |
| Triggers too often       | Loads for unrelated queries                       | Add negative triggers; be more specific                                                  |
| MCP fails                | Skill loads but MCP calls fail                    | Check connection, auth, tool name spelling; test MCP independently                       |
| Instructions ignored     | Claude doesn't follow the workflow                | Shorten content; put critical rules at top; use precise commands; add validation scripts |
| Slow / degraded          | Responses slow or quality drops                   | Move docs to `references/`; keep `SKILL.md` under 5,000 words; disable unused skills     |
| Multiple skills conflict | Overlapping descriptions                          | Differentiate descriptions; add exclusion notes                                          |

**CRITICAL:** For operations with side effects (creating records, sending messages, charging accounts), validate inputs before calling the MCP tool. Code is deterministic; language interpretation isn't. Consider a validation script rather than relying on instructions alone.

**Model laziness** - if Claude skips validation steps, add explicit encouragement in the user prompt (more effective than in `SKILL.md`):

```markdown
## Performance Notes

- Take your time to do this thoroughly
- Quality is more important than speed
- Do not skip validation steps
```

---

## Appendices

### A: Development Checklist

**Phase 1 - Before You Start:**

- [ ] Identified 2-3 concrete use cases
- [ ] Tools identified (built-in or MCP)
- [ ] Reviewed this guide and example skills
- [ ] Planned folder structure

**Phase 2 - During Development:**

- [ ] Folder named in kebab-case (`my-skill-name`)
- [ ] `SKILL.md` file exists (exact spelling, case-sensitive)
- [ ] YAML frontmatter has `---` delimiters (open and close)
- [ ] `name` field: kebab-case, no spaces, no capitals
- [ ] `description` includes WHAT (it does) and WHEN (to use it)
- [ ] No XML tags (`<` or `>`) anywhere in frontmatter
- [ ] Instructions are clear and actionable
- [ ] Error handling included
- [ ] References clearly linked

**Phase 3 - Before Upload:**

- [ ] Tested triggering on obvious tasks
- [ ] Tested triggering on paraphrased requests
- [ ] Verified it does NOT trigger on unrelated topics
- [ ] Functional tests pass
- [ ] Tool integration works (if applicable)
- [ ] Compressed as `.zip` file

**Phase 4 - After Upload:**

- [ ] Tested in real conversations
- [ ] Monitoring for under/over-triggering
- [ ] Collecting user feedback
- [ ] Iterating on description and instructions
- [ ] Updating version number in metadata

**Quick diagnostic:**

| #   | Problem              | First Place to Check                          |
| --- | -------------------- | --------------------------------------------- |
| 1   | Won't upload         | Phase 2 checklist - naming, YAML format       |
| 2   | Won't trigger        | Description missing trigger phrases           |
| 3   | Triggers too much    | Description too vague; add negative triggers  |
| 4   | Instructions ignored | Too verbose or buried; restructure `SKILL.md` |
| 5   | MCP calls failing    | Connection, auth, or tool name mismatch       |

### B: YAML Frontmatter Reference

```yaml
---
name: skill-name # Required: kebab-case only
description: What it does. Use when... # Required: what + when + trigger phrases
license: MIT # Optional
allowed-tools: "Bash(python:*) WebFetch" # Optional: 1-500 chars
model: opus # Optional: override default model (opus/sonnet/haiku)
effort: high # Optional: reasoning effort  -  low / medium / high / max
context: fork # Optional: "fork" runs skill in an isolated subagent
user-invocable: false # Optional: false = background knowledge only, no slash command
paths: "**/*.test.ts" # Optional: auto-activate when these file patterns are touched
disable-model-invocation: true # Optional: skill can only be triggered manually
argument-hint: "Pass the PR URL" # Optional: hint shown in slash-command autocomplete
hooks: # Optional: lifecycle hooks at specific execution points
  pre: scripts/validate.sh
  post: scripts/cleanup.sh
metadata: # Optional: any custom key-value pairs
  author: Company Name
  version: 1.0.0
  mcp-server: server-name
  category: productivity
  tags: [project-management, automation]
  documentation: https://example.com/docs
---
```

**Security:**

- Allowed: standard YAML types, custom metadata, descriptions under 1024 chars
- Forbidden: XML angle brackets (`<` or `>`), skills named with "claude" or "anthropic" prefix, code execution in YAML

### C: Key Takeaways

1. **Skills transform Claude from general assistant to specialized agent** with procedural knowledge, executable scripts, and on-demand references.
2. **`SKILL.md` is the only required file** - YAML frontmatter for trigger matching, Markdown body for execution instructions.
3. **Progressive disclosure saves 70-90% of tokens** by loading skill details only when triggered.
4. **Scripts provide deterministic reliability** for tasks that must produce consistent, exact results.
5. **Skills and MCP are complementary** - MCP provides connections, skills provide procedures.
6. **Same skill format works everywhere** - Claude.ai, Claude Code, and the Anthropic API.
7. **Composability is built-in** - Claude automatically sequences multiple skills for complex tasks.
8. **Treat skills like code** - version control, test systematically, iterate on real feedback.

### D: Resources

**Official Anthropic documentation:**

- [Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Best Practices Guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skills API Quickstart](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart)
- [API Reference](https://platform.claude.com/docs/en/api/overview)
- [MCP Documentation](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Agent SDK Documentation](https://docs.claude.com/en/docs/agent-sdk/overview)

**Blog posts:**

- [Introducing Agent Skills](https://claude.com/blog/skills)
- [Engineering Blog: Equipping Agents for the Real World](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Skills Explained](https://claude.com/blog/skills-explained)
- [How to Create Skills for Claude](https://claude.com/blog/how-to-create-skills-key-steps-limitations-and-examples)
- [Building Skills for Claude Code](https://claude.com/blog/complete-guide-to-building-skills-for-claude)
- [Improving Frontend Design through Skills](https://claude.com/blog/improving-frontend-design-through-skills)
- [Building AI Agents for the Enterprise](<https://cdn.prod.website-files.com/6889473510b50328dbb70ae6/69f3af1f0b8ebe5cde42fcda_Claude-Building-AI-Agents-in-the-Enterpise-04302026_v2%20(1).pdf>)

**API & SDK:**

- [Skills API Quickstart](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart)
- [Create Custom Skills](https://docs.claude.com/en/api/skills/create-skill)
- [Skills in the Agent SDK](https://docs.claude.com/en/docs/agent-sdk/skills)

**Skills repositories:**

- [github.com/anthropics/skills](https://github.com/anthropics/skills)
- [claude.com/connectors](https://www.claude.com/connectors)
- [agentskills.io](https://agentskills.io)

**Community:**

- [Claude Developers Discord](https://discord.com/invite/6PPFFzqPDZ)
- [GitHub Issues](https://github.com/anthropics/skills/issues)

**Learning:**

- [Introduction to Agent Skills](https://anthropic.skilljar.com/) - Anthropic's official course on Skilljar covering agent fundamentals, skill architecture, step-by-step creation, testing, and publishing
- [Module 5: AI Agents & Automation](https://learn-prompting.fr/guides/rag-retrieval-augmented-generation) - Deep dive into agent procedures, context management, multi-step task decomposition, testing, and production deployment

**Source documents:**

- [The Complete Guide to Creating Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) - Anthropic, January 29, 2026
- [Building Skills for Claude: The Complete Guide to Modular AI Expertise](https://learn-prompting.fr/blog/building-skills-for-claude-complete-guide) - Dorian Laurenceau, April 24, 2026

### E: Starter Templates by Persona

The following are complete, ready-to-paste `SKILL.md` files. Save each to `.claude/skills/<skill-name>/SKILL.md` (Claude Code) or ZIP and upload to Claude.ai. Replace anything in `[BRACKETS]` with your own values.

Templates are organized by persona. More templates - including Product Manager, Startup Founder, and Business Professional sets - are catalogued in the community at [agentskills.io](https://agentskills.io).

#### Everyday Users

**Meeting Notes Autopilot:**

```markdown
---
name: meeting-notes-autopilot
description: Transforms raw meeting transcripts into structured notes with decisions, action items, owners, and deadlines in a consistent searchable format. Use when given a meeting transcript, recording summary, or rough meeting notes.
---

# Meeting Notes Autopilot

When given a meeting transcript, recording summary, or rough notes:

## Output Format

### Meeting Metadata

- Date: [extract from transcript]
- Attendees: [list all participants mentioned]
- Duration: [if available]
- Meeting type: [standup/review/brainstorm/1:1/other]

### Decisions Made

For each decision: what was decided, who decided it, any context or constraints mentioned.

### Action Items

Table format:

| Owner | Action | Deadline | Priority |
| ----- | ------ | -------- | -------- |

Flag any action item without an owner as UNASSIGNED.

### Key Discussion Points

3-7 bullets capturing substance. Skip pleasantries and tangents.

### Open Questions

Anything raised but not resolved. Tag with who should answer.

### Follow-up Needed

What should happen before the next meeting.

## Rules

- Never fabricate attendee names. Use only names mentioned in the transcript.
- If the transcript is unclear, say "unclear from transcript" rather than guessing.
- Keep bullet points under 2 sentences each.
```

---

**Email Draft Writer:**

```markdown
---
name: email-drafter
description: Drafts emails in the user's personal voice and style. Use when asked to write, draft, or compose an email.
---

# Email Draft Writer

## My Email Style

- Tone: [FRIENDLY / PROFESSIONAL / CASUAL] - default to professional-friendly
- Length: Short (2-3 paragraphs max)
- Greeting: "Hey [Name]," for peers; "Hi [Name]," for external
- Sign-off: [YOUR PREFERRED SIGN-OFF]
- Never use: more than one exclamation point per email, emojis in work email, "Hope this email finds you well"

## Rules

1. Match formality to the recipient: internal = casual, client = professional.
2. Lead with the ask or the point. No throat-clearing paragraphs.
3. If the email requires a decision, bold the options.
4. Keep paragraphs to 2-3 sentences max.

## Output Format

1. Subject line
2. Full email body
3. Flag anything to double-check before sending

## Pro Tip

Add 3-5 real emails you've written at the bottom of this file as examples. Claude will match your voice much more accurately.
```

---

**Weekly Review Generator:**

```markdown
---
name: weekly-review
description: Generates a structured weekly review from notes, calendar events, and completed tasks. Use when asked to do a weekly review, reflect on the week, or plan next week.
---

# Weekly Review Generator

When given the week's data (notes, calendar, task list, journal entries):

## Output Structure

### This Week's Wins

3-5 accomplishments, big or small. Include anything finished, shipped, or meaningfully progressed.

### What Didn't Get Done (And Why)

Tasks that rolled over. Be honest: was it prioritization, blocked, or avoidance?

### Key Learnings

2-3 things learned or realized. Can be professional, personal, or about a tool or process.

### Energy Audit

- What gave energy this week?
- What drained it?
- Pattern check: is this the same as last week?

### Next Week's Top 3 Priorities

Only 3. Force rank them. Each must be specific and completable within the week.

### One Thing to Stop Doing

A habit, commitment, or task that isn't serving you.

## Rules

- Be direct. Don't sugarcoat unfinished work.
- If not enough data is provided, ask specific questions before generating.
```
