---
name: skiller
description: "Meta-agent that orchestrates complex multi-task jobs end to end. Activate immediately when the user says 'skiller' or '$skiller' anywhere in their message. Also use when the user describes a multi-step job that may need new capabilities, skill discovery, or workflow coordination. Trigger phrases: 'skiller', '$skiller', 'hey skiller', 'skiller do', '$skiller do', 'help me do X end to end', 'orchestrate a workflow', 'build a pipeline for', 'figure out what skills I need', 'handle everything for'. Does not trigger for single-skill tasks already covered by an installed skill."
version: "1.0.0"
license: MIT
metadata:
  author: juanlazarde@gmail.com
  requires: find-skills, skill-creator
---

# Skiller

Skiller is a meta-agent workflow orchestrator. It accepts any high-level requirement, breaks it into tasks, finds or builds the right skill for each task, runs the pipeline, delivers results to `inbox/`, collects feedback, and logs everything.

**Folder conventions:**
- `outbox/` — drop files here for Skiller to read. Skiller reads **only** from this folder, never from arbitrary paths the user mentions.
- `inbox/` — Skiller writes all final deliverables here for you to read.
- `wip/` — inter-task state (task briefs, intermediate outputs). Do not edit manually during a session.
- `logs/` — session changelogs.

```
User Requirement
      │
      ▼
[Phase 0] Pre-flight checks
      │
      ▼
[Phase 1] Requirements Intake ──────► confirm with user
      │
      ▼
[Phase 2] Task Planning ─────────────► agents/task-planner.md
      │                                writes wip/task-plan.md
      │                                writes wip/task-NNN-brief.md (×N)
      ▼
[Phase 3] Skill Research (per task) ► agents/skill-researcher.md
      │                                updates wip/task-NNN-brief.md
      ▼
[Phase 4] Skill Provisioning (per task)
      │   FOUND_LOCAL  → no action needed
      │   FOUND_REMOTE → safety check + user confirm + npx install
      │   NOT_FOUND    → fill brief template → skill-creator builds skill
      ▼
[Phase 5] Workflow Execution (per task in dependency order)
      │   each task reads wip/task-NNN-brief.md
      │   each task writes wip/task-NNN-output.*
      ▼
[Phase 6] Output Assembly
      │   writes inbox/[filename]
      ▼
[Phase 7] Feedback ──────────────────► agents/feedback-collector.md
      │                                writes wip/feedback-summary.md
      ▼
[Phase 8] Changelog
          updates skills based on feedback
          appends to logs/changelog.md
```

---

## Phase 0: Pre-flight

Before doing anything else, run these checks:

**Check 1 — Required skills installed**
Scan `~/.claude/skills/`, `~/.agents/skills/`, and `~/.codex/skills/` for `find-skills` and `skill-creator`.
If either is missing, print the following and stop:

```
SKILLER — BLOCKED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Missing required skill: [skill-name]

Install it with:
  npx skills add anthropics/skills@find-skills -g -y
  npx skills add anthropics/skills@skill-creator -g -y

Then retry your request.
```

**Check 2 — Working directory writable**
Confirm the current working directory exists and is writable. Create the following folders if they do not exist:
- `outbox/`
- `wip/`
- `inbox/`
- `logs/`

**Check 3 — Print status banner**
```
SKILLER v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Working directory: [absolute path to cwd]
Required skills:   find-skills [OK] · skill-creator [OK]
Folders ready:     outbox/ · wip/ · inbox/ · logs/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 1: Requirements Intake

1. Read the user's requirement exactly as stated. Do not interpret or alter it yet.

2. Scan the `outbox/` folder and list any files found there. If files are present, confirm them with the user:
   > "I found these files in outbox/: [list]. I'll use these as source material. Anything else to add, or shall I proceed?"
   Skiller reads **only** from `outbox/` for user-provided material — never from arbitrary paths mentioned in conversation.

3. Ask one clarifying question **only if** the intended output format is genuinely ambiguous (e.g., the user hasn't specified whether they want a single document, multiple files, a structured JSON, etc.). Do not ask about process — Skiller owns the process. If the output format is clear or inferable, skip this step.

4. Restate the requirement as a single sentence in your own words. Present it to the user:
   > "Here's how I understood your requirement: [one-sentence restatement]. Is this correct? (yes / correct it)"

5. Do not proceed to Phase 2 until the user confirms.

---

## Phase 2: Task Planning

Delegate to `agents/task-planner.md`. Pass:
- The confirmed one-sentence requirement
- The absolute path to the current working directory
- Today's date

The task planner will write `wip/task-plan.md` and one `wip/task-NNN-brief.md` per task.

Once the planner confirms it is done, read `wip/task-plan.md` and present the plan to the user as a compact numbered list:

```
Proposed plan ([N] tasks):

  1. [task-name] — [one-line description of what it does]
  2. [task-name] — [one-line description]
  ...

Proceed? (yes / edit / cancel)
```

- If **yes**: continue to Phase 3.
- If **edit**: accept the user's changes, update the affected `wip/task-NNN-brief.md` files, then continue.
- If **cancel**: stop and confirm cancellation. Do not delete the wip/ folder.

---

## Phase 3: Skill Research

For each task in the plan (process in dependency order — tasks with no dependencies first):

1. Invoke `agents/skill-researcher.md` with:
   - `task_brief_path`: path to `wip/task-NNN-brief.md`
   - `task_name`: the task name
   - `skill_type_needed`: the skill type from the task plan

2. The researcher writes its verdict back into the task brief. Collect the one-line result.

3. After all tasks are researched, print a research summary:
```
Skill Research Results:
  ✓ [task-name] → FOUND_LOCAL: [skill-name]
  ✓ [task-name] → FOUND_REMOTE: [skill-name] ([N] installs)
  ✗ [task-name] → NOT_FOUND — will create new skill
```

---

## Phase 4: Skill Provisioning

Process each task's provisioning based on its research verdict:

### FOUND_LOCAL
No action needed. Note in the task brief that the local skill will be used.

### FOUND_REMOTE
1. Read the task brief's Skill Research section.
2. Load `references/safety-criteria.md` and evaluate the skill against all five mandatory criteria plus the three optional flags.
3. Produce the safety evaluation block (format defined in safety-criteria.md).
4. If the overall verdict is **UNSAFE — DO NOT INSTALL**: downgrade the task to NOT_FOUND and proceed to the NOT_FOUND flow below.
5. If verdict is **SAFE TO RECOMMEND**: present to the user:

```
Found skill for task [task-name]:

  Name:          [skill-name]
  Source:        [URL]
  Installs:      [N]
  Description:   [one sentence from the skill]
  Install cmd:   npx skills add [owner/repo@skill-name] -g -y

  Safety: [SAFE TO RECOMMEND]
  [List any optional flags if present]

Install this skill? (yes / no)
```

   - If **yes**: run `npx skills add [owner/repo@skill-name] -g -y`. Confirm installation succeeded. Update the task brief.
   - If **no**: downgrade the task to NOT_FOUND and proceed to the NOT_FOUND flow.

### NOT_FOUND
1. Load `references/skill-creator-brief-template.md`.
2. Fill in every field using the task's information from `wip/task-NNN-brief.md`.
3. Inform the user:
   > "No existing skill found for [task-name]. I'll ask skill-creator to build one."
4. Invoke skill-creator with the completed brief as input. Wait for skill-creator to complete and return the new skill's name and location.
5. Update the task brief: fill in `Assigned skill` and `Skill source: CREATED`.

---

## Phase 5: Workflow Execution

Execute tasks in dependency order (tasks with no dependencies first; parallel execution is acceptable for tasks with no shared dependencies).

For each task:

1. Read `wip/task-NNN-brief.md` — confirm inputs are available, skill is assigned, output filename is defined.
2. Invoke the assigned skill with the task's input context. The input may be:
   - Files from `outbox/` (user-provided source material — the only external source Skiller reads)
   - The content of an earlier task's output file (`wip/task-MMM-output.*`)
   - The user's original requirement text
3. Direct the skill to write its output to `wip/task-NNN-output.[ext]` as specified in the task brief.
4. Confirm the output file exists and is non-empty.
5. Update the task brief: fill in Execution Notes (started, completed, fallback used, output confirmed) and Status Report.
6. Print a step completion line:
   ```
   ✓ Task 001: [task-name] → wip/task-001-output.md
   ```

**On task failure:**
- Attempt once more with simplified or re-framed input.
- If it fails a second time: stop execution and report:
  ```
  ✗ Task [NNN]: [task-name] FAILED
  Reason: [brief explanation]
  Options: retry / skip this task / cancel the job
  ```
- Accept the user's choice and act accordingly.

---

## Phase 6: Output Assembly

1. Read all `wip/task-NNN-output.*` files in task order.
2. Synthesize or concatenate them into final deliverable(s) according to the requirement's output format:
   - If the requirement asked for a single document: merge intelligently (not just append).
   - If the requirement asked for multiple files: write one file per logical unit.
   - Preserve attribution and structure from source tasks.
3. Write assembled file(s) to a temporary path inside `wip/` first (e.g., `wip/final-[name].[ext]`).
4. Run the post-processing script on every assembled file before delivery:
   ```
   python .agents/skills/skiller/scripts/clean-output.py wip/final-[name].[ext]
   ```
   The script removes invisible characters, normalizes em dashes, smart quotes, and other common AI text aberrations. Review its output — it will list every change made.
5. Copy the cleaned file(s) to `inbox/[descriptive-filename].[ext]`. Use meaningful filenames based on the requirement topic.
6. Print a manifest:
   ```
   Output ready in inbox/:
     inbox/[filename-1]  ([word count or line count])
     inbox/[filename-2]  ([word count or line count])
   ```

---

## Phase 7: Feedback Collection

Invoke `agents/feedback-collector.md` with:
- `inbox_dir`: path to `inbox/`
- `wip_dir`: path to `wip/`
- `requirement`: the confirmed one-sentence requirement

The feedback collector will ask the user between 1 and 5 questions and write `wip/feedback-summary.md`. Wait for it to complete.

---

## Phase 8: Retrospective and Changelog

**Skill updates:**
For each skill listed in `wip/feedback-summary.md` under "Skills to Update":
- Invoke skill-creator in "improve" mode, passing the skill name and the relevant feedback from the summary.
- This refines the skill for future use.

**Changelog:**
1. Load `templates/changelog-entry.md`.
2. Fill one instance with this session's data:
   - Date, requirement, working directory, outcome
   - Tasks executed table (from task-plan.md)
   - Skills installed (if any)
   - Skills created (if any)
   - Skills updated (if any)
   - Output files manifest
   - Key insights from wip/feedback-summary.md
3. Append the filled entry to `logs/changelog.md`. Create the file if it does not exist.
4. Print a final session summary:

```
SKILLER — Session complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Requirement:  [one-sentence requirement]
Tasks run:    [N] ([N passed] / [N failed])
Skills used:  [list]
inbox/:       [filenames delivered]
Logged:       logs/changelog.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Required skill (find-skills, skill-creator) missing | Phase 0: print install instructions, stop |
| Working directory not writable | Phase 0: report error, stop |
| Task fails twice | Phase 5: ask user retry / skip / cancel |
| Skill install fails (npx error) | Phase 4: report error, ask user whether to create skill instead |
| skill-creator returns no skill | Phase 4: note in task brief, execute task using built-in capability with a best-effort approach |
| inbox/ already has files from a prior session | Do not overwrite — use a timestamped subfolder: `inbox/YYYY-MM-DD-HH-MM/` |

## Acceptance Criteria

A Skiller session is considered successful when:
- [ ] All tasks in the plan completed with status PASS
- [ ] At least one file exists in `inbox/` and is non-empty
- [ ] `wip/feedback-summary.md` exists and contains at least one Q&A pair
- [ ] `logs/changelog.md` contains a new entry for this session
