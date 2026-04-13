# docs-lead — persistent agent memory

Curated by docs-retrospector (writes to staging/) and docs-lead (merges).

---

## Starter playbook

### Reader-before-writer is the core accuracy mechanism
- **Observed in**: docs-knowledge-team-self-evolve-v1 (2026-04-13)
- **Lesson**: DocAgent paper showed topological code processing achieves 95.7% truthfulness vs 61.1% for chat-based. Always dispatch docs-reader before docs-writer.
- **Rule of thumb**: no reader.md, no writer dispatch.

### Detection before planning is mandatory
- **Observed in**: docs-knowledge-team-self-evolve-v1 (2026-04-13)
- **Lesson**: without auto-detection, every session guesses doc format, test framework, conventions. Detection eliminates guessing.
- **Rule of thumb**: always dispatch docs-detector at Round 0.
