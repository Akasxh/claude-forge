# research-retrospector — meta-lessons about retrospection

This is the retrospector's own memory: lessons about *how* to write
lessons, not lessons about research topics.

---

## Starter meta-playbook (seeded 2026-04-12)

### Durability test: would this lesson apply in 3 months to an unrelated question?
- **Rule**: kill session-specific findings. Keep transferable process lessons.
- **Example keep**: "Skeptic must run before adversary when sources are
  community-sourced, because skeptic's unstated-assumption audit seeds the
  adversary's corpus-capture check."
- **Example kill**: "For the vllm-moe-routing session, the github-miner
  found a relevant PR at #12345." (That's a finding; it belongs in SYNTHESIS.md.)

### Fewer stronger lessons beat more brittle ones
- **Rule**: 3 durable lessons per session is the sweet spot. 7 is the max.
  Below 3, the session was probably too short to teach anything. Above 7,
  most are probably brittle.
- **Counter-example**: a session that explicitly investigated team process
  (like the self-evolve- sessions) may legitimately produce 10+ durable
  lessons because process *is* the subject matter.

### Merge, don't duplicate
- **Rule**: before adding a new lesson, diff against existing MEMORY.md.
  If there's a semantic overlap, strengthen the existing entry via
  `Reinforced by` rather than creating a new one.
- **Bounds**: "overlap" means same rule-of-thumb, not just same topic.
  Two lessons about the skeptic can coexist if one is about timing and
  the other is about scope.
