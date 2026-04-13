# Research Team Protocol

The Research Team is the first fully-collaborative subagent team in this
setup. It is a **leader + 12 specialists** hierarchy, **all running on
Opus 4.6 with max effort** (hard contract, no downgrades ever),
coordinating through **files on disk** rather than through conversational
context.

This document is the contract every team member reads before acting.

## Roster

| Role | Agent name | Lens |
|------|------------|------|
| Leader | `research-lead` | orchestration, arbitration, synthesis |
| Specialist | `research-cartographer` | structural topology |
| Specialist | `research-archaeologist` | git history and decisions (local) |
| Specialist | `research-librarian` | official docs, Context7, HF hub |
| Specialist | `research-tracer` | runtime behavior and causal chains |
| Specialist | `research-empiricist` | real experiments and measurements |
| Specialist | `research-skeptic` | red team, competing hypotheses |
| Specialist | `research-historian` | prior art: arXiv, HN, Reddit, papers |
| Specialist | `research-linguist` | types, naming, idioms |
| Specialist | `research-web-miner` | Playwright scraping + public JSON APIs |
| Specialist | `research-github-miner` | `gh api` REST/GraphQL at scale |
| Specialist | `research-synthesist` | cross-source integration |
| Specialist | `research-scribe` | ledger curator, schema enforcer |

## Model contract (non-negotiable)

Every agent in this team runs on `claude-opus-4-6[1m]` with max effort.
Never dispatch a specialist with a model override. Never "temporarily"
downgrade for budget reasons — there is no budget to save on Max plan,
and quality is the only optimization target.

## Toolbox (who owns what)

| Capability | Primary tool | Owner(s) |
|------------|--------------|----------|
| Static codebase Grep/Read | Grep, Read, Glob | cartographer, tracer, linguist, archaeologist |
| Local git history | `git log/blame/show` via Bash | archaeologist |
| Official library docs | `mcp__plugin_context7_context7__*` | librarian |
| Hugging Face papers | `huggingface-skills:huggingface-papers` | librarian, historian |
| HF datasets / hub | `huggingface-skills:huggingface-datasets`, `hf-cli` | historian, empiricist |
| Browser automation | `mcp__playwright__*` (navigate, evaluate, snapshot, network_requests, click, fill_form) | web-miner |
| JS-rendered scraping | Playwright | web-miner |
| Public JSON APIs (HN Algolia, Reddit, arXiv, S2, OpenAlex, npm, PyPI, crates.io, StackExchange) | WebFetch | web-miner, historian |
| GitHub REST/GraphQL at scale | `gh api`, `gh api graphql` | github-miner |
| GitHub code/issue/PR search | `gh search *` | github-miner, historian (quick checks only) |
| Running real experiments | Bash + any language runtime | empiricist |
| Framing + brainstorming | `superpowers:brainstorming` | research-lead |
| Parallel dispatch pattern | `superpowers:dispatching-parallel-agents` | research-lead |
| Systematic debugging | `superpowers:systematic-debugging` | tracer, empiricist |
| Completion gate | `superpowers:verification-before-completion` | research-lead |

## Site playbooks (web-miner primarily)

- **X.com / Twitter** — Playwright with a logged-in persistent context;
  prefer catching the `/i/api/graphql/...` endpoints via
  `browser_network_requests` over parsing rendered HTML. No scraping of
  logged-out pages (incomplete + brittle).
- **Hacker News** — Algolia API first
  (`hn.algolia.com/api/v1/search` + `items/<id>` for comment trees).
  Only scrape the HTML ranking page if ordering matters.
- **YC companies** — Playwright for the JS-rendered directory; capture
  the `/api/` XHRs for structured JSON. JSON-LD blocks in company pages.
- **Reddit** — `.json` suffix on listing URLs, 60/min per IP.
- **Substack** — `/api/v1/archive?sort=new` + `/api/v1/posts/<slug>`.
- **dev.to** — public REST API at `dev.to/api/articles`.
- **Lobsters** — `lobste.rs/t/<tag>.json`.
- **GitHub trending** — scrape `github.com/trending/<lang>?since=<period>`
  (no API exists).
- **Eng blogs** — `/feed` / `/rss` / `/atom.xml` → JSON-LD → WebFetch HTML.

## Entry point

You never talk to a specialist directly. You talk to `research-lead`. The
lead decides which specialists to dispatch, in what order, and how to
reconcile their findings.

In Claude Code:
```
Agent({ subagent_type: "research-lead", prompt: "<your question>" })
```

## Shared workspace

Every research session lives in its own directory:

```
.claude/teams/research/<slug>/
├── QUESTION.md        # the question, scope, acceptance criteria
├── HYPOTHESES.md      # numbered candidate answers (pre-investigation)
├── EVIDENCE/          # one file per specialist that's been dispatched
│   ├── cartographer.md
│   ├── archaeologist.md
│   ├── librarian.md
│   ├── tracer.md
│   ├── empiricist.md
│   ├── skeptic.md
│   ├── historian.md
│   ├── linguist.md
│   ├── web-miner.md           ← raw corpora under web-miner/raw/
│   ├── github-miner.md        ← raw JSON under github-miner/raw/
│   └── synthesist.md
├── SYNTHESIS.md       # running synthesis, owned exclusively by research-lead
├── LOG.md             # append-only activity log (every agent writes)
└── OPEN_QUESTIONS.md  # unresolved sub-questions
```

Plus a team-wide index:

```
.claude/teams/research/INDEX.md   # one-line summary of every past session
.claude/teams/research/_archive/  # sessions > 90 days with integrated findings
```

## Ownership rules

| File | Who writes | Who reads |
|------|------------|-----------|
| `QUESTION.md` | `research-lead` | everyone |
| `HYPOTHESES.md` | `research-lead` + `research-skeptic` | everyone |
| `EVIDENCE/<name>.md` | only the named specialist | everyone |
| `SYNTHESIS.md` | `research-lead` only | everyone |
| `LOG.md` | everyone (append-only) | everyone |
| `OPEN_QUESTIONS.md` | `research-lead` + any specialist | everyone |
| `INDEX.md` | `research-scribe` only | everyone |

**Nobody edits another specialist's evidence file.** If you disagree with a
finding, raise it in `OPEN_QUESTIONS.md` or via the skeptic, and let
`research-lead` arbitrate.

## Round structure

1. **Framing** — lead writes `QUESTION.md` and seeds `HYPOTHESES.md`.
2. **Dispatch** — lead fires N specialists **in parallel** (one message,
   multiple `Agent` calls).
3. **Return** — each specialist writes to their own `EVIDENCE/*.md` and
   appends one line to `LOG.md`.
4. **Arbitrate** — lead reads evidence files, handles contradictions
   (usually via the skeptic or empiricist).
5. **Synthesize** — lead updates `SYNTHESIS.md`.
6. **Iterate or deliver** — if confidence is not "high" and the acceptance
   criteria aren't met, go to (2). Hard cap: 4 rounds.

## Confidence scale

- **High** — multiple independent specialists converge, skeptic has tried
  and failed to break it, critical experiments have been run.
- **Medium** — specialists agree but the skeptic round hasn't happened, or
  key experiments are deferred.
- **Low** — single-source, or contradictions unresolved, or the evidence
  is indirect.

No "high confidence" without an explicit skeptic pass.

## Citation schema (enforced by `research-scribe`)

- Code: `path/to/file.ts:123`
- Commit: 12+ char sha with quoted message
- Doc: URL + section + retrieval ISO-date
- Experiment: `EVIDENCE/empiricist.md#<anchor>` with raw output
- Prior art: URL + author + year + retrieval date

## Git identity (all agents, all teams)

Before any commit or push, run:
```bash
bash ~/.claude/lib/git-identity.sh
```
It inspects the repo's `origin` remote, matches the owner against your
logged-in `gh` accounts, switches if needed, and sets a **local**
`user.name` / `user.email` from the active `gh` account. The global
`PreToolUse` hook runs it automatically on `git commit` / `git push` /
`gh pr create` — but run it explicitly if you want to be sure.

## Session naming

`<slug>` is a short kebab-case id chosen by `research-lead` from the
question. Examples:
- `vllm-paged-attention-semantics`
- `why-auth-middleware-leaks-tokens`
- `should-we-adopt-turbopack`

If the user is continuing a previous investigation, reuse the slug and
append to existing files — don't start a new directory.

## Escalation

If after 4 rounds the confidence is still not "high", `research-lead` must
return to the user with:
- The best-available answer at current confidence
- An explicit list of what's still unresolved
- A concrete proposal for what would raise confidence (more compute,
  access to X, a decision from the user, etc.)

Never loop silently past 4 rounds.
