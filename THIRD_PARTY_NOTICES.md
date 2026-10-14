# Third-party notices

The integration and coordinator are MIT licensed. Each vendored dependency retains its own license, copyright, and attribution. Payload files are unchanged; adapters live outside vendor. Every file is covered by the SHA-256 inventory in `plugins/ui-design-agent/dependencies.lock.json`.

| Dependency | Upstream | Pinned commit | License |
| --- | --- | --- | --- |
| Interface Design | https://github.com/Dammyjay93/interface-design | `2f9be3206855bcb2d1d0af262c8bae25cba6658d` | MIT |
| UI UX Pro Max | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | `7246805992a42b7bba37d4cac83b01416f0c6c44` | MIT |
| Impeccable | https://github.com/pbakaus/impeccable | `2f98774f86bc05563876643db37e6c37c322850f` | Apache-2.0 |

Full license texts are `skills/ui-design/vendor/<dependency>/UPSTREAM-LICENSE` inside the plugin. Original skill metadata, reference content, scripts, data provenance and bundled attribution files are retained. Impeccable's optional launcher can download its separately versioned binary on first explicit use; installation and default reviews do not invoke it. Vendoring its instructions does not bundle that binary.
