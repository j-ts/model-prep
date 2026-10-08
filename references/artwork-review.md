# Appearance capture, reconstruction and SVG review

## S1: capture correspondence

**Input:** preserved appearance or reference images. **Output:** recoverable evidence and surface mapping. **Allowed changes:** capture/registration artifacts, copied scene for necessary baking. **Pass:** original appearance reproducible on relevant surfaces. **Failure/rollback:** retain source, label unmapped surfaces, avoid edits that destroy remaining correspondence.

Retain original full-resolution images, UV values, material slots, transforms and atlas assignments. Preserve packed dependencies, procedural/material appearance and vertex colours as appropriate; bake onto a copy only when needed. Record wrap, mirrored/overlapping islands and surfaces sharing artwork. List all surfaces one path influences before approval. Keep multiple atlases traceable.

For mesh plus photos, register views using landmarks and a camera/projection model. Distinguish pigment/linework from highlights, shadows, scratches and perspective. Record uncertainty/occlusions; never extrapolate unseen interiors as observed. Create new UVs only on a revision and within the user's constraints.

Full-source coordinates are canonical. A crop uses `(x_source, y_source) = (x_crop + x0, y_crop + y0)`; resized/rotated crops need the full reproducible transform. Landmark-check generated cleanup for local and distant warping. If it cannot be registered, use it as a proposal and redraw in original coordinates, never replace the baseline.

## S3: interpretation

**Input:** captured appearance, palette and scope. **Output:** named proposed regions and disputed decisions. **Allowed changes:** draft masks/paths, no production mesh. **Pass:** connections/separations and deviations reviewable. **Failure/rollback:** return to evidence and accepted paths, retain informative rejected candidates.

- **Simplified (default):** identify forms, remove noise, restore continuity, merge negligible islands and redraw clean shapes while retaining identity. Mark important deviations, omissions and inferred connections.
- **Faithful:** retain distinctive asymmetry, corners and short edges. Repair technical noise conservatively; convenience does not justify redesign.
- **Local restoration:** bound the changed region and freeze everything else, especially corrections. One scratch does not authorize erasing adjacent borders or closing unrelated gaps.

Preserve corners, endpoints, junctions and islands as anchors; smooth selected spans. A guide stroke can indicate intent, not a literal cut/deletion mask. Define shared seams once in full-source coordinates and reuse them in adjacent regions/crops. Open working contours are legitimate, but SVG fills implicitly close open paths: do not call them complete masks. Check holes, overlap and coverage. Pixel width is not physical printable width.

## S4: editable review and acceptance

**Input:** proposed/user-edited paths and aligned evidence. **Output:** SVG plus overlay/flat views and per-region state. **Allowed changes:** review artifacts until acceptance. **Pass:** both views derive from saved paths, original recoverable, named editable paths and uncertainties preserved. **Failure/rollback:** repair a new candidate; keep previous SVG and production scene unchanged.

Use original dimensions as `viewBox="0 0 W H"`; embed the full-resolution raster with a data URI. Use Inkscape layers or equivalent groups:

| Group ID | Contents |
|---|---|
| `original-reference` | Aligned, locked, hideable immutable raster |
| `working-outlines` | Named editable curves and unfinished boundaries |
| `flat-colour-regions` | Closed geometry, requested fills, islands and holes |
| `user-corrected-regions` | User edits/accepted replacements, authoritative over AI proposals |
| `review-annotations` | Uncertainty, occlusions, junction notes; never print data |

Use stable unique region IDs and labels; approval belongs in the manifest. When a correction replaces a flat region, disable/remove the superseded region only in the new candidate and reference its replacement. Do not stack conflicting printable shapes. A guide or unfinished correction stays draft, not a closed print region. Define fill rules for holes and inspect them in the actual renderer.

Generate two views from the saved SVG:

1. **Overlay:** raster with exact borders/annotations, avoiding opaque fills obscuring comparison.
2. **Flat:** exact flat/corrected regions without source shading or annotation colours. Describe incomplete coverage outside print layers.

Inspect both with a local SVG renderer/vector editor; render PNGs for chat when useful. Crops present the same full-source paths. A 3D projection helps seams/curvature but does not replace editable SVG. Photos may need multiple linked registered SVGs, not a fictitious complete atlas.

Deliver the concrete review before seeking acceptance; identify regions and next operation. Consume edited SVGs directly on continuation, hash them and compare changed regions/shared seams. Preserve corrections. Unchanged accepted regions need no repeated approval; altered ones lose affected acceptance. Partial approval enables independent regions only; unresolved regions remain explicit in model/export status.

## SVG helper

Run from the installed skill directory, or use absolute script paths. Python 3.10+, no pip dependencies:

```bash
python scripts/review_svg.py init --image /path/to/original.png --output /path/to/job/review_v001.svg --palette '#000000' '#ffffff' '#ff0000'
python scripts/review_svg.py views /path/to/job/review_v002.svg --overlay /path/to/job/overlay_v002.svg --flat /path/to/job/flat_v002.svg
```

Use `python3` if required; quote hex colours. `init` creates an **empty scaffold**. Add the actual artwork before delivery. For other raster types embed the original manually, or use a lossless working PNG while retaining original/hash/registration.

`views` preserves path and transform values and leaves the source unchanged. In the overlay, flat/corrected shapes use cyan strokes with no fill, so their exact boundaries remain visible over the raster. The fixed stroke width is one SVG user unit (source pixel before preserved transforms); scaling can change its displayed width. The flat view retains original shape styles. Both files remain **PREVIEW ONLY**.

Helper limits: UTF-8 SVG; five uniquely named direct-child groups; drawing content inside those groups; embedded PNG references. It rejects DTD/entities, script/events, animation, foreignObject, stylesheet elements, external resources and image/use/text in print groups. Complex editor-generated SVGs can be handled in a vector editor instead of weakening/replacing accepted artwork just to satisfy the helper. This is not a complete SVG sanitizer or validator. PNG checking covers header dimensions, not decoding. Mask closure, overlap, palette, rendering and approval still require artifact checks. Existing outputs are refused.
