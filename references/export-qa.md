# S7: export and optional slicer handoff

**Inputs:** saved validated scene, accepted artwork provenance, target workflow/deliverable. **Output:** new export and QA, optional slicer evidence. **Allowed changes:** new artifacts and requested slicer project; no print control. **Pass:** actual file has expected dimensions/parts/colours and stated encoding. **Failure/rollback:** retain scene/SVG, label failed export, correct the cause and export a new revision.

## Choose deliverable

- **Established Bambu path:** prefer one OBJ with vertex RGB when requested/appropriate. Multiple objects/parts can share a file without fusion. Keep object identity, separation, Blender master and SVG. Do not substitute texture-dependent OBJ+MTL or fuse parts for “one file”.
- **Bambu project/3MF:** when requested or useful and agreed. Discover current capabilities; generic 3MF and painted Bambu project 3MF differ.
- **Other targets:** use requested compatible geometry format and confirm colour support. STL is geometry-only and unitless: document mm interpretation. OBJ colour extensions and 3MF encodings depend on importer. A geometry export can be useful with multicolour support explicitly unverified.

Inspect installed Blender export options: built-in exporters may not preserve the required attribute domain. Use a confirmed exporter; never invent an operator or treat texture materials as proof of vertex RGB output.

## Artifact checks

1. Verify file exists, has payload and parses/imports into an isolated scene. Do not overwrite the master during round-trip checks.
2. Confirm parts/separation, dimensions/units/orientation, valid indices/faces, finite coordinates, normals and relevant mesh integrity. Coincident vertices for colour discontinuities need a physical-seam/slicer check.
3. For vertex-colour OBJ, inspect `v x y z r g b` under the declared extension/range; other OBJ variants can include other values. Verify expected coloured vertices/faces, categorical palette and absence of unintended shades. Compare fronts/backs, seams, thin borders and separate components to accepted artwork.
4. Check dependencies. A self-contained colour OBJ must not require MTL/images for its colours. Include dependencies when a texture-based route was explicitly selected.
5. Record QA with hash/source revision. Only mark **EXPORT READY** after required checks; unresolved regions or failed required checks prevent an unqualified ready claim.

## Capability versus this artifact

Record a known working OBJ import method as **capability verified**, with versions if known. Do not repeatedly prove it exists. Still check today's dimensions, colours and relevant faces.

Inspect/slice this artifact when requested or when resolving a concrete new risk, such as boundary vertex duplication, thin islands or unfamiliar encoding. Record slicer/version, profile, scale, colour matching, parts and observations. Under **SLICER VERIFIED**, distinguish import-preview inspection from completed slicing/toolpath inspection. Preserve warnings and never mark a failed slice verified.

Match palette to filament/process only when known. No AMS slot/loading assumption. Explain an actual process limitation before altering the design.

## Optional Bambu delegation

Read installed `bambu-studio-ai`, especially `references/multicolor.md` and `references/model-specs.md`; discover command options and delegate only relevant work. [Upstream](https://github.com/heyixuan2/bambu-studio-ai) is optional, not a dependency for other printers.

Repair/orientation of painted projects can invalidate paint; prefer geometry work before final painting and reapply accepted paths if topology changes. Per-triangle auto-colourisation cannot replace intricate accepted contours on sparse geometry. Do not invoke model search/generation, printer discovery, monitoring or printing just because the companion can.

Opening/preparing a file never means printing started. This skill leaves printer control to the user. Exports, renders and slices cannot prove physical fit or structural safety.
