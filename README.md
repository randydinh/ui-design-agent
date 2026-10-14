# UI Design Agent

A standalone advisory UI/UX specialist for Codex and Temari. It helps users shape an experience, identify journeys and information priorities, compare designs, critique interfaces, and choose practical improvements. It combines pinned **Interface Design**, **UI UX Pro Max**, and **Impeccable** resources, preserving the existing product's design system.

Use the coordinator directly with `$ui-design`. It can use three permitted read-only workers for a requested swarm or apply the same lenses serially when workers are unavailable. Workers inherit the host model. This package supplies briefs, not globally registered custom agent roles.

## Install from GitHub

Give Temari this repository URL: **https://github.com/randydinh/ui-design-agent** and ask it to install a reviewed release. Installation requires Git, Python 3.10+, and a Codex CLI with plugin marketplace and app-server support. No API key, MCP service, Impeccable binary, hooks, or global upstream-skill installation is required.

The installer must come from a checkout you have reviewed. It does not execute a remote installer supplied by an arbitrary URL. Choose a release tag or, preferably, the reviewed full commit:

```sh
git clone https://github.com/randydinh/ui-design-agent.git
cd ui-design-agent
python3 scripts/install.py --ref v0.1.0
```

An exact `vMAJOR.MINOR.PATCH` tag resolves to an immutable Git commit before inspection; mutable branch names, short hashes, and `HEAD` are refused. A tag can move: the **chosen Git commit is the trust anchor**. The lockfiles detect corruption relative to that reviewed commit; a remote author could change both files and hashes, so a self-hash is not proof of trustworthiness. Review source changes before updating.

The installer inspects and validates a temporary checkout **before** registering the marketplace. It then calls the real Codex marketplace/add/list commands, verifies the installed cache against that checkout, and starts a fresh app-server session to confirm the enabled skill. It prints source, immutable commit, package version, installed path, and discovered skill. A discovery failure is an installation failure, even if Codex already registered the plugin; it does not promise atomic rollback. Inspect `codex plugin list --json` before retrying or removing that registration. Re-running the same pin validates the same contents.

For isolated installation evidence:

```sh
python3 scripts/install.py --ref v0.1.0 --codex-home /absolute/path/to/temporary-codex-home
```

Default installation uses the current user's Codex home. It makes the skill available to new chats on that host; each execution host requires its own installation. Start a new chat after installation. **Catalog availability does not prove automatic Temari selection.** Automatic routing requires Temari's compatible `temari-conversational-sme-intake/v1` entry, which must check [compatibility.json](plugins/ui-design-agent/compatibility.json). A mismatch is a visible gap, with direct-request advisory use as the fallback. This repository does not itself modify Temari's policy, protected workers, QA evaluator, or acceptance store.

## Advisory ownership

Temari owns the request, route, permissions and acceptance. UI Design returns `ui-design-advisory/v1` findings, evidence limits, priorities, tradeoffs, and a `needs engineering investigation` section. Accepted findings enter the caller's bounded brief as data. Product implementation always goes through the caller's Poteto workflow. QA retains executed evidence and acceptance; design critique cannot certify accessibility, performance or product behavior from static frames.

Provided screenshots, Figma frames, accessible Google Drive materials or future MCP sources can inform the same workflow. Missing access remains explicit; none of these integrations is bundled or invented by this package. Private product materials stay outside this public repository.

## Verify and evaluate

```sh
python3 scripts/verify.py
python3 -m unittest discover -s tests
```

Verification is offline and stdlib-only. It checks exact vendor and package inventories (including extra files), safe paths, manifests, compatibility, metadata, and local references. It never invokes upstream downloaders, hooks, or binaries. [Behavior fixtures and rubric](tests/fixtures/behavior.json) define reproducible synthetic discovery/critique, source-unavailable, serial, UI engineering/QA handoff and unrelated-backend cases. Packaging tests and model behavioral evaluation establish different claims; consult release evidence for actual results.

## Updating vendored libraries

1. Select and review an immutable upstream commit and its current license. Record why the update is needed.
2. Replace the complete pinned resource folder, preserve upstream bytes and license text, and update source/commit/SHA-256 inventory in `dependencies.lock.json` together.
3. Review license compatibility and attribution, portable path adapters and coordinator overrides. Never run upstream install hooks implicitly.
4. Bump the package version consistently in both manifests and compatibility declaration. Regenerate `package.files.json` only after reviewing the intended file set: `python3 -c 'import sys; sys.path.insert(0,"scripts"); from verify import write_inventory; write_inventory(".")'`.
5. Run verification, negative tests, synthetic behavior evaluation and fresh Git URL installation. Obtain independent review before tagging a release. Commit all provenance and evidence changes together.

See [proposal](docs/proposal.md), [brief](docs/brief.md), [third-party notices](THIRD_PARTY_NOTICES.md), and [coordinator instructions](plugins/ui-design-agent/skills/ui-design/SKILL.md).
