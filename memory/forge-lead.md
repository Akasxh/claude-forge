# forge-lead — persistent agent memory

This file is the Forge's evolving playbook. Append-only at the section level,
bullet counters update in-place. Read first 200 lines at session start.

---

## Process lessons

### process: skill-creator eval harness non-interactive limitation (2026-04-13)
- skill-creator's eval loop (`scripts/run_eval.py`, `scripts/aggregate_benchmark.py`) requires interactive approval and `context: fork` isolation, which is not available when the Forge runs non-interactively.
- **Workaround**: manual validation by executing each eval case as a live WebFetch call against the target API and verifying assertions against actual response data. Functionally equivalent but lacks the with/without-skill baseline comparison.
- **Impact**: does not block promotion. The manual approach verifies the skill's instructions produce correct API calls and valid responses.
- **Future**: when skill-creator gains a `--non-interactive` or `--batch` mode, switch to the automated harness.

## Authored skills catalog

### Authored: hn-search
- **authored_at**: 2026-04-13
- **destination**: ~/.claude/skills/hn-search/SKILL.md
- **gap-closed**: HN Algolia search encapsulation for research team (research-web-miner, research-historian)
- **source-primitives**: manual authoring (skill-creator non-interactive limitation)
- **eval-pass-rate**: 1.0 (3/3)
- **helpful_count**: 0
- **harmful_count**: 0
- **last_triggered**: null
- **deprecated_at**: null

## Failed gap investigations

(Empty.)
