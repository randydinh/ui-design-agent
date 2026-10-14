# Verification evidence

Release verification is recorded against exact commits and installed payloads. The executable checks are `python3 scripts/verify.py` and `python3 -m unittest discover -s tests`. The synthetic behavior suite and independent rubric are `tests/fixtures/behavior.json`.

The initial package candidate passed its offline verifier, 22 focused tests, and an independent code review. A real isolated local marketplace install and a fresh app-server catalog read also passed. These establish local package behavior only. The release record will add Git URL installation, exact installed cache verification, actual model behavior results and compatible Temari intake evidence before final completion claims.
