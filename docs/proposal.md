# Proposal: an external UI Design agent for Temari

Revision 002 adds durable fresh-thread awareness and explicit Temari SME workflow routing. Akamaru review of revision 001 is pending; this revision will be submitted as a separate append-only bridge file.

## User outcome

A user can give Temari the repository URL, install the package through the supported Codex host plugin mechanism, and ask one specialist to help define an experience, design a flow, compare proposals, or critique an existing interface. The agent uses three pinned design skill libraries and returns one coherent recommendation. It can use independent native workers when available.

## Product scope

| Mode | Typical request | Useful deliverable |
| --- | --- | --- |
| Discover the experience | “What should this screen do for an operator?” | Goals and user tasks, constraints, journey, prioritized content and open assumptions |
| Design an experience | “Help us work out this flow” | Information architecture, happy and alternate paths, state/permission matrix, wireframe or interaction specification, options and tradeoffs |
| Compare and critique | “Review current UI against these Figma proposals” | Evidence-linked comparison, prioritized findings, concrete changes and rationale |
| Recommend and validate | “Which direction should we use?” | Recommended direction, confidence, dependencies, observable success criteria and a usability-test plan |
| Implement when requested | “Build this approved flow” | Scoped changes with implementation verification delegated back through Temari's engineering route |

Discovery must distinguish observed research from assumptions. The agent can propose a research plan but cannot call hypothetical personas, needs, or behavior validated research. Recommendations must explain impact, supporting evidence, tradeoffs, and how to check them. Visual frame review cannot prove runtime keyboard behavior, accessibility conformance, performance, or backend telemetry.

## Architecture decision

| Candidate | Advantages | Costs and limits | Decision |
| --- | --- | --- | --- |
| Separate host plugin with coordinator skill and package-local worker briefs | Documented host Git URL installation, self-contained three-skill payload, simple public surface, separate payload ownership | Host-native workers and Figma/browser access depend on installed capabilities; serial fallback needs explicit reporting | Use for v1 |
| Dedicated MCP agent service with its own model orchestration | Explicit callable service, potentially usable across different hosts | Server operation, model credentials, authorization and artifact transport, duplicate lifecycle ownership | Defer until a cross-host service requirement justifies it |
| Add a generic external-agent registry to Temari | A literal Temari install-agent command | Changes Temari's contract, source and admission behavior; larger independent feature | Outside this package's v1 scope |

The external agent is advisory. Temari retains user intent, route admission, engineering delegation and final acceptance. Giving a GitHub URL is a conversational installation request; v1 does not introduce a `temari install-agent` command or imply that installation proves any host capability.

## Package and interfaces

- One coordinator `ui-design` skill, with the three complete upstream libraries nested inside its folder. Native plugin registration and skill discovery must be tested separately; copying a skill folder does not prove native plugin installation.
- Interface Design specialist owns visual structure, hierarchy, components and interaction consistency.
- UI UX Pro Max specialist owns tasks, journeys, usability, accessibility guidance and focused catalog searches.
- Impeccable specialist owns critique, clarity, cognitive load, exception states and refinement.
- All specialists receive the same brief and source map. They work read-only for proposal review and inherit the host model. Their briefs are loaded into generic host workers, not assumed to be auto-registered custom roles.
- The coordinator settles disagreements against user goals, existing design-system truth and evidence, then returns one report. Use only the host's available concurrency; batch or run serially when needed.
- `dependencies.lock.json` records source URLs, immutable commits, licenses and SHA-256 payload inventories.
- Host plugin commands install the inspected package. A Python installer resolves an explicit revision, validates the checkout, installs that pinned commit and reads back the installed payload. It runs no upstream hooks or Impeccable binary.

## Delivery plan and throughput checkpoint

- [x] Ground the three upstream libraries and current Temari dependency boundary. Existing source inspection found a host plugin/skill boundary, not a generic agent registry.
- [x] Draft the discovery/design/critique contract and run an independent local Poteto method review.
- [x] Submit revision 001 to the actual Akamaru/Muse instance through the Google Drive bridge; upload and document contents were read back.
- [ ] Submit revision 002 with the new fresh-thread SME requirements. Record the matching response and resolve material findings before publication. Akamaru review is pending; a local agent cannot substitute for it.
- [ ] Build the package, deterministic verification and URL installer. Preserve vendor files unchanged.
- [ ] Add a bounded external-SME intake reference to Temari and direct Poteto conversational entries; rebuild and verify the host bundle. Keep protected worker skill-discovery restrictions intact.
- [ ] Exercise fresh-context experience-design, UI engineering, QA and unrelated-backend requests with the actual coordinator and specialist prompts, and evaluate output against task-specific acceptance criteria.
- [ ] Publish the authorized public repository and test a fresh installation from its GitHub URL. Record limitations and reproducible evidence.

Throughput checkpoint:

1. Blocking first steps. Review the experience scope and integration boundary before publishing. Verify licenses and pinned sources before copying payloads.
2. Independent workstreams. Coordinator instructions and references have one owner. Package manifests, install/verification code and release integration have a separate owner. Independent review reads both.
3. Shared mutable state. Vendor payloads remain immutable. One coordinator writes the proposal, lockfile and release evidence. Workers do not write shared host configuration.
4. Smallest safe decomposition. One lead and three specialist lenses cover this scope. Avoid a new backend or Temari execution runtime for v1.

## Acceptance evidence

Package acceptance requires intact, pinned licensed payloads; portable paths; passing verifier and meaningful tamper/failure tests; a real upstream search; successful Git URL installation in a fresh isolated Codex home; installed skill readback; and independent proposal/package review.

Behavior acceptance requires a representative exercise that produces a user-goal model, useful flow and state specification, evidence-linked critique, actionable recommendation and validation plan while respecting supplied tokens and capability gaps. Runtime accessibility and Figma write access are separately scoped capabilities and are not implied by this result.

## Poteto principles applied

Model the Domain shaped the shared brief, mode table, three specialist responsibilities and the versioned dependency inventory instead of independent drifting prompts. Prove It Works shaped the fresh Git URL install, installed-payload readback and representative behavior evaluation rather than treating file creation as completion.

This plan has received an independent local review using the Poteto method. The requested Akamaru/Muse evaluation is pending. It is not a canonical Temari run receipt or full-feature completion claim.

## Installation evidence and exact host route

Observed on this host: `codex plugin marketplace add <local-repo-path> --json`, `codex plugin add ui-design-agent@ui-design-agents --json`, and `codex plugin list --marketplace ui-design-agents --json` succeeded in a fresh isolated Codex home. List readback reported the plugin installed and enabled at version 0.1.0. This is a local-path registration check, not Git URL installation, skill-catalog discovery, or native worker execution proof.

Documented and confirmed by CLI help: marketplace registration accepts an HTTPS Git URL and `--ref`. The release check will register the public GitHub URL at the exact published commit, install with `codex plugin add`, read back enabled registration, verify the installed payload and skill catalog, then exercise the actual coordinator. The optional Python installer wraps these commands; it must not replace them with a folder-copy operation.

Official host references: https://developers.openai.com/plugins/build/plugins and https://learn.chatgpt.com/docs/agent-configuration/subagents . Figma/browser access depends on the caller's connected tools and permissions; no new Figma integration is bundled.

## Reproducible behavior evaluation

Retain a sanitized input, exact coordinator and specialist prompts, native-versus-serial execution, complete output and criteria-based review. A synthetic station operations task will deliberately include unavailable battery telemetry, stale communication status and conflicting proposed layouts. The output must identify user goals, a coherent journey/flow and IA, permission and recovery states, useful prioritized recommendations, preserved supplied tokens, meaningful disagreement resolution and honest source limitations. Mark heuristic review and proposed validation separately from executed runtime checks or user research.

## Local independent review disposition

The local reviewer found the UX contract materially complete and preferred the separate host plugin over a dedicated MCP service for v1. Its findings prompted the explicit Akamaru review step, separate native-plugin evidence, reproducible behavioral acceptance, a disagreement decision record and proportional discovery scope. These are proposal/instruction reviews; package verification, Git URL installation and behavioral evaluation remain pending.

## Durable awareness and workflow integration

Randy requires awareness in every new Temari thread and appropriate subject-matter-expert use. Two separate behaviors must be proven.

1. **Host discovery.** Install and enable the UI Design plugin in the user's Codex host scope. The entry has normal implicit invocation enabled and a precise description. New host conversations should receive its skill identity and description without depending on prior-chat memory, per-project copies, or an explicit `$ui-design` mention. Each execution host needs its own installation; disabled or absent plugins remain unavailable.
2. **Temari routing.** Add a shared host-specialist intake reference to the public Temari and direct Poteto conversational entries. Use the host-provided skill/plugin inventory once per new-chat intake, identify relevant installed SMEs, load only applicable specialist instructions, and supply a bounded brief. Do not scan arbitrary global directories, install missing tools silently, or select every SME for every task. Temari accepts or rejects advisory findings against user intent and evidence, then carries accepted bounded context into its existing workflow briefs.

Current observed discovery evidence: two independent fresh Codex app-server processes queried `skills/list` with `forceReload: true` from a neutral directory and the Temari workspace. Both returned exactly the coordinator `ui-design-agent:ui-design`, user scope, enabled true, correct pluginId and no skill errors. The three nested vendor skills remained package resources rather than additional discoverable entries. This is catalog exposure, not proof of automatic routing or delegation.

Current routing gap: Temari's public conversational entry selects existing research/engineering/QA responsibilities but has no installed-external-SME intake step. Its method loader points at the bundled catalog. The CLI does not intercept every chat or enforce natural-language selection. The integration is therefore a small separately verified Temari conversational-entry change, alongside the standalone agent repo.

| Workflow | When UI Design contributes | Temari retains |
| --- | --- | --- |
| UX discovery and design | Goals/tasks, journeys, flows, IA, interaction states, Figma comparisons, choices and validation plans | User intent, product decisions, requirements and scope |
| UI engineering planning | Translate accepted design findings into UI constraints and acceptance criteria before implementation | Architect/build/review requirements, permissions and candidate verification |
| UI implementation review | Design fidelity, clarity, state completeness and interaction critique against the selected candidate | Functional testing, independent engineering review and delivery |
| QA | Read-only usability/accessibility observations and proposed scenarios for relevant UI tickets | Actual executed evidence, product oracle, evaluator disposition and acceptance |
| Unrelated backend or operational work | Skip unless a material UI/user-journey dependency exists | Existing route without forced design overhead |

The protected Codex worker driver deliberately disables ambient host skill discovery. Keep that restriction. SME selection occurs in the conversational host entry, and accepted findings enter existing bounded worker context. Do not add arbitrary execution fields or let the design plugin approve engineering or QA results.

Acceptance must include fresh-context requests without an explicit designer mention, observed skill selection and correct caller handoff, a relevant UI engineering and QA case, an unrelated backend negative control, a missing/disabled-plugin case and a serial fallback when workers are unavailable. Also verify the rebuilt Temari bundle contains the intake reference. Global catalog registration alone cannot satisfy these routing tests.

## Source evidence for Temari integration boundary

Observed current source entry points inspected during this proposal:

- `packages/workflow-runtime/public/skills/temari/SKILL.md`, responsibility selection around lines 31–38.
- `packages/workflow-runtime/public/skills/temari/references/method-library.md`, bundled method loading around lines 20–23.
- `packages/workflow-runtime/public/skills/poteto-mode/SKILL.md`, conversational evidence intake around line 43.
- `libs/host-adapters/src/lib/codex-exec-worker.ts`, bounded brief context around line 437.
- `libs/host-adapters/src/lib/codex-model-driver.ts`, protected skill/agent access restrictions around lines 44–47 and skip_host_skill_discovery around lines 93–96.

These are navigation references for current inspected source, not a claim that the routing change has already shipped. No proprietary source text is copied into this public package.
