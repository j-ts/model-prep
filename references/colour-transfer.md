# S5: transfer accepted artwork to the surface

**Inputs:** accepted SVG hash/regions, palette, mapping and last-good scene. **Output:** separately saved colour revision and QA. **Allowed changes:** colour representation and only permitted, necessary local boundary refinement. **Pass:** regions appear on correct surfaces, palette and protected dimensions retained. **Failure/rollback:** discard the candidate scene, reload checkpoint, retain SVG and explain failed mapping. Artwork acceptance does not authorize damage to protected geometry.

## Choose the representation before mutation

1. Read actual accepted paths, resolve corrected replacements and reject incomplete masks/contradictory overlap for affected regions. Exclude baseline raster, guide strokes and annotations from print classes.
2. Use recorded atlas/material/UV or registered projections. Keep sources separate. SVG normally has Y down; check UV/image orientation with asymmetric landmarks instead of guessing. Confirm front/back, mirrors, repetitions and wrap.
3. Rasterize the same paths into categorical labels, or intersect boundaries with mapped triangles. Separate anti-aliased display colours from print labels. Choose raster resolution from projected feature sizes, inspect coverage/holes and never reclassify the shaded original after acceptance.
4. Test the representation on a copy with difficult boundaries: coarse triangle, UV seam, curved face and mirror/repeat when present. Then apply across the intended surface.

## Sparse topology and sharp colour boundaries

Texture detail can cross a triangle, but one-colour-per-face/vertex targets cannot necessarily reproduce it. A texture+MTL package is not the requested single vertex-colour OBJ. Discover actual exporter/importer support and preserve an established route.

For precise categorical mesh colours, resolve boundaries locally on a copied mesh. Interpolate new positions/UVs from the original surface; keep shape, dimensions and protected surfaces within agreed tolerance. Shared boundary vertices may need separate exported vertex records/corners at identical positions to prevent colour blending. These colour seams can look topologically disconnected to mesh checks: distinguish them from physical cracks and inspect actual slicer treatment; a continuous render does not prove manifoldness.

If topology changes are forbidden and the encoding cannot retain thin borders, preserve geometry and deliver a projection/diagnostic. Present concrete options: authorize local refinement, use an actually supported alternative encoding, or accept an illustrated detail loss. Block only dependent transfer/export. Never silently round regions to triangles, thicken borders, erase islands, change accepted SVGs or invent textured-OBJ support.

Inspect installed Blender colour-attribute domains and exporter behaviour: corner colours, point colours and face materials are different. Account for colour-space conversion; palette RGB is usually sRGB, not necessarily the values expected in scene-linear attributes. Compare exported values/classes under the declared encoding tolerance rather than trusting the viewport.

## Optional companion exporter

The [bambu-studio-ai multicolour reference](https://github.com/heyixuan2/bambu-studio-ai/blob/main/references/multicolor.md) describes `colorize` and OBJ/painted-project output. Read the installed version and `--help`. Its dominant-colour-per-triangle method is a useful baseline/export route when it preserves the artwork; it is not an exact boundary resolver for approved thin contours on coarse meshes.

## Transfer checks

- Compare overlay, flat view and surface projection against the same accepted revision/hash. Inspect small features, holes and shared seams.
- Check all relevant components/material domains, including backs/interiors/mirrors. Keep unseen or unmapped surfaces labelled; no invented fidelity.
- Count categorical values/classes, detect interpolation shades and uncoloured faces. Render anti-aliasing is not print colour.
- Compare dimensions, protected positions/surfaces and UV correspondence with the checkpoint. Permitted refinement requires geometric/interpolated-mapping validation, not equal vertex counts.
- Save a new scene with accepted artwork provenance. Report **COLOUR APPLIED** only for verified applied regions; export/slicing are separate.

Prefer repair before painting. Later topology changes may invalidate paint; re-transfer from accepted paths and repeat artifact checks.
