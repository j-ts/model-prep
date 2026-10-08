# S2 and S6: geometry, fit and physical preparation

## Geometry contract

**Input:** saved source/capture, dimensions and protected features. **Output:** versioned scene and measurements. **Allowed changes:** requested corrections only. **Pass:** dimensions and relevant geometric conditions measured, mapping/protected features retained. **Failure/rollback:** reload checkpoint, retain diagnostics, never repair the immutable source.

Inventory evaluated meshes, world transforms, disconnected objects, cavities and mating surfaces. Inspect non-manifold/boundary edges, normals, intersections and wall thickness as relevant, distinguishing deliberate openings/separate parts from defects. A hollow part's cavity is not a hole to fill. Prefer local repair over unnecessary remeshing.

Blender unit settings alone do not rescale existing geometry. Establish coordinate-to-mm conversion from metadata/known dimensions, then measure evaluated world geometry. For target dimension `D`, scale is `D/current_dimension`; identify the measured axis/reference. Uniformly scale an assembly about a consistent origin, preserving relative positions. UV coordinates can remain unchanged while physical artwork widths and clearances scale.

Measure the result rather than trusting UI settings. Record original/final dimensions, applied object transforms and UV/colour correspondence. Check normals/export after negative or mirrored transforms. Preserve protected sliding faces.

## Functional fit

Identify parts, mating faces, motion/insertion direction, travel and stops. Check collision along the assembly path, not just final pose. Measure local gaps and surrounding stock; outer bounds do not prove fit.

Define clearance as per-side, radial, diametral or total. For a circular pair, hole diameter minus peg diameter is diametral clearance; half is radial. No universal tolerance. Account for supplied printing, paint, material and calibration allowances. Resizing scales existing gaps: report that and do not silently replace them. A geometric check cannot prove sliding performance; a scoped fit coupon can be prepared, but the user controls printing.

## Orientation, envelope and segmentation contract

**Input:** unsplit master, usable envelope/profile and cut/joint scope. **Output:** assessed orientation or separate split revision and assembly notes. **Allowed changes:** preparation copies and authorized/necessary splits/joints. **Pass:** parts and assembly path checked, registration preserved. **Failure/rollback:** return to unsplit master, retain labelled failed candidate.

Use the active profile's usable process region, including exclusions and each tool's reach. Otherwise supplied X/Y/Z in mm is enough for geometric screening; do not infer printer/nozzle/material/AMS features. Missing volume blocks final printer-fit claims, not unrelated work.

Test plausible orientations and existing separate parts before cuts. Check transformed bounds and known excluded regions. State brim/raft/support/reach margins separately; bare-part fit does not establish supported-slice fit. Do not split merely because nominal bed size is mentioned.

Split when requested or needed after orientation checks and within preparation scope. Show consequential seams affecting appearance/function. Preserve unsplit master and registration across cuts; avoid important ornament/mating features when possible. Label parts and orientations.

Add keys/connectors if requested or necessary for a workable assembly. Check wall stock, insertion, orientation, collision, assembly order and access. Make dimensions/clearances explicit and editable. Inspect boolean/cut results without filling designed cavities or destroying sliding gaps.

## Requested relief only

Use the same accepted paths, preserve unraised model and expose one editable `relief_height_mm` parameter. Keep reversible modifiers/procedural construction until export. No universal default height. Recheck seating faces, interiors, thickness, intersections and fit. Artwork approval alone does not authorize relief.

Report measurements and limitations. Nozzle/material-dependent fine features, supports and print-quality checks remain unverified without settings. Visual geometry is not a physical trial or structural certification.
