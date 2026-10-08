---
name: model-prep
description: Prepare supplied 3D models in Blender for FDM printing, including limited-colour artwork, editable SVG contour review, approved colour transfer, geometry edits, dimensions, part fit, splitting and export. Use for textured models, meshes with reference images, or geometry-only assets. Supports any specified usable print volume and optional Bambu Studio handoff. Not a model-search or printer-control skill.
---

# Model Prep

Turn provided models and appearance references into deliberate, reviewable artwork and reversible print-preparation revisions. Use Blender, preferably through available Blender MCP tools. This is an agent workflow with a small SVG helper, not a universal automatic mesh converter. Discover the installed tools; do not invent capabilities or claim unperformed checks.

## Start with the requested stage

Interpret `process`, `resize`, `split`, `review contours`, and natural-language equivalents. Default artwork mode is **simplified**; use **faithful** or **local restoration** when requested. Extract the palette, protected geometry/UVs, preview-only limits, dimensions, output and optional printer envelope. Ask only for information blocking the next dependent operation; continue independent work.

Read [intake and revision state](references/intake-state.md) for every model job. Read other references only when their stage applies:

| Stage | Work product and boundary | Procedure |
|---|---|---|
| S0 Intake | Source snapshot, scope, units, known unknowns | [Intake/state](references/intake-state.md) |
| S1 Appearance capture | Recoverable images, UV/material correspondence or registered reference views, before destructive edits | [Artwork/review](references/artwork-review.md) |
| S2 Geometry work | Requested resize, correction, repair or fit assessment in a new scene | [Geometry/fit](references/geometry-fit.md) |
| S3 Interpretation | Proposed categorical regions; mark inferred connections | [Artwork/review](references/artwork-review.md) |
| S4 SVG review | Editable raster-plus-vector SVG, overlay and flat preview from the same saved paths | [Artwork/review](references/artwork-review.md) |
| S5 Colour application | Accepted paths mapped to a separately saved model | [Colour transfer](references/colour-transfer.md) |
| S6 Physical preparation | Orientation/envelope assessment; optional relief, cuts and joints; unsplit master retained | [Geometry/fit](references/geometry-fit.md) |
| S7 Export | Compatible artifact with measured QA; optional actual slicer inspection | [Export/QA](references/export-qa.md) |
| S8 Delivery | Requested products, current scene, status and remaining checks | [Intake/state](references/intake-state.md#delivery) |

Stages are conditional, not a command to execute everything. Capture appearance before edits that invalidate it. Review artwork before production colour/topology changes, unless the user explicitly combines those stages. Relief, segmentation and printing are separate from colour approval.

## Authority and boundaries

- Never edit original inputs in place. Save meaningful edits, experiments and retries to new timestamped revisions. Keep dependencies, approved artwork and the unsplit master.
- Preserve user-corrected SVG paths and connection decisions. On continuation, read the actual saved SVG and its approval record, not an earlier mask or conversation summary. Never regenerate over corrections.
- Exact accepted paths drive previews, masks and surface transfer. A separately redrawn approximation is not equivalent. Bind acceptance to a file hash and region scope; edits after approval need review only for affected regions and dependencies.
- Preview-only may create review artifacts, but cannot modify the production scene, apply old approvals, or publish an export as finished. Name the unchanged current scene in the report.
- Use exactly the requested printable palette. Source shading, anti-aliasing and annotation colours are not print classes. Do not assume filament loading, AMS, nozzle count or printer model from palette size.
- Protect cavities, sliding/mating faces, UVs and dimensions. No topology change merely for easier tracing. If exact borders need refinement but geometry is protected, show the conflict and stop only that transfer/export stage.
- Millimetres describe geometry; pixels and UV coordinates describe artwork. Preserve their mapping. Never treat a photo as a registered texture.
- Tool absence blocks only dependent work. Consult [tool setup](references/tools-setup.md) when Blender, SVG rendering or a requested slicer capability is unavailable.
- Do not search for replacement models, upload user assets to external services, start or monitor prints, or modify unrelated configuration as a side effect of model preparation.

## Approval and evidence

Make decisions reviewable before requesting approval: deliver the real SVG and paired views, identify uncertain regions, and state the concrete next action. Existing explicit authorization carries forward; do not ask again for ordinary implementation choices. A generic `process` request does not approve a newly invented major artwork change.

| Label | Evidence required |
|---|---|
| PREVIEW ONLY | Review artifact; production colours/geometry unchanged |
| REVIEW REQUIRED | Named unresolved region, mapping or consequential decision |
| ARTWORK APPROVED | User acceptance of identified SVG hash/regions; no export implied |
| COLOUR APPLIED | Saved model using those regions; transfer checks passed |
| EXPORT READY | Actual file plus artifact checks, not slicer proof |
| SLICER VERIFIED | This artifact inspected/sliced with named version/profile; describe which |
| BLOCKED | Named missing input or failed check and affected stage only |

Geometry-only jobs can go straight to export without artwork approval. Historical exporter compatibility can be **capability verified**; it never establishes that today's model sliced or physically fits.

## Example

User: `process character.glb, use black, white and red; keep UVs; preview first`.

Inventory the model and dependencies, preserve UV correspondence, and interpret shapes into the requested palette. Deliver a layered editable SVG, source overlay and flat preview with ambiguous joins marked. Report **PREVIEW ONLY**, identify the current unchanged scene, and seek acceptance of specific proposed regions. After acceptance, apply the same saved paths using the transfer procedure and create a new scene. Do not add relief or splits without scope for them.

## Deterministic helper

See [SVG helper usage](references/artwork-review.md#svg-helper). `scripts/review_svg.py` creates a PNG-backed review scaffold or derives two SVG presentations from an edited review. It neither traces artwork nor approves it, maps a mesh, renders PNGs or proves printability. Complete the actual artwork; never deliver an empty scaffold as finished work.
