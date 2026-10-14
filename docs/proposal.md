# UI Design Agent delivery design

The accepted design uses one external host plugin with a UI/UX coordinator and three package-local, pinned skill libraries. Interface Design supplies hierarchy and component guidance, UI UX Pro Max supplies usability reference searches, and Impeccable supplies critique. Native workers inherit the caller's model and permissions; unavailable workers use explicitly labeled serial lenses.

The agent helps shape goals, journeys, workflows, information architecture, interaction states and validation plans; compares current evidence with proposed designs; and recommends concrete changes. It returns advisory findings. Temari owns user intent, permissions, routing and acceptance. Authorized product implementation returns to Poteto's engineering workflow. QA observations do not become executed QA evidence.

## Review resolutions

Akamaru accepted proposal 001 and revision 002 with findings. The review evidence is retained in the operator's private task record, separate from this public package.

| Finding | Resolution |
| --- | --- |
| Public redistribution license determination | `plugins/ui-design-agent/license-review.json`, retained component licenses, upstream NOTICE and supplemental MIT notices |
| Worked disagreement resolution | Coordinator example resolves operator density versus cognitive load against task/evidence |
| Trust anchor | Chosen published Git commit; payload inventories verify content within that commit |
| Behavior rubric and failure cases | `tests/fixtures/behavior.json` defines independent scoring, thresholds, hard failures and seven cases |
| Vendor update procedure | README requires reviewed source pins, notices, inventories, tests and a new package version |
| Engineering investigation survives synthesis | Named report-contract handoff slot |
| Cross-repository version compatibility | Plugin-root `compatibility.json` declares `temari-conversational-sme-intake/v1` and `ui-design-advisory/v1`; caller verifies identity/content |
| Uncertain relevance and dismissal | One bounded clarification/mention; dismissal suppresses repeat suggestions; explicit mismatch fallback |

## Integration

Global host installation exposes the coordinator in new chats on that host. Compatible Temari conversational intake selects the SME for material design tasks and carries accepted/rejected/deferred findings into existing bounded briefs. Protected engineering workers retain ambient-skill-discovery restrictions. Compatibility declaration is a data contract, not host capability proof. No new Temari execution route, evaluator, agent registry or MCP service is introduced.

## Verification boundaries

Offline verification and focused failure tests cover package structure, content inventory, path safety, metadata, license provenance and installer handling. Release verification additionally needs real Git URL installation, enabled-plugin readback, fresh skill discovery and an actual independent behavioral review. See release evidence for what ran. Static frames do not prove keyboard behavior, accessibility conformance, performance, user research or backend telemetry.
