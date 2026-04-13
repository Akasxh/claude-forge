# testing-lead — persistent agent memory

Curated by testing-retrospector (writes to staging/) and testing-scribe (merges via flock+timeout+atomic-rename).
Read first 200 lines at session start.

---

## Starter playbook (seeded 2026-04-12 from Testing/QA Team design session)

### Detector runs FIRST — no test generation without a project profile
- **Observed in**: testing-qa-team-self-evolve-v1 (2026-04-12) — design session prior-art analysis
- **Failure mode addressed**: FM-1.1 (disobey task specification) — generating tests for wrong framework
- **Lesson**: ASTER (IBM, ICSE 2025 Distinguished Paper) demonstrated that static analysis BEFORE LLM prompting is the difference between competitive and inferior test generation. ASTER's preprocessing phase extracts method signatures, call hierarchies, and dependencies — then crafts prompts using these insights. Without this, LLMs generate tests that import wrong modules, use wrong assertion styles, or target wrong test directories. The testing-detector specialist is the ASTER preprocessing phase generalized to any language.
- **Rule of thumb**: testing-detector is dispatched in Round 0, before any other specialist. Its output (EVIDENCE/detector.md) is a mandatory input to planner, writer, property, fixture, and runner. No exceptions.
- **Counter-example / bounds**: if the user explicitly specifies the framework and conventions ("write pytest tests for src/auth.py"), the detector's role shrinks to verification — confirm the user's claim and fill in coverage baseline. It still runs.

### 3x test execution catches LLM-generated flakiness at 63% root cause rate
- **Observed in**: testing-qa-team-self-evolve-v1 (2026-04-12) — arxiv 2601.08998 (SAP HANA + DuckDB + MySQL + SQLite empirical study)
- **Failure mode addressed**: FM-2.6 (reasoning-action mismatch) — test says PASS but is flaky
- **Lesson**: LLM-generated tests have a HIGHER flakiness rate than human-written tests. The dominant cause (63% of 115 flaky tests) is reliance on non-guaranteed ordering — iterating over sets/dicts/unordered collections and asserting on specific positions. LLMs transfer flakiness patterns from the prompt context (existing tests) to generated tests. Running 3x catches non-deterministic passes. The testing-runner specialist's 3x execution pattern is calibrated against this empirical finding.
- **Rule of thumb**: testing-runner runs every new test 3 TIMES. Any test that passes < 3/3 is classified FLAKY and must be fixed before the evaluator sees it. The 3x pattern is a minimum — for timing-dependent tests, consider 5x or 10x with jitter.
- **Counter-example / bounds**: pure unit tests with no I/O, no randomness, and no concurrency are unlikely to be flaky. 1x is sufficient for deterministic pure-function tests, but 3x is cheap insurance.

### Property-based + example-based hybrid catches 81.25% of bugs vs 68.75% each alone
- **Observed in**: testing-qa-team-self-evolve-v1 (2026-04-12) — arxiv 2510.25297 (HumanEval empirical study)
- **Failure mode addressed**: FM-3.2 (incomplete verification) — example tests miss edge cases
- **Lesson**: neither property-based testing nor example-based testing alone is sufficient. PBT excels at finding performance issues and edge cases through input space exploration. EBT excels at detecting specific boundary conditions and special patterns. The 12.5% improvement from combining both is the testing-property specialist's raison d'etre.
- **Rule of thumb**: for functions with many valid inputs (string processors, numeric computations, data transformers), dispatch BOTH testing-writer AND testing-property. The planner should flag these targets in the test plan. For functions with few valid inputs (configuration switches, enum handlers), example-based tests alone are sufficient.
- **Counter-example / bounds**: PBT is expensive for functions with complex preconditions (valid JWT tokens, well-formed SQL queries). When the input generator is harder to write than the tests, skip PBT and write thorough examples instead.

### Over-mocking is the #1 LLM test generation anti-pattern
- **Observed in**: testing-qa-team-self-evolve-v1 (2026-04-12) — Meta TestGen-LLM + ACH research + Diffblue 2025 benchmark
- **Failure mode addressed**: FM-3.3 (incorrect verification) — tests verify mocks, not code
- **Lesson**: Meta's research shows "the mock is broken (LLM generated it wrong)" as a primary false-positive cause. The testing-skeptic's Attack 1 (over-mocking audit) is the primary defense. The rule: mock EXTERNAL dependencies (DB, API, filesystem, network). Do NOT mock internal collaborators (pure functions, data transformers, validators in the same module). A test that mocks the function under test's direct collaborators is testing the mock, not the code.
- **Rule of thumb**: testing-fixture classifies every dependency as EXTERNAL (mock) or INTERNAL (don't mock). The skeptic audits this classification. When in doubt, don't mock — use the real implementation and make the test an integration test.
- **Counter-example / bounds**: some internal collaborators have expensive side effects (writing to disk, sending emails). These get mocked at the BOUNDARY — mock the I/O call, not the business logic function that calls it.

### Mutation score is the ground truth for test quality, not coverage %
- **Observed in**: testing-qa-team-self-evolve-v1 (2026-04-12) — Meta ACH (FSE 2025), accepted 73% by engineers
- **Failure mode addressed**: FM-3.2 (incomplete verification) — 100% coverage with 0% mutation kill
- **Lesson**: Meta's ACH system demonstrated that mutation-guided test generation produces tests that find bugs coverage metrics miss. Coverage tells you "this line was executed." Mutation score tells you "the tests would fail if this line were wrong." A test suite can have 100% line coverage and 50% mutation score — meaning half the code could be wrong without any test catching it. The testing-evaluator's Dimension 5 (mutation score) captures this.
- **Rule of thumb**: for comprehensive-tier sessions, mutation testing is MANDATORY. For coverage-tier, it's recommended on P0 targets. The evaluator treats mutation score as advisory (not strict) because mutation testing is computationally expensive, but a low score is a STRONG signal that the tests need strengthening.
- **Counter-example / bounds**: trivial code (getters, setters, simple forwarding) has low mutation value — most mutants are equivalent. Focus mutation testing on business logic, error handling, and security-critical code.

### Match the project's existing conventions — never impose new ones
- **Observed in**: testing-qa-team-self-evolve-v1 (2026-04-12) — ASTER user study (70% adoption with minor/no changes when matching style)
- **Failure mode addressed**: FM-2.3 (task derailment) — generating tests in wrong style
- **Lesson**: ASTER's user study with 161 developers showed 70% willing to adopt generated tests with "minor or no changes." The key factor: tests that MATCH existing project conventions. The testing-detector discovers conventions; every generator follows them. If the project uses pytest with conftest.py fixtures, generate pytest with conftest.py fixtures. If the project uses Jest with beforeEach, generate Jest with beforeEach. Introducing a new framework or style is task derailment.
- **Rule of thumb**: the detector's project profile is binding on every generator. If the project has no tests (greenfield), the detector recommends community-standard conventions for the language. The planner may override ONLY with documented justification.
- **Counter-example / bounds**: if existing conventions are actively harmful (e.g., all tests in one file, no assertions, mocking everything), the planner may recommend a migration — but this is a separate task, not part of test generation.

### Adopted-persona pattern 2 is universal to team leaders
- **Inherited from**: research-lead MEMORY.md, reinforced by engineering-team-self-evolve-v1
- **Failure mode addressed**: architectural constraint (subagents cannot spawn subagents)
- **Lesson**: when testing-lead is invoked as a subagent, it cannot dispatch specialists. It reads specialist files as behavioral contracts and executes their methods directly. The protocol's gates still hold. Copy the pattern verbatim from research-lead and engineering-lead.
- **Rule of thumb**: specialist files are specs, not just dispatching targets. In adopted-persona mode, execute the spec, write the output file, proceed through the gate sequence.
- **Counter-example / bounds**: only applies while subagent-spawn is architecturally blocked.
