# Design report contract

Use this contract for specialist returns and lead synthesis. Adapt presentation length to the user's request; do not expose long internal design monologues.

## Specialist return

- Lens and execution: name, native worker or serial, upstream entrypoint read, additional references or queries used.
- Sources inspected: exact files/lines, Figma URLs/frame identifiers, supplied screenshot names, or runtime routes/captures. State whether each is current code, observed runtime, proposed design, or reference guidance.
- Findings: each includes priority (`P1` task blocked or materially misleading, `P2` meaningful usability/state gap, `P3` optional improvement), evidence, task impact, recommendation, confidence, and needed verification. Treat uncertain risks as risks, not observed failures.
- Source gaps and contradictions: missing frames, inaccessible runtime, unverified metrics, unclear requirements, or conflicting tokens. Identify what would resolve each material gap.

## Lead report

Lead with the recommended outcome and the user's most important design decision. Include:

1. **Scope and execution:** target surface/audience, discovery/design/critique mode and whether implementation was authorized, `native-swarm`, `batched-native-swarm`, or `serial`; which of the three lenses completed and any package/tool gap.
2. **Evidence:** compact source inventory and its limits. Reuse worker findings; identify unresolved contradictions and the basis for decisions. For material specialist disagreements, record competing recommendations, supporting evidence, the chosen direction and remaining uncertainty.
3. **Recommendation:** prioritized changes tied to user tasks. For discovery/design work, include the current versus desired journey where known, proposed workflow/IA, viable options and tradeoffs, and a testable validation plan. Mark research evidence, working hypotheses, and proposals distinctly. For comparison work, a table with information area, current evidence, proposed evidence, recommendation, and priority. Mark unknown or uninspected cells explicitly.
4. **Design/data contract:** only where useful, the needed fields, definitions, state distinctions, existing-system constraints, and proposed examples. Label suggested capabilities and synthetic values.
5. **Verification and artifacts:** what was actually checked, concrete artifact paths, implementation changes if authorized, and remaining validation. A heuristic review is not a full accessibility, performance, or runtime audit.
6. **Caller handoff:** next actionable step and unresolved decisions. For Temari, status is `advisory-ready` or `advisory-partial`; Temari determines acceptance and closeout.

Do not claim that a native swarm ran when only serial analysis occurred. Do not infer customer behavior or system capability from attractive mockups, source matches, or upstream guidelines. Keep private customer data, screenshots, proprietary source, and project-specific briefs out of the public agent repository; report through the authorized caller or its chosen private artifact location.
