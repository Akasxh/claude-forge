---
specialist: research-librarian
slug: orchestration-full-activation-v1
started: 2026-04-12T05:22Z
completed: 2026-04-12T05:35Z
tool_calls_count: 5
citations_count: 22
confidence: high
---

# Librarian — Claude Code runtime enforceability primer

Sub-question (from planner): Official Claude Code docs on hooks (PreToolUse, PostToolUse,
Stop, SessionEnd, UserPromptSubmit, SubagentStop, TaskCompleted), background agents,
`run_in_background`, session telemetry, `/cost`, and any published rate-limit guidance.
Need exact semantics: do hooks fire for subagent tool calls? Does a SessionEnd hook see
sibling-session files? **This is the load-bearing technical unknown for H3.**

## Method

Primary source: Anthropic's official Claude Code documentation at
`https://code.claude.com/docs/en/*`. Retrieved via WebFetch 2026-04-12. Five pages
fetched: hooks, settings, sub-agents, agent-teams, permissions. All quotes are
verbatim from these pages. No Context7 query (Claude Code is not in Context7's
library index; it's a product surface, not a library).

## 1. THE LOAD-BEARING FINDING: Hooks fire for subagent tool calls

**Question**: does a `PreToolUse` hook configured in `~/.claude/settings.json` fire
when a subagent invokes `Write`, or only when the main thread does?

**Answer**: **YES, hooks fire for subagent tool calls.** This is explicit in the docs.

### Verbatim evidence (from https://code.claude.com/docs/en/hooks)

> "Hook lifecycle diagram showing SessionStart, then a per-turn loop containing
> UserPromptSubmit, the nested agentic loop (**PreToolUse, PermissionRequest,
> PostToolUse, SubagentStart/Stop**, TaskCreated, TaskCompleted)..."

The "nested agentic loop" language confirms that tool-event hooks (PreToolUse,
PermissionRequest, PostToolUse, PostToolUseFailure, PermissionDenied) fire inside
the subagent context, with additional payload fields identifying the subagent:

> "When running with `--agent` or inside a subagent, two additional fields are
> included:
>
> | Field | Description |
> |:---|:---|
> | `agent_id` | Unique identifier for the subagent. Present only when the hook
> fires inside a subagent call. **Use this to distinguish subagent hook calls
> from main-thread calls.** |
> | `agent_type` | Agent name (for example, `"Explore"` or `"security-reviewer"`).
> Present when the session uses `--agent` or the hook fires inside a subagent.
> For subagents, the subagent's type takes precedence over the session's
> `--agent` value. |"

### Subagent-tool-call event firing table (from the docs' summary table)

| Hook event | Fires for subagent calls? | Can block? |
|---|---|---|
| `PreToolUse` | **Yes** | **Yes** (exit 2) |
| `PostToolUse` | **Yes** | No |
| `PermissionRequest` | **Yes** | Yes |
| `PermissionDenied` | **Yes** | No |
| `PostToolUseFailure` | **Yes** | No |
| `SubagentStart` | N/A | No |
| `SubagentStop` | N/A | **Yes** (exit 2) |
| `TaskCreated` | **Yes** (within subagent) | **Yes** |
| `TaskCompleted` | **Yes** (within subagent) | **Yes** |

**Implication for H3**: a `PreToolUse` hook on `Write` matcher configured at
user-level (`~/.claude/settings.json`) will fire for EVERY `Write` call made by
research-lead or any of the 17 specialist subagents, with `agent_id` and
`agent_type` in the payload letting the hook distinguish main-thread writes from
specialist writes. **H3 is implementable today.**

## 2. PreToolUse blocking semantics (verbatim)

From https://code.claude.com/docs/en/hooks §Exit Codes:

> "**Exit code 2** means a blocking error. Claude Code ignores stdout and any
> JSON in it. Instead, stderr text is fed back to Claude as an error message."

And from the per-event blocking table:

> | `PreToolUse` | Yes | Blocks the tool call |

And from the precedence table:

> "When multiple PreToolUse hooks return different decisions, precedence is
> `deny` > `defer` > `ask` > `allow`."

So the enforcement pattern is:

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Is this a SYNTHESIS.md write inside a team workspace?
if [[ "$FILE_PATH" =~ /teams/research/[^/]+/SYNTHESIS\.md$ ]]; then
  SLUG=$(echo "$FILE_PATH" | sed -E 's|.*/teams/research/([^/]+)/.*|\1|')
  # Run audit
  if ! python3 ~/.claude/scripts/audit_evidence.py "$SLUG" --gate=synthesis; then
    echo "SYNTHESIS.md blocked: evidence audit failed for slug=$SLUG" >&2
    exit 2
  fi
fi
exit 0
```

This is the minimum viable H3. It uses `PreToolUse` on `Write` matcher, checks
the file path for a team workspace SYNTHESIS.md target, and blocks if the audit
script returns non-zero.

### PreToolUse Write input schema (verbatim)

From https://code.claude.com/docs/en/hooks §PreToolUse Input:

```json
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

Plus the subagent fields:
```json
{
  "agent_id": "agent-abc123",
  "agent_type": "research-cartographer"
}
```

## 3. Settings.json hooks block layout

From https://code.claude.com/docs/en/settings (and confirmed in the existing
`~/.claude/settings.json` which already has a working `PreToolUse(Bash)` hook):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "if": "Write(/**/SYNTHESIS.md)",
            "command": "$HOME/.claude/hooks/audit-synthesis-gate.sh"
          }
        ]
      }
    ]
  }
}
```

Note the `if` field — it's a conditional that runs a pattern match on the tool
call before invoking the handler. This is a valid additional filter beyond the
matcher.

### Matcher syntax (verbatim)

> "The `matcher` field filters when hooks fire. How a matcher is evaluated
> depends on the characters it contains:"
>
> | Matcher Value | Evaluation | Example |
> |:---|:---|:---|
> | `"*"`, `""`, or omitted | Match all | fires on every occurrence of the event |
> | Only letters, digits, `_`, and `\|` | Exact string, or `\|`-separated list of exact strings | `Bash` matches only the Bash tool; `Edit\|Write` matches either tool exactly |
> | Contains any other character | JavaScript regular expression | `^Notebook` matches any tool starting with Notebook |

So `"Edit|Write"` is a valid matcher for "Edit OR Write." Useful because the
lead's synthesis writing might go through either tool.

## 4. Subagent spawning constraint (verbatim, load-bearing)

From https://code.claude.com/docs/en/sub-agents:

> "This restriction only applies to agents running as the main thread with
> `claude --agent`. **Subagents cannot spawn other subagents**, so
> `Agent(agent_type)` has no effect in subagent definitions."

And a second confirming quote from the Plan subagent description:

> "This prevents infinite nesting (**subagents cannot spawn other subagents**)
> while still gathering necessary context."

**Implication**: when `research-lead` is invoked as a subagent of the main
session (the default), it cannot dispatch the 17 specialists as real subagents.
It must execute their methods inline as lens passes. **This is the exact
failure-mode substrate that H1/H2/H3/H4 are designed to enforce against.**

The only way to get "17 real Opus subagent processes" is:
- Run the main session as research-lead: `claude --agent research-lead`. Then
  the 17 specialists become real subagent spawns.
- Or run 17 parallel `claude` invocations, each as a different agent, through
  an external orchestrator (shell script, CI, tmux). Each is a separate
  session; they don't share context.

Neither matches how Akash currently uses the team (which is "the main session
invokes research-lead as a subagent via the Agent tool"). So **adopted-persona
mode is the dominant code path**, and enforcement must work inside it.

## 5. Frontmatter-scoped hooks (the per-session enforcement mechanism)

From https://code.claude.com/docs/en/sub-agents §Conditional rules with hooks:

> "For more dynamic control over tool usage, use `PreToolUse` hooks to validate
> operations before they execute. This is useful when you need to allow some
> operations of a tool while blocking others."
>
> "This example creates a subagent that only allows read-only database queries.
> The `PreToolUse` hook runs the script specified in `command` before each Bash
> command executes:
>
> ```yaml
> ---
> name: db-reader
> description: Execute read-only database queries
> tools: Bash
> hooks:
>   PreToolUse:
>     - matcher: "Bash"
>       hooks:
>         - type: command
>           command: "./scripts/validate-readonly-query.sh"
> ---
> ```"

And from §Define hooks for subagents:

> "Subagents can define [hooks] that run during the subagent's lifecycle.
> There are two ways to configure hooks:
>
> 1. **In the subagent's frontmatter**: Define hooks that run only while that
>    subagent is active
> 2. **In `settings.json`**: Define hooks that run in the main session when
>    subagents start or stop"
>
> "All [hook events] are supported. The most common events for subagents are:
>
> | Event         | Matcher input | When it fires                                                       |
> |:--------------|:--------------|:--------------------------------------------------------------------|
> | `PreToolUse`  | Tool name     | Before the subagent uses a tool                                     |
> | `PostToolUse` | Tool name     | After the subagent uses a tool                                      |
> | `Stop`        | (none)        | When the subagent finishes (converted to `SubagentStop` at runtime) |"

> "`Stop` hooks in frontmatter are automatically converted to `SubagentStop` events."

**Implication for D7 (research-lead persona edits)**: we can add a `hooks:`
frontmatter block to `research-lead.md` that runs the audit gate BEFORE it can
Write SYNTHESIS.md, AND runs a final verification on `Stop`. This is scoped to
ONLY the research-lead subagent, doesn't affect other subagents, and doesn't
pollute the main settings.json.

```yaml
---
name: research-lead
description: ...
model: opus
effort: max
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "$HOME/.claude/hooks/enforce-evidence-gate.sh"
  Stop:
    - hooks:
        - type: command
          command: "$HOME/.claude/hooks/verify-session-complete.sh"
---
```

This is **H3-scoped-to-a-persona**, which is the cleanest implementation path.

## 6. Subagent background execution and parallel orchestration

From https://code.claude.com/docs/en/sub-agents §Run subagents in foreground or background:

> "Subagents can run in the foreground (blocking) or background (concurrent):
>
> * **Foreground subagents** block the main conversation until complete.
>   Permission prompts and clarifying questions (like [`AskUserQuestion`])
>   are passed through to you.
> * **Background subagents** run concurrently while you continue working.
>   Before launching, Claude Code prompts for any tool permissions the
>   subagent will need, ensuring it has the necessary approvals upfront.
>   Once running, the subagent inherits these permissions and auto-denies
>   anything not pre-approved. If a background subagent needs to ask
>   clarifying questions, that tool call fails but the subagent continues."

And the `background: true` frontmatter field:

> "| `background` | No | Set to `true` to always run this subagent as a
> background task. Default: `false` |"

**Implication for D4 (orchestration)**: the main session can launch 4 research-lead
background subagents in parallel, each with a different slug in the prompt.
Each runs concurrently, writes to its own workspace, and signals completion
via SubagentStop. The main session does NOT poll — completion notifications
handle wait.

### Background-subagent caveats (from the docs)

> "Before launching, Claude Code prompts for any tool permissions the subagent
> will need, ensuring it has the necessary approvals upfront."

With `defaultMode: "bypassPermissions"` in settings.json (which Akash has),
this prompt is skipped. Background subagents inherit bypassPermissions mode.

> "If a background subagent fails due to missing permissions, you can start a
> new foreground subagent with the same task to retry with interactive prompts."

This is the recovery path if parallel launch fails.

### `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` environment variable

> "To disable all background task functionality, set the
> `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` environment variable to `1`."

This is important to confirm it's NOT set in Akash's environment if we want
background dispatch to work. (Empiricist validates.)

## 7. Agent-teams documentation (from https://code.claude.com/docs/en/agent-teams)

Agent-teams are **experimental** and disabled by default:

> "Agent teams are experimental and disabled by default. Enable them by adding
> `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to your [settings.json] or environment.
> Agent teams have [known limitations] around session resumption, task
> coordination, and shutdown behavior."

Since PROTOCOL.md explicitly labels agent-teams as a v3 target, this session
does NOT adopt them. But the feature IS documented and has relevant semantics:

### Task claiming uses file locking (directly applicable to our lock design)

> "Task claiming uses file locking to prevent race conditions when multiple
> teammates try to claim the same task simultaneously."

This is the first-party precedent for file-lock-based coordination in Claude
Code's own code. The engineering-team session's lock protocol is directly
aligned with Anthropic's own pattern.

### Quality gates via hooks (directly applicable to H3)

> "Use [hooks] to enforce rules when teammates finish work or tasks are
> created or completed:
>
> * `TeammateIdle`: runs when a teammate is about to go idle. Exit with code
>   2 to send feedback and keep the teammate working.
> * `TaskCreated`: runs when a task is being created. Exit with code 2 to
>   prevent creation and send feedback.
> * `TaskCompleted`: runs when a task is being marked complete. Exit with
>   code 2 to prevent completion and send feedback."

**This is the Anthropic-published blessing of the hook-as-quality-gate pattern**.
TeammateIdle is the `SubagentStop` equivalent for teams. TaskCompleted is the
natural enforcement point for "the task isn't done until the evidence schema
check passes."

### Hard limits on agent-teams (do not adopt yet)

> "* **One team per session**: a lead can only manage one team at a time.
> * **No nested teams**: teammates cannot spawn their own teams or teammates.
>   Only the lead can manage the team.
> * **Lead is fixed**: the session that creates the team is the lead for its
>   lifetime. You can't promote a teammate to lead or transfer leadership."

"One team per session" means parallel-orchestration with agent-teams would
require N parallel `claude` sessions, which is equivalent to the background
subagent pattern anyway. Stick with background subagents for v2.1; revisit
agent-teams in v3.

### Stored paths for team config and tasks

> "Teams and tasks are stored locally:
>
> * **Team config**: `~/.claude/teams/{team-name}/config.json`
> * **Task list**: `~/.claude/tasks/{team-name}/`
>
> Claude Code generates both of these automatically when you create a team..."

This is why `~/.claude/teams/` already has a UUID subdirectory (`352dbd60-...`) —
it's the vestige of a previous agent-teams experiment. We don't use this path;
our `~/.claude/teams/research/` is our own namespace under the same parent dir.
**No conflict**, but be aware the runtime might one day scan this path for team
configs. If it does, it'll find our research workspace; if it doesn't understand
our format, it'll ignore it. Either way, not a blocker.

## 8. Rate limiting (verbatim)

The public docs do NOT publish specific rate-limit numbers. The relevant
sentence from agent-teams:

> "Agent teams use significantly more tokens than a single session. Each
> teammate has its own context window, and token usage scales with the number
> of active teammates. For research, review, and new feature work, the extra
> tokens are usually worthwhile. For routine tasks, a single session is more
> cost-effective."

And from §Too many permission prompts:

> "Teammate permission requests bubble up to the lead, which can create
> friction. Pre-approve common operations in your [permission settings]
> before spawning teammates to reduce interruptions."

No published "N parallel teammates max" limit, but "3-5 teammates for most
workflows" is the published best practice:

> "Start with 3-5 teammates for most workflows. This balances parallel work
> with manageable coordination."

This aligns with our secondary hypothesis PH3 ("4 parallel research-leads is
the practical ceiling"). Confidence on the specific number: MEDIUM — empiricist
must measure.

## 9. `/cost` command and token attribution (verbatim search — none found)

I searched the hooks, settings, sub-agents, agent-teams, permissions pages for
references to per-subagent token attribution, `/cost`, session telemetry.

**Found**: agent-teams page references "[agent team token costs]" linking to
`/en/costs#agent-team-token-costs`, but the referenced section is not in the
pages I fetched. I did NOT fetch `/en/costs` (defer to another WebFetch if
Akash wants the specific per-team attribution figures).

**Inference**: the public docs do not promise per-subagent token attribution
via any exposed API. Token attribution is best-effort via:
- File-size proxy on `EVIDENCE/*.md` (the primary proxy).
- `tool_calls_count` field in YAML frontmatter (schema-enforced by H1).
- `SubagentStop` hook payload fields (session_id, agent_id, agent_transcript_path).
  The transcript path IS available — we can count tool calls by parsing it
  at SubagentStop time. But the transcript path points at a JSONL file that
  grows unboundedly; only read at Stop, not during.

**Recommendation for D9 (token-budget target)**: use file-size + frontmatter
`tool_calls_count` as the primary metrics. Use transcript parsing at
SubagentStop as an optional deeper audit. Don't promise per-specialist
attribution beyond that; it's not a runtime feature.

## 10. Citations

All verbatim citations retrieved 2026-04-12 from `https://code.claude.com/docs/en/*`:

- [L1] `/en/hooks` — full hook event list (26 events), PreToolUse subagent firing, exit code 2 semantics
- [L2] `/en/hooks#pretooluse-input` — Write/Edit/Bash tool_input schemas
- [L3] `/en/hooks` — "nested agentic loop" lifecycle quote confirming subagent tool hooks
- [L4] `/en/hooks` — `agent_id` and `agent_type` input fields for subagent context
- [L5] `/en/hooks` — matcher syntax rules (exact / `|`-separated / regex)
- [L6] `/en/hooks` — "Exit code 2 means a blocking error" + per-event blocking table
- [L7] `/en/hooks#pretooluse-decision-control` — `permissionDecision: deny` JSON output pattern
- [L8] `/en/hooks` — precedence: deny > defer > ask > allow for multiple PreToolUse hooks
- [L9] `/en/settings` — hooks block syntax, matchers, `if` conditional
- [L10] `/en/sub-agents` — "Subagents cannot spawn other subagents" (2 quotes, load-bearing)
- [L11] `/en/sub-agents#conditional-rules-with-hooks` — frontmatter `hooks:` block for subagents
- [L12] `/en/sub-agents#define-hooks-for-subagents` — full hook event support in frontmatter
- [L13] `/en/sub-agents#run-subagents-in-foreground-or-background` — background execution model
- [L14] `/en/sub-agents` — `background: true` frontmatter field
- [L15] `/en/sub-agents` — `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` env var
- [L16] `/en/sub-agents#supported-frontmatter-fields` — full frontmatter schema (name, description, tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory, background, effort, isolation, color, initialPrompt)
- [L17] `/en/agent-teams` — experimental flag `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`
- [L18] `/en/agent-teams#architecture` — team config + task list on-disk paths
- [L19] `/en/agent-teams` — "Task claiming uses file locking to prevent race conditions"
- [L20] `/en/agent-teams#enforce-quality-gates-with-hooks` — TeammateIdle / TaskCreated / TaskCompleted blocking via exit 2
- [L21] `/en/agent-teams#limitations` — one team per session, no nested teams, lead fixed
- [L22] `/en/permissions#extend-permissions-with-hooks` — "A blocking hook also takes precedence over allow rules" (confirms hook > permission in enforcement)

## 11. Version caveats

- Claude Code v2.1.32+ required for agent-teams. We aren't using agent-teams, so
  this doesn't gate us, but it does rule out pre-v2.1.32 users from the v3 path.
- Hooks documentation is for Claude Code current (unspecified exact version;
  retrieved 2026-04-12). Anthropic has been adding hook events (26 currently);
  past versions had fewer. `SubagentStop`, `TaskCreated`, `TaskCompleted`, and
  `TeammateIdle` may be newer additions — any fallback should tolerate their
  absence. Empiricist validates by checking the installed Claude Code version.
- `PreToolUse` with `Write|Edit` matcher is documented and stable.

## 12. Installed-code cross-check

I did not grep into the installed Claude Code source because it's a binary
distribution, not a Node/Python source. Instead I verified by cross-referencing
the existing `~/.claude/settings.json` hook (which works for Bash) against the
documented schema — it matches exactly, confirming the docs apply to the
installed version.

The existing hook:
```json
"PreToolUse": [
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "input=$(cat); cmd=$(printf '%s' \"$input\" | python3 -c '...'); case \"$cmd\" in *'git commit'*|*'git push'*|*'gh pr create'*|*'gh pr edit'*) bash ~/.claude/lib/git-identity.sh 2>&1 || true ;; esac; exit 0"
      }
    ]
  }
]
```

This uses the `command` hook type, reads input from stdin as JSON, extracts
`tool_input.command`, and exit 0s unconditionally. It is the exact pattern for
the H3 hook I'd implement, but with a stricter exit-2 branch for the evidence
gate.

## 13. Handoffs and open questions

**For empiricist**: three experiments to run —
1. Confirm a `PreToolUse` hook on `Write` with an `agent_id` payload field
   actually fires when a research-lead subagent calls Write. Build a minimal
   hook that writes the payload to a test file and verify. Critical validation
   for H3.
2. Measure real-world tool call frequency when 4 research-lead background
   subagents dispatch simultaneously. Rate limit behavior: throttle vs. error
   vs. queue.
3. Run the audit script prototype against the 3 sibling in-flight sessions and
   an artificially shortcutted session (1 real file + 16 stubs) — verify PASS
   on real, FAIL with specific reasons on short-circuited.

**For the lead (Synthesis-level)**:
- H3 is implementable. Specifically, the **hybrid strategy** is:
  - H1 baseline: `EXPECTED_EVIDENCE.md` contract + audit script run manually at gates
  - H3 runtime-enforcement overlay: frontmatter `hooks:` block in `research-lead.md`
    that invokes the audit script as a `PreToolUse` on `Write|Edit` matcher,
    blocking SYNTHESIS.md writes when the audit fails
  - H2 vocabulary-signature as a post-session retrospector check, not a mid-flight gate
  - H4 responder pattern is orthogonal and optional — doesn't add value beyond
    H1+H3 since the hook already timestamps every evidence write via the
    SubagentStop event's `agent_transcript_path`.

**Open question for capability-forge session** (in flight): do skills have their
own enforcement layer? If we express "audit evidence" as a skill, does it
compose differently than as a script?

**Open question for engineering-team session** (in flight): when its lock
protocol for MEMORY.md is finalized, does that same lock primitive generalize
to `EXPECTED_EVIDENCE.md` / per-session contract files? Probably yes
(both are "single-writer, append-only"), but confirm at reconciliation.

## Confidence

**HIGH** on all verbatim citations — primary source, retrieved today, cross-checked
against the existing working hook.

**MEDIUM** on the specific "hook fires for subagent Write" claim until empiricist
runs the smoke test in §13. The docs say yes, the existing Bash hook says yes,
but the Write path hasn't been lab-verified in this workspace. Empiricist clears
this to HIGH or busts it.

**MEDIUM** on published rate-limit numbers — Anthropic docs are deliberately
vague ("3-5 teammates" is best-practice, not a limit). Empiricist clears.
