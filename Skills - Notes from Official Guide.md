# The Complete Guide to Building Skills for Claude

Notes from Official Anthropic Documentation

> Stop re-prompting. Package your domain expertise into a skill once, and Claude applies it consistently every time — without setup, without reminders.

## Table of Contents

[Introduction](#introduction)
[Chapter 1: Fundamentals](#chapter-1-fundamentals)
[Chapter 2: Planning and Design](#chapter-2-planning-and-design)
[Chapter 3: Testing and Iteration](#chapter-3-testing-and-iteration)
[Chapter 4: Distribution and Sharing](#chapter-4-distribution-and-sharing)
[Chapter 5: Patterns and Troubleshooting](#chapter-5-patterns-and-troubleshooting)
[Chapter 6: Resources and References](#chapter-6-resources-and-references)

## Introduction

- Skills give Claude persistent, structured expertise through a simple folder format.
- A [skill](https://claude.com/blog/skills) is a set of instructions that tells Claude how to handle specific tasks or workflows.
- The architecture loads only what's needed, when it's needed, minimizing context overhead.
- For MCP builders, skills provide the workflow layer that transforms tool access into reliable outcomes.
- Example of a skill: [skill-creator](#the-skill-creator-skill) — an interactive guide that helps you build new skills.

## Chapter 1: Fundamentals

### Skill folders contain

```tree
📁 skill-name/
├── SKILL.md          ← Required: Markdown instructions w/YAML frontmatter
├── scripts/          ← Optional: Executable code (Python, Bash, etc.)
├── references/       ← Optional: docs, guides, examples
└── assets/           ← Optional: templates, fonts, icons`
```

### Core design principles

- **Progressive Disclosure**: Only load what's needed — minimizes token usage, in a three-level system:
  - **Level 1. YAML frontmatter**: Always in Claude's system prompt, letting it know when to use it.
  - **Level 2. `SKILL.md` body**: Loads when Claude judges it relevant, contains full instructions.
  - **Level 3. Linked files**: Additional files loaded on demand, containing specialized instructions.

- **Composability**: Multiple skills can be active simultaneously — design to coexist.
- **Portability**: One skill, all surfaces — [Claude.ai](https://claude.ai), Claude Code, API.

### For MCP Builders: Skills + Connectors

- MCP servers provide the tools and data access; skills provide the expertise on how to use them effectively.
- Kitchen analogy: MCP provides the kitchen (tools, ingredients, and equipment); skills the recipes.
- How they work together:

|          | MCP (Connectivity)                                            | Skills (Knowledge)                                 |
| -------- | ------------------------------------------------------------- | -------------------------------------------------- |
| Purpose  | Connects Claude to your service (Notion, Asana, Linear, etc.) | Teaches Claude how to use your service effectively |
| Function | Provides real-time data access and tool invocation            | Captures workflows and best practices              |
| Scope    | What Claude can do                                            | How Claude should do it                            |

#### Without and With Skills: The User Experience

|                             | MCP without Skills                                                          | MCP with Skills                                                                                     |
| --------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| User Experience             | Users have access to tools but must figure out how to use them on their own | Users get guided workflows that automatically leverage the MCP tools                                |
| Outcomes                    | Inconsistent results, user frustration, and support tickets                 | Reliable, consistent outcomes with less user effort and higher satisfaction                         |
| Value to Users              | Access to powerful tools but with a steep learning curve                    | Immediate value through embedded expertise and best practices                                       |
| Value to MCP Builders       | MCP is just a connection; users may not see the value of your integration   | Your integration shines as users experience the full potential through skills                       |
| Business Impact             | Users may give up or blame your integration for poor results                | Higher adoption, better reviews, and stronger retention due to superior experience                  |
| Support Burden              | High support tickets for "how do I do X with your integration?"             | Lower support tickets as users can rely on the skill's guidance                                     |
| Competitive Differentiation | Your MCP is just a connector; competitors can easily replicate              | Skills create a unique value layer that differentiates your integration                             |
| User Onboarding             | Users struggle to get started and may never see the value                   | Skills provide an immediate "aha moment" that demonstrates value and encourages exploration         |
| Long-term Engagement        | Users may use the MCP sporadically or abandon it                            | Skills encourage regular use by making it easier and more rewarding to engage with your integration |

## Chapter 2: Planning and Design

- Good skills are designed, not written. The quality of the design determines the quality of the skill.
- The description (YAML frontmatter) is the most critical part of the skill — it determines whether Claude even loads it.
- Define success criteria upfront, then structure the skill around achieving those outcomes.

### Workflow

1. Define 2–3 concrete use cases before writing a single line.

   **Example:**

   ```markdown
   Use Case: Project Sprint Planning
   Trigger: User says "help me plan this sprint"/"create sprint tasks"
   Steps:

   1. Fetch current project status from Linear (via MCP)
   2. Analyze team velocity and capacity
   3. Suggest task prioritization
   4. Create tasks in Linear with proper labels and estimates

   Result: Fully planned sprint with tasks created
   ```

2. Key Design Questions:
   - _What does a user want to accomplish?_ → Description
   - _What multi-step workflows does this require?_ → Workflow
   - _Which tools are needed (built-in or MCP?)_ → Tools, Scripts or MCP
   - _What domain knowledge or best practices should be embedded?_ → References

### Common Skill Use Case Categories

1. **Category 1: Document & Asset Creation**. Create consistent, high-quality output including documents, presentations, apps, designs, code, etc.
   - Key techniques:
     - Embedded style guides and brand standards
     - Template structures for consistent output
     - Quality checklists before finalizing
     - No external tools required - uses Claude's built-in capabilities
   - Prompt example:

     ```text
     Prompt: "Create distinctive, production-grade frontend interfaces with high design quality. Use when building web components, pages, artifacts, posters, or applications."
     ```

   - Example:  [frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) skill or skills for [docx, pptx, xlsx, and ppt](https://github.com/anthropics/skills/tree/main/skills).

2. **Category 2: Workflow Automation**. Multi-step processes that benefit from consistent methodology, includes MCP server coordination.
   - Key techniques:
     - Step-by-step workflow with validation gates
     - Templates for common structures
     - Built-in review and improvement suggestions
     - Iterative refinement loops
   - Prompt example:

     ```text
     Prompt: "Interactive guide for creating new skills. Walks the user through use case definition, frontmatter generation, instruction writing, and validation."
     ```

   - Example: [skill-creator skill](https://github.com/anthropics/skills/tree/main/skills/skill-creator)

3. **Category 3: MCP Enhancement**. Guidance to enhance the tool access an MCP server provides.
   - Key techniques:
     - Coordinates multiple MCP calls in sequence
     - Embeds domain expertise
     - Provides context users would otherwise need to specify
     - Error handling for common MCP issues
   - Prompt example:

     ```text
     Prompt: "Automatically analyzes and fixes detected bugs in GitHub Pull Requests using Sentry's error monitoring data via their MCP server."
     ```

   - Example: [GitHub PR analysis with Sentry](https://github.com/getsentry/sentry-for-claude/tree/main/skills/sentry-code-review)

### Define success criteria

- **Quantitative** metrics: Objective measures of skill performance:
  - Skill triggers on 90% of relevant queries (test with 10-20 queries): Automatic vs. explicit loads.
  - Completes workflow in X tool calls: Count tool calls & tokens consumed with and without the skill.
  - 0 failed API calls per workflow: Track retry rates & errors in MCP server logs during test runs.
  - Response time under Y seconds: Measure time from trigger to final output.
  - User satisfaction score of 4+ out of 5: Collect feedback from test users.
  - Reduction in support tickets related to the task by 50%: Track support inquiries before and after skill deployment.
- **Qualitative** metrics: Subjective measures of user experience and output quality:
  - Users don't need to prompt Claude about next steps: Note how often you need to redirect or clarify.
  - Workflows complete without correction: Compare consistency/quality after same request runs 3-5x.
  - Consistent results across sessions: Can new users succeed on first try with minimal guidance?
  - Positive user feedback on ease of use and output quality: Collect testimonials and feedback from users.
  - Demonstrable improvement in output quality compared to manual processes: Compare outputs with and without the skill for the same input.
  - Users report increased confidence in using the tool after skill implementation: Collect user feedback on confidence levels before and after using the skill.

### Technical requirements

#### File Structure

```tree
📁 skill-name/
├── SKILL.md                    ← Required: Markdown instructions w/YAML frontmatter
├── scripts/                    ← Optional: Executable code (Python, Bash, etc.)
│    ├── process_data.py        ← Example
│    └── validate.sh            ← Example
├── references/                 ← Optional: docs, guides, examples
│    ├── api-guide.md           ← Example
│    └── examples/              ← Example
└── assets/                     ← Optional: templates, fonts, icons
     └── report-template.md     ← Example
```

#### Critical rules

- **Skill folder naming**: Use kebab-case (e.g. notion-project-setup). No spaces, underscores nor capital letters.
- **`SKILL.md` naming**: Case-sensitive (exactly `SKILL.md`). No variations (`SKILL.MD`, `skill.md`, etc.).
- **No `README.md`**: Don't include `README.md` inside the skill folder. All docs in `SKILL.md` or `references/`.
- **YAML Frontmatter**: Opening section of `SKILL.md` and how Claude understands whether to load your skill.
- **Format**:

  ```yaml
  ---
  name: skill-name
  description: What it does. Use when user asks to [specific phrases].
  ---
  ```

- YAML frontmatter must be enclosed by `---` at the top and bottom.
- **Fields**:
  - **name**: kebab-case only. No spaces or capitals. Match folder name. Cannot be Claude or Anthropic.
  - **description**: What the skill does AND when to use it (trigger conditions). <1024 characters. No XML tags (< or >). Include specific tasks users might say. Mention file types if relevant.
  - **license** (optional): Use if making skill open source, Common: MIT, Apache-2.0.
  - **compatibility** (optional): <500 characters, Indicates environment requirements: e.g. intended product, required system packages, network access needs, etc.
  - **metadata** (optional): Any custom key-value pairs, i.e. author, version, mcp-server.

    ```yaml
    metadata:
      author: ProjectHub
      version: 1.0.0
      mcp-server: projecthub
    ```

### Writing Effective Descriptions

> "Provides enough information for Claude to know when each skill should be used without loading all of it into context." (First level of progressive disclosure) -According to Anthropic's [engineering blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

- **Structure: [What it does] + [When to use it] + [Key capabilities]**
- Good example:

  ```text
  - Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".
  - Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".
  - End-to-end customer onboarding workflow for PayFlow. Handles account creation, payment setup, and subscription management. Use when user says "onboard new customer", "set up subscription", or "create PayFlow account".
  ```

- Bad example:

  ```text
  - (Too vague) Helps with projects.
  - (Missing triggers) Creates sophisticated multi-page documentation systems.
  - (Too technical, no user triggers) Implements the Project entity model with hierarchical relationships.
  ```

### Writing Effective Skills

- Keep `SKILL.md` focused on core instructions.
- Move detailed documentation to `references/` and link to it.
- After the frontmatter, write the actual instructions in Markdown.
- Recommended **structure**:

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

  '''bash
  python scripts/fetch_data.py --project-id PROJECT_ID
  '''

  Expected output: [describe what success looks like]

  (Add more steps as needed)

  ## Examples

  ### Example 1: [common scenario]

  User says: "Set up a new marketing campaign"

  Actions:

  1. Fetch existing campaigns via MCP
  2. Create new campaign with provided parameters

  Result: Campaign created with confirmation link

  (Add more examples as needed)

  ## Troubleshooting

  Error: [Common error message]

  Cause: [Why it happens] Solution: [How to fix]

  (Add more error cases as needed)

  ## Best Practices for Instructions

  ### Be Specific and Actionable

  ✅ **Good:**

  Run python scripts/validate.py --input {filename} to check data format. If validation fails, common issues include:

  - Missing required fields (add them to the CSV)
  - Invalid date formats (use YYYY-MM-DD)

  ❌ **Bad:**

  Validate the data before proceeding.

  ## Error handling

  ### Common Issues

  #### MCP Connection Failed

  If you see "Connection refused":

  1. Verify MCP server is running: Check Settings > Extensions
  2. Confirm API key is valid
  3. Try reconnecting: Settings > Extensions > [Your Service] > Reconnect

  Reference bundled resources clearly

  Before writing queries, consult `references/api-patterns.md` for:

  - Rate limiting guidance

  - Pagination patterns
  - Error codes and handling
  ```

## Chapter 3: Testing and Iteration

Skills can be tested at varying levels of rigor depending on your needs:

- **Manual testing in [Claude.ai](https://www.claude.ai/)** - Run queries directly and observe behavior. Fast iteration, no setup required.
- **Scripted testing in Claude Code** - Automate test cases for repeatable validation across changes.
- **Programmatic testing via skills API** - Build systematic evaluation suites that run test sets.

Choose the approach that matches your quality requirements and the visibility of your skill. E.g. small-team internal skills have different testing needs than one deployed to thousands of enterprise users.

**Pro Tip**: Iterate on a single task before expanding

- Iterate on a single challenging task until Claude succeeds, then extract the winning approach into a skill.
- This leverages Claude's in-context learning and provides faster signal than broad testing.
- Once you have a working foundation, expand to multiple test cases for coverage.

### Recommended Testing Approach

Three testing areas:

1. **Triggering tests**: Ensure your skill loads at the right times.
   - ✅ Triggers on obvious tasks (e.g. "Help me set up a new ProjectHub workspace")
   - ✅ Triggers on paraphrased requests (e.g. "I need to create a project in ProjectHub")
   - ❌ Doesn't trigger on unrelated topics (e.g. "What's the weather in San Francisco?")
2. **Functional tests**: Verify the skill produces correct outputs.
   - Valid outputs generated
   - API calls succeed
   - Error handling works
   - Edge cases covered

   - Example:

   ```text
       Test: Create project with 5 tasks
       Given: Project name "Q4 Planning", 5 task descriptions
       When: Skill executes workflow
       Then:
        - Project created in ProjectHub
        - 5 tasks created with correct properties
        - All tasks linked to project
        - No API errors
   ```

3. **Performance comparison**: Prove the skill improves results vs. baseline.
   - Use the metrics from Define Success Criteria. Here's what a comparison might look like.
   - Example, baseline comparison:
     - **Without skill**: User provides instructions each time, 15 back-and-forth messages, 3 failed API calls requiring retry, 12,000 tokens consumed.
     - **With skill**: Automatic workflow execution, 2 clarifying questions only, 0 failed API calls, 6,000 tokens consumed.

## The `skill-creator` skill

- It helps build and iterate on skills.
- Is an available plugin in Claude.ai directory or download for Claude Code.
- It does not execute automated test suites or produce quantitative evaluation results.

Creating skills:

- Generate skills from natural language descriptions
- Produce properly formatted SKILL.md with frontmatter
- Suggest trigger phrases and structure

Prompt:

```text
Use the skill-creator skill to help me build a skill for [your use case]
```

Reviewing skills:

- Flag common issues (vague descriptions, missing triggers, structural problems)
- Identify potential over/under-triggering risks
- Suggest test cases based on the skill's stated purpose

Iterative improvement:

- After using your skill and encountering edge cases or failures, bring those examples back to skill-creator.
- Example:

  ```text
  Use the issues & solution identified in this chat to improve how the skill handles [specific edge case]
  ```

Iteration Signals:

| Signal               | Symptoms                                                          | Fix                                                    |
| -------------------- | ----------------------------------------------------------------- | ------------------------------------------------------ |
| **Undertriggering**  | Skill doesn't load; users manually enabling it; support questions | Add more keywords and trigger phrases to description   |
| **Overtriggering**   | Loads for irrelevant queries; users disabling it                  | Add negative triggers; be more specific in description |
| **Execution issues** | Inconsistent results; API failures; users correcting Claude       | Improve instructions; add error handling               |

## Chapter 4: Distribution and Sharing

- Skills can be distributed individually, organization-wide, or programmatically via the API.
- The open standard at [agentskills.io](https://agentskills.io) means your skill isn't locked to Claude.
- For MCP builders, skills complete the integration story — users with both MCP and a skill get a dramatically better experience than those with MCP alone.

Current distribution model (January 2026)

1. How individual users get skills:
   a. Download the skill folder
   b. Zip the folder (if needed)
   c. Upload to Claude.ai via Settings > Capabilities > Skills
   d. Or place in Claude Code skills directory

2. Organization-level skills:
   a. Admins can deploy skills workspace-wide (shipped December 18, 2025)
   b. Automatic updates
   c. Centralized management

3. An open standard:
   ○ We've published Agent Skills as an open standard -a portable tool across platforms. See [agentskills.io](https://agentskills.io) for more information.

4. Using skills via API
   ○ For programmatic use cases, such as building applications, agents, or automated workflows that leverage skills, the API provides direct control over skill management and execution.
   ○ Skills in the API require the Code Execution Tool beta -provides secure environment needed to run.
   ○ Key capabilities:
   § /v1/skills endpoint for listing and managing skills
   § Add skills to Messages API requests via the container.skills parameter
   § Version control and management through the Claude Console
   § Works with the Claude Agent SDK for building custom agents

### When to use skills via the API vs. [Claude.ai](https://www.claude.com/ai)

| Use Case                                   | Best Surface              |
| ------------------------------------------ | ------------------------- |
| End users interacting with skills directly | `Claude.ai` / Claude Code |
| Manual testing during development          | `Claude.ai` / Claude Code |
| Individual, ad-hoc workflows               | `Claude.ai` / Claude Code |
| Applications using skills programmatically | API                       |
| Production deployments at scale            | API                       |
| Automated pipelines and agent systems      | API                       |

For implementation details, see:

- [Skills API Quickstart](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart)
- [Create Custom skills](https://docs.claude.com/en/api/skills/create-skill)
- [Skills in the Agent SDK](https://docs.claude.com/en/docs/agent-sdk/skills)

### Recommended approach today

1. Host on GitHub
   - Public repo for open-source skills
   - Clear README with installation instructions (e.g. not inside skills folder)
   - Example usage and screenshots

2. Document in Your MCP Repo
   - Link to skills from MCP documentation
   - Explain the value of using both together
   - Provide quick-start guide

3. Create an Installation Guide
4. Download or `git clone https://github.com/yourcompany/skills`
5. Install: Claude.ai > Settings > Skills > Upload skill (zip folder)
6. Enable: Toggle on [Your Service] skill; ensure connected MCP server
7. Test: Ask Claude: "Set up a new project in [Your Service]"

### Positioning — Outcomes, Not Features

- **Good**: "The ProjectHub skill sets up complete project workspaces in seconds — pages, databases, and templates — instead of 30 minutes of manual setup."
- **Bad**: "The ProjectHub skill is a folder containing YAML frontmatter and Markdown instructions that calls our MCP server tools."

## Chapter 5: Patterns and Troubleshooting

- Five proven patterns cover the vast majority of skill use cases.
- Knowing which pattern fits your workflow shapes the structure of your `SKILL.md`.
- When things go wrong, most issues fall into three buckets:
  - Skill won't load (description),
  - Instructions aren't followed (`SKILL.md` content), or
  - MCP calls fail (connectivity/config).

| Framing           | User Says                              | Skill Does                                     | Notes                                                |
| ----------------- | -------------------------------------- | ---------------------------------------------- | ---------------------------------------------------- |
| **Problem-first** | "I need to set up a project workspace" | Orchestrates the right MCP calls in sequence   | Users describe outcomes; the skill handles the tools |
| **Tool-first**    | "I have Notion MCP connected"          | Teaches Claude optimal workflows for that tool | Users have access; the skill provides expertise      |

### Patterns

#### Pattern 1: Sequential Workflow Orchestration

**Use when**: Users need multi-step processes in a specific order.
**Key techniques**: explicit step ordering, dependencies between steps, validation at each stage, rollback instructions.
**Example**: New customer onboarding workflow for a SaaS product, coordinating multiple MCP calls.

```markdown
## Workflow: Onboard New Customer

### Step 1: Create Account

Call MCP tool: `create_customer`
Parameters: name, email, company

### Step 2: Setup Payment

Call MCP tool: `setup_payment_method`
Wait for: payment method verification

### Step 3: Create Subscription

Call MCP tool: `create_subscription`
Parameters: plan_id, customer_id (from Step 1)

### Step 4: Send Welcome Email

Call MCP tool: `send_email`
Template: welcome_email_template
```

#### Pattern 2: Multi-MCP Coordination

**Use when**: Workflows span multiple services.
**Key techniques**: clear phase separation, data passing between MCPs, centralized error handling.
**Example**: Design-to-development handoff workflow spanning Figma, Drive, Linear, and Slack MCPs.

```markdown
### Phase 1: Design Export (Figma MCP)

1. Export design assets from Figma
2. Generate design specifications
3. Create asset manifest

### Phase 2: Asset Storage (Drive MCP)

1. Create project folder in Drive
2. Upload all assets
3. Generate shareable links

### Phase 3: Task Creation (Linear MCP)

1. Create development tasks
2. Attach asset links to tasks
3. Assign to engineering team

### Phase 4: Notification (Slack MCP)

10. Post handoff summary to #engineering
11. Include asset links and task references
```

#### Pattern 3: Iterative Refinement

**Use when**: Output quality improves with iteration.
**Key techniques**: explicit quality criteria, validation scripts, know when to stop iterating.
**Example**: Report generation

```markdown
## Iterative Report Creation

### Initial Draft

1. Fetch data via MCP
2. Generate first draft report
3. Save to temporary file

### Quality Check

1. Run validation script: `scripts/check_report.py`
2. Identify issues:
   - Missing sections
   - Inconsistent formatting
   - Data validation errors

### Refinement Loop

1. Address each identified issue
2. Regenerate affected sections
3. Re-validate
4. Repeat until quality threshold met

### Finalization

1. Apply final formatting
2. Generate summary
3. Save final version
```

#### Pattern 4: Context-Aware Tool Selection

**Use when**: Same outcome, different tools depending on context.
**Key techniques**: clear decision criteria, fallback options, transparency about choices.
**Example**: File storage

```markdown
## Smart File Storage

### Decision Tree

1. Check file type and size
2. Determine best storage location:
   - Large files (>10MB): Use cloud storage MCP
   - Collaborative docs: Use Notion/Docs MCP
   - Code files: Use GitHub MCP
   - Temporary files: Use local storage

### Execute Storage

Based on decision:

- Call appropriate MCP tool
- Apply service-specific metadata
- Generate access link

### Provide Context to User

Explain why that storage was chosen
```

#### Pattern 5: Domain-Specific Intelligence

**Use when**: Your skill adds specialized knowledge beyond tool access.
**Key techniques**: domain expertise embedded in logic, compliance-before-action, comprehensive documentation.
**Example**: Financial compliance

```markdown
## Payment Processing with Compliance

### Before Processing (Compliance Check)

1. Fetch transaction details via MCP
2. Apply compliance rules:
   - Check sanctions lists
   - Verify jurisdiction allowances
   - Assess risk level
3. Document compliance decision

### Processing

IF compliance passed:

- Call payment processing MCP tool
- Apply appropriate fraud checks
- Process transaction

ELSE:

- Flag for review
- Create compliance case

### Audit Trail

- Log all compliance checks
- Record processing decisions
- Generate audit report
```

### Troubleshooting

| Problem              | Error / Symptom                    | Fix                                                                                                             |
| -------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Won't upload         | "Could not find `SKILL.md`"        | Rename file exactly `SKILL.md` (case-sensitive)                                                                 |
| Won't upload         | "Invalid frontmatter"              | Add --- delimiters; close all quotes                                                                            |
| Won't upload         | "Invalid skill name"               | Use kebab lowercase: my-cool-skill                                                                              |
| Doesn't trigger      | Skill never loads automatically    | Add specific trigger phrases to description; test by asking Claude when it would use the skill                  |
| Triggers too often   | Loads for unrelated queries        | Add negative triggers ("Do NOT use for..."); be more specific                                                   |
| MCP fails            | Skill loads but MCP calls fail     | Check: connection status, auth/API keys, tool name spelling (case-sensitive), test MCP independently            |
| Instructions ignored | Claude doesn't follow the workflow | Shorten content; put critical rules at top; use precise commands not vague language; add scripts for validation |
| Slow / degraded      | Responses slow or quality drops    | Move docs to `references/`; keep `SKILL.md` under 5,000 words; disable unused skills                            |

**CRITICAL**: Before calling `create_project`, verify:

- Project name is non-empty
- At least one team member assigned
- Start date is not in the past

**Advanced technique**: For critical validations, consider bundling a script that performs the checks programmatically rather than relying on language instructions. Code is deterministic; language interpretation isn't. See the [Office skills](https://github.com/anthropics/skills/tree/main/skills) for examples of this pattern.

**Model "laziness"** - Add explicit encouragement. **Note**: Adding this to user prompts is more effective than in `SKILL.md`.:

```markdown
## Performance Notes

- Take your time to do this thoroughly
- Quality is more important than speed
- Do not skip validation steps
```

## Chapter 6: Resources and References

If you're building your first skill, start with the Best Practices Guide, then reference the API docs as needed.

### Anthropic Resources

- [Best Practices Guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [API Reference](https://platform.claude.com/docs/en/api/overview)
- [MCP Documentation](https://modelcontextprotocol.io/docs/getting-started/intro)

### Blog Posts

- [Introducing Agent Skills](https://claude.com/blog/skills)
- [Engineering Blog: Equipping Agents for the Real World](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Skills Explained](https://claude.com/blog/skills-explained)
- [How to Create Skills for Claude](https://claude.com/blog/how-to-create-skills-key-steps-limitations-and-examples)
- [Building Skills for Claude Code](https://claude.com/blog/complete-guide-to-building-skills-for-claude)
- [Improving Frontend Design through Skills](https://claude.com/blog/improving-frontend-design-through-skills)
- [Building AI agents for the Enterprise](<https://cdn.prod.website-files.com/6889473510b50328dbb70ae6/69f3af1f0b8ebe5cde42fcda_Claude-Building-AI-Agents-in-the-Enterpise-04302026_v2%20(1).pdf>)

### Public skills repository

- [GitHub: anthropics/skills](https://github.com/anthropics/skills)
- [Contains Anthropic-created skills you can customize](https://discord.com/invite/6PPFFzqPDZ)

### Tools and Utilities

`skill-creator` skill:

- Built into [Claude.ai](https://claude.ai) and available for Claude Code
- Can generate skills from descriptions
- Reviews and provides recommendations
- Use:

  | Purpose        | Prompt Example                               |
  | -------------- | -------------------------------------------- |
  | Create a skill | "Help me build a skill for [use case]"       |
  | Review a skill | "Review this skill and suggest improvements" |

### Getting Support & Reporting Issues

- General questions: Community forums at the [Claude Developers Discord](https://discord.com/invite/6PPFFzqPDZ)
- GitHub Issues: [anthropics/skills/issues](https://github.com/anthropics/skills/issues)
- Include: Skill name, error message, steps to reproduce

## Reference A: Quick Checklist

**Phase 1**: Before You Start

- [ ] Identified 2–3 concrete use cases
- [ ] Tools identified (built-in or MCP)
- [ ] Reviewed this guide and example skills
- [ ] Planned folder structure

**Phase 2**: During Development

- [ ] Folder named in kebab-case (e.g., `my-skill-name`)
- [ ] `SKILL.md` file exists (exact spelling, case-sensitive)
- [ ] YAML frontmatter has `---` delimiters (open and close)
- [ ] name field: kebab-case, no spaces, no capitals
- [ ] description includes **WHAT** (it does) and **WHEN** (to use it)
- [ ] No XML tags (`<` or `>`) anywhere in frontmatter
- [ ] Instructions are clear and actionable
- [ ] Error handling included
- [ ] Examples provided
- [ ] References clearly linked

**Phase 3**: Before Upload

- [ ] Tested triggering on obvious tasks
- [ ] Tested triggering on paraphrased requests
- [ ] Verified it does NOT trigger on unrelated topics
- [ ] Functional tests pass
- [ ] Tool integration works (if applicable)
- [ ] Compressed as `.zip` file

**Phase 4**: After Upload

- [ ] Tested in real conversations
- [ ] Monitoring for under/over-triggering
- [ ] Collecting user feedback
- [ ] Iterating on description and instructions
- [ ] Updating version number in metadata

**Quick Diagnostic**

| #   | Problem              | First Place to Check                          |
| --- | -------------------- | --------------------------------------------- |
| 1   | Won't upload         | Phase 2 checklist — naming, YAML format       |
| 2   | Won't trigger        | Description missing trigger phrases           |
| 3   | Triggers too much    | Description too vague; add negative triggers  |
| 4   | Instructions ignored | Too verbose or buried; restructure `SKILL.md` |
| 5   | MCP calls failing    | MCP connection, auth, or tool name mismatch   |

## Reference B: YAML Frontmatter

```yaml
---
name: skill-name                          <- Required: kebab-case only
description: What it does. Use when...    <-- Required: what + when + trigger phrases
license: MIT                              <-- Optional: for open-source skills
allowed-tools: "Bash(python:\*) WebFetch" <-- Optional: restrict tool access
metadata:                                 <-- Optional: any custom key-value pairs
  - author: Company Name
  - version: 1.0.0
  - mcp-server: server-name
  - category: productivity
  - tags: [project-management, automation]
  - documentation: [https://example.com/docs](https://example.com/docs)
  - support: <support@example.com>
---
```

### Field Reference

| Field         | Required | Rules                                                                            |
| ------------- | -------- | -------------------------------------------------------------------------------- |
| name          | Yes      | kebab-case, no spaces, no capitals, should match folder name                     |
| description   | Yes      | Must include what + when; under 1024 chars; no XML tags; include trigger phrases |
| license       | No       | e.g., MIT, Apache-2.0                                                            |
| allowed-tools | No       | 1–500 chars; restricts which tools the skill can invoke                          |
| metadata      | No       | Any custom key-value pairs; suggested: author, version, mcp-server               |

### Security Rules

**Allowed**:

- Standard YAML types: strings, numbers, booleans, lists, objects
- Custom metadata fields
- Long descriptions (< 1024 characters)

**Forbidden**:

- XML angle brackets (< or >) — frontmatter is injected into Claude's system prompt; malicious
- Skills named with claude or anthropic prefix (reserved by Anthropic)
- Code execution in YAML (safe YAML parsing is enforced)

## Reference C: Complete Skill Examples

For full, production-ready skills demonstrating the patterns in this guide:

- **Document Skills** -[PDF](https://github.com/anthropics/skills/tree/main/skills/pdf), [DOCX](https://github.com/anthropics/skills/tree/main/skills/docx), [PPTX](https://github.com/anthropics/skills/tree/main/skills/pptx), [XLSX](https://github.com/anthropics/skills/tree/main/skills/xlsx) creation
- **Various workflow** -[Example Skills](https://github.com/anthropics/skills/tree/main/skills)
  patterns](<https://github.com/anthropics/skills/tree/main/skills>)
- **Connectors** -[Partner Skills Directory](https://www.claude.com/connectors) - View skills from various partners such as Asana, Atlassian, Canva, Figma, Sentry, Zapier, and more

## Sources

- [The Complete Guide to Creating Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
- [Markdown Community Guide to Creating Skills for Claude](https://github.com/kevin828/the-complele-guide-to-building-skills-for-claude)
- [Community Gist Guide](https://gist.github.com/liskl/269ae33835ab4bfdd6140f0beb909873)
- [Anthropic's Agent Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Anthropic's Best Practices Guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Anthropic's API Reference](https://platform.claude.com/docs/en/api/overview)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/docs/getting-started/intro)
- [GitHub: anthropics/skills](https://github.com/anthropics/skills)
- [Claude Developers Discord](https://discord.com/invite/6PPFFzqPDZ)
- [Anthropic Engineering Blog: Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Improving Frontend Design through Skills](https://claude.com/blog/improving-frontend-design-through-skills)
- [Building AI agents for the Enterprise](<https://cdn.prod.website-files.com/6889473510b50328dbb70ae6/69f3af1f0b8ebe5cde42fcda_Claude-Building-AI-Agents-in-the-Enterpise-04302026_v2%20(1).pdf>)
- [Introducing Agent Skills](https://claude.com/blog/skills)
- [Skills Explained](https://claude.com/blog/skills-explained)
- [How to Create Skills for Claude](https://claude.com/blog/how-to-create-skills-key-steps-limitations-and-examples)
- [Anthropic's Agent SDK Documentation](https://docs.claude.com/en/docs/agent-sdk/overview)
-
