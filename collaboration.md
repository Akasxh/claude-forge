# Multi-Session Collaboration Protocol

When multiple Claude Code terminals work on the same project, they coordinate through `.claude/coordination/`. This file defines how sessions discover, claim, and complete work without conflicts.

## Coordination Directory

All coordination lives in `.claude/coordination/` at the project root:

```
.claude/coordination/
  PLAN.md        — Overall plan and architecture (written by orchestrator)
  TASKS.md       — Task board: backlog, in-progress, done, blocked
  LOG.md         — Activity log from all sessions
  REVIEWS.md     — Review queue and feedback
```

## Task Board Format (TASKS.md)

```markdown
## Backlog
- [ ] TASK-1: [description] | files: [owned files] | priority: high/med/low | depends: none
- [ ] TASK-2: [description] | files: [owned files] | priority: high | depends: TASK-1

## In Progress
- [~] TASK-3: [description] | claimed-by: [role] | started: [HH:MM] | files: [owned files]

## Review
- [?] TASK-4: [description] | completed-by: [role] | ready-for-review: [HH:MM] | files: [changed files]

## Done
- [x] TASK-5: [description] | completed: [HH:MM] | reviewed: yes/no

## Blocked
- [!] TASK-6: [description] | blocked-by: TASK-1 | reason: [why]
```

## Rules for All Sessions

### File Ownership
Each task specifies which files it owns. A session MUST NOT edit files owned by another in-progress task. This prevents write conflicts. If you need to touch a file owned by another task, add a note to LOG.md and wait for that task to complete.

### Claiming Tasks
1. Read TASKS.md
2. Find the highest-priority unclaimed task in Backlog that has no unmet dependencies
3. Move it to "In Progress" with your role and timestamp
4. Work ONLY on the files listed in that task

### Completing Tasks
1. Finish all work for the task
2. Run tests for the files you changed
3. Move the task to "Review" in TASKS.md
4. Add an entry to LOG.md: `[HH:MM] [role]: Completed TASK-N — [summary of changes]`
5. Add the task to REVIEWS.md with the list of changed files

### Logging
Every session MUST append to LOG.md when:
- Starting work on a task
- Completing a task
- Encountering a blocker
- Making a decision that affects other tasks
- Finishing a review

Format: `[HH:MM] [role]: [action] — [details]`

### Conflict Prevention
- Never edit a file that another session's in-progress task owns
- Never move another session's task without their consent (via LOG.md)
- If you discover a conflict, STOP and log it — don't try to merge manually
- Use `git stash` if you need to temporarily set aside changes

## Session Roles

### Orchestrator (Terminal 1)
- Analyzes the project and creates the initial PLAN.md
- Breaks the plan into tasks in TASKS.md
- Monitors LOG.md for blockers and coordinates between sessions
- Can also implement tasks when workers are busy
- Resolves blocked tasks and re-prioritizes as needed

### Worker (Terminal 2, 3, ...)
- Reads TASKS.md and claims the next unclaimed task
- Implements the task within its owned files
- Runs tests and moves task to Review when done
- Claims the next task and repeats

### Reviewer (optional dedicated terminal)
- Watches REVIEWS.md for completed tasks
- Reviews code changes for correctness, security, and style
- Writes feedback in REVIEWS.md under the task entry
- Moves reviewed tasks to Done (or back to In Progress with feedback)

### Tester (optional dedicated terminal)
- Watches for tasks moved to Review or Done
- Writes comprehensive tests for new/changed code
- Runs the full test suite and reports results in LOG.md
- Files test-related bugs as new tasks in TASKS.md

## Starting a Collaboration Session

### First terminal (Orchestrator):
1. Analyze the project
2. Ask the user what to build
3. Create `.claude/coordination/` with PLAN.md and TASKS.md
4. Tell the user how many worker terminals to open

### Subsequent terminals (Workers/Reviewer/Tester):
1. Read `.claude/coordination/TASKS.md`
2. Announce your role in LOG.md
3. Start working according to your role
4. Keep TASKS.md and LOG.md updated as you work
