# Third-party notices

The integration and coordinator are MIT licensed. Each vendored dependency retains its own license, copyright, and attribution. Payload files are unchanged; adapters live outside vendor. Every file is covered by the SHA-256 inventory in `plugins/ui-design-agent/dependencies.lock.json`.

| Dependency | Upstream | Pinned commit | License |
| --- | --- | --- | --- |
| Interface Design | https://github.com/Dammyjay93/interface-design | `2f9be3206855bcb2d1d0af262c8bae25cba6658d` | MIT |
| UI UX Pro Max | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | `7246805992a42b7bba37d4cac83b01416f0c6c44` | MIT |
| Impeccable | https://github.com/pbakaus/impeccable | `2f98774f86bc05563876643db37e6c37c322850f` | Apache-2.0 |

Full license texts are `skills/ui-design/vendor/<dependency>/UPSTREAM-LICENSE` inside the plugin. Original skill metadata, reference content, scripts, data provenance and bundled attribution files are retained. Impeccable's optional launcher can download its separately versioned binary on first explicit use; installation and default reviews do not invoke it. Vendoring its instructions does not bundle that binary.

## Redistribution determination (2026-10-14)

Reviewed component license texts permit this separable public distribution with their original terms preserved. Root MIT applies to our integration; Impeccable remains Apache-2.0, and MIT component attribution remains required. The recorded scope, source pins, license hashes and obligations are in `plugins/ui-design-agent/license-review.json` beside the dependency inventory. This is a package-specific determination, not a relicensing of upstream work.

Impeccable's root `NOTICE.md` is preserved as `UPSTREAM-NOTICE.md` in its vendor folder. That notice credits ehmo's MIT platform-design-skills for derived iOS/Android reference guidance. Full MIT texts for those references and the bundled modern-screenshot library (wxm) accompany the payload as `PLATFORM-DESIGN-SKILLS-LICENSE` and `MODERN-SCREENSHOT-LICENSE`. These added attribution files are separately inventoried; original payload bytes remain unchanged.

Cataloged font families, licensing metadata and icon names are not font files or icon artwork. Downloading or embedding such assets for a product requires checking the selected assets' own terms. No endorsement or trademark right is claimed. The optional Impeccable binary is not redistributed here.
