# Verification evidence

The 0.1.0 payload was reviewed on 2026-10-14 against commit `9664f0a5093d943e97a2d09e3a3c557df578af22`. Follow-up `d1cdcccebc1a972ebe523507a39203e50765eafd` hardens installer response-shape validation without changing the specialist payload. Release tags resolve to their exact Git commit; consult GitHub checks for the final release commit.

## Executed package and installation checks

- Offline verifier: PASS, 155 package files including 143 upstream/notice files. Extra-file, path, inventory, metadata and reference checks are enforced.
- Installer/package tests: 25/25 PASS, including malformed CLI/RPC output and controlled post-registration failure diagnostics.
- Independent source review: no outstanding actionable findings after the installer repair.
- Actual public GitHub URL installation: PASS in an isolated Codex home, repeat installation PASS, installed cache byte inventory matched the selected commit.
- Actual user-host installation: PASS; fresh app-server `skills/list` exposed enabled `ui-design-agent:ui-design` at the verified installed path.
- No model turn, third-party downloader, hook or upstream binary runs during installation/discovery.

The release-check wrapper composes the installer; its focused mocked tests establish wrapper behavior only. Real URL installation and model behavior are separate evidence. Run `python3 scripts/release_check.py --source https://github.com/randydinh/ui-design-agent --ref FULL_COMMIT` for a new isolated installation/discovery check.

## Model behavior

Seven synthetic native-host responses were independently judged. Experience discovery, unavailable-source comparison, serial card/table comparison, and UI engineering/QA advice scored 12, 11, 12 and 11 of 12. Each met the 10/12 threshold, with full evidence-honesty and ownership scores. Backend-only, incompatible-contract and user-dismissal routing cases passed their applicable boundaries. No fabricated inspection, runtime accessibility claim, product implementation or acceptance, or fake swarm was found.

This establishes bounded output quality given the candidate Temari instructions and supplied enabled catalog observation. Initial contexts were fresh; later cases reused collaborators with scenario resets, so the complete fresh-context protocol is not established by this batch. Native model identity was not exposed. A separate CLI-model attempt failed due to host/provider model support and supplies no passing behavior evidence. No actual product/Figma inspection, runtime accessibility conformance, customer research or executed product QA is claimed.

The checked-in fixtures remain the reproducible acceptance protocol. Native-worker swarm execution and automatic selection in independent new chats on every host require their own evidence. Skill catalog discovery establishes availability, not automatic interception of every chat. Compatible Temari caller instructions perform the advisory intake; they do not change protected workers or add an execution route.

Private review correspondence, host paths, task state and raw local model evidence remain outside this public repository. Akamaru proposal findings were resolved through pinned license/notice provenance, an explicit compatibility declaration, advisory ownership and evidence/claim limits; the final code also received independent review.
