# UI Design Agent maintenance

This is a standalone Codex plugin marketplace, not an Nx workspace. Keep Temari dependencies external. Preserve upstream payloads verbatim and update pinned commits, license texts, and file inventories together. Do not copy private product source or customer data into public examples.

Run `python3 scripts/verify.py` and `python3 -m unittest discover -s tests` after package changes. For release, test Git URL installation into a temporary Codex home using `scripts/install.py --codex-home <temporary-directory>`. Native worker prompts inherit the host model and permissions; package-local briefs are not auto-registered custom roles.
