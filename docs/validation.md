# Validation record

Recorded 8 October 2026. This distinguishes package checks from actual model/print validation.

## Automated helper checks

Run from the repository root with Python 3.10+:

```text
python -m unittest discover -s tests -v
```

Eleven CLI-level tests passed locally on Windows / Python 3.11. Tests create synthetic PNG/SVG inputs in isolated temporary directories and verify:

- Exact embedded reference bytes, image dimensions, palette and source hash.
- Empty scaffold status, editable layer structure and locked reference.
- Source file unchanged; saved path geometry and transforms retained in both views.
- Exact accepted flat/corrected boundaries shown as stroke-only overlay; flat artwork styles retained.
- Visibility and preview-only provenance.
- Refusal to overwrite source/existing outputs or use identical destinations.
- Cleanup of a newly reserved preview if the second output cannot be created.
- Rejection of missing layers, non-PNG/invalid-palette inputs, active/external SVG content, animation and raster content in print layers.

The helper was developed against failing CLI tests. Review added regression cases for initially hidden flat boundaries and allowed SVG animation. Both fixes passed the complete suite. `ruff check scripts tests` and `ruff format --check scripts tests` passed after formatting. The skill-creator `quick_validate.py` also passed; it validates package metadata/scaffolding, not model behaviour.

GitHub Actions runs the same dependency-free unittest suite on Linux and Windows with Python 3.10. Consult the repository's actual Actions result for a particular commit; defining a workflow alone is not proof of a successful run.

## Independent agent scenarios

An initial agent without this skill proposed reasonable source-preserving plans but interpreted an ambiguous “one colour OBJ” request as textured OBJ plus sidecars. That exposed a handoff ambiguity worth making explicit; it is not a controlled performance benchmark. A fresh agent subsequently read the skill and relevant references and produced plans for the following explicit scenarios before comparing with the original design specification:

| Scenario | Required behaviour observed in the independent plan |
|---|---|
| Local scratch cleanup; preview only; existing corrected junction and open contours | Preserved corrections, bounded restoration, left unrelated gaps draft, paired SVG views, unchanged production scene |
| Approved thin borders; coarse mesh; one vertex-colour OBJ; geometry protected | Preserved the established route, diagnosed representation conflict, blocked only dependent transfer/export instead of changing topology or delivering sidecars |
| Two-part sliding assembly resized to 180 mm; 220 x 220 x 250 mm volume; no nozzle/material | Clarified measured reference, preserved UVs, measured scaled gaps/motion and bare envelope, left process/physical fit unverified |
| STL plus front/back photos; faithful artwork; unseen hollow interior | Registered references, preserved cavity, identified unknown interior, separated artwork acceptance from transfer/export |

The reviewer found no material specification gap in those decisions. These are **plan-based behavioural checks**, not executed Blender jobs.

## Repeatable evaluation

Give a fresh agent the skill and one scenario above, without the expected-behaviour column. With a real disposable fixture, ask it to deliver the requested artifact in an isolated output directory. Check the actual source hashes, SVG paths, manifest, Blender measurements and status claims, not just its narrative. Any mesh/slicer test needs the relevant tools and an explicitly supplied test asset.

Reject a result that silently closes unrelated contours, approximates approved thin borders, blocks all work for missing nozzle settings, invents unseen artwork, equates preview with applied changes, or equates exported/sliced with physically fitted.

## Not verified for this release

- Live discovery in all three agent products or Blender MCP connectivity.
- Rendering of the synthetic paired SVGs: files were generated, but browser inspection was blocked because local file URLs are disallowed. XML/geometry/style assertions ran successfully; no visual pass is claimed.
- Actual UV-to-surface mapping, vertex-colour OBJ import, slicing, printer execution or physical fit.
- Broad SVG conformance/security auditing; the helper intentionally accepts a constrained subset and is not a general sanitizer.

Installation paths and setup commands were checked against linked primary documentation. Artistic fidelity and print-specific accuracy still require per-job review and measurements.
