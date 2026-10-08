# Model Prep

An agent skill for editing supplied Blender models and preparing them for FDM printing. Its main workflow turns complex textures or reference artwork into deliberate limited-colour regions, exposes them as editable SVGs, and applies the accepted design back to the model.

Works with **Codex, Claude Code and Google Antigravity (AGY)**. Supports any FDM printer with a supplied usable build volume; Bambu Studio integration is optional.

## What it covers

- Source preservation, UV/reference registration and versioned Blender scenes.
- Simplified, faithful or local contour restoration; embedded-raster SVGs with editable regions, overlay and flat previews.
- User corrections and per-region approval before colour transfer.
- Requested resizing, repair, functional fit, optional relief, splitting and keyed joints.
- Artifact-specific export checks, including the established single vertex-colour OBJ route for Bambu Studio.

This package is a **complete staged agent playbook**, plus a small tested SVG helper. Blender does the modelling; the agent chooses and validates the mapping for the actual asset. It does not contain a universal SVG-to-mesh converter, slicer or printer driver. Installing the skill alone does not install or connect Blender.

## Install

Requires Git and a local agent client. Python **3.10+** is needed only for the SVG helper; it uses the standard library. Blender and a working control route are needed for model operations. A vector editor such as Inkscape is useful for SVG corrections.

Clone the **whole repository**, with `SKILL.md` directly inside the `model-prep` folder. Choose one scope per client to avoid duplicate discovery. If a destination already exists, inspect it and use the update instructions below instead of replacing it.

### Codex

Global install, Bash/macOS/Linux:

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/j-ts/model-prep.git "$HOME/.agents/skills/model-prep"
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills" | Out-Null
git clone https://github.com/j-ts/model-prep.git "$env:USERPROFILE\.agents\skills\model-prep"
```

Invoke **`$model-prep`**. Codex discovers skill changes automatically; restart if missing. Current official guidance uses `.agents/skills` for local authoring. [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills)

### Claude Code

Bash/macOS/Linux:

```bash
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/j-ts/model-prep.git "$HOME/.claude/skills/model-prep"
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills" | Out-Null
git clone https://github.com/j-ts/model-prep.git "$env:USERPROFILE\.claude\skills\model-prep"
```

Invoke **`/model-prep`**. Use `/skills` to check discovery; if the parent skills folder was created during this session, use `/reload-skills`. These filesystem instructions target local Claude Code, not a cloud chat. [Claude Code skills documentation](https://code.claude.com/docs/en/skills)

### Google Antigravity 2.0 / IDE

Bash/macOS/Linux:

```bash
mkdir -p "$HOME/.gemini/config/skills"
git clone https://github.com/j-ts/model-prep.git "$HOME/.gemini/config/skills/model-prep"
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gemini\config\skills" | Out-Null
git clone https://github.com/j-ts/model-prep.git "$env:USERPROFILE\.gemini\config\skills\model-prep"
```

### Antigravity CLI (`agy`)

The CLI has a different global directory. Bash/macOS/Linux:

```bash
mkdir -p "$HOME/.gemini/antigravity-cli/skills"
git clone https://github.com/j-ts/model-prep.git "$HOME/.gemini/antigravity-cli/skills/model-prep"
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gemini\antigravity-cli\skills" | Out-Null
git clone https://github.com/j-ts/model-prep.git "$env:USERPROFILE\.gemini\antigravity-cli\skills\model-prep"
```

Start a new conversation and invoke **`/model-prep`**, or mention it by name. IDE Customizations and CLI `/skills` expose installed skills. The current workspace directory is plural `.agents/skills`; singular `.agent/skills` is legacy compatibility. [Antigravity skills documentation](https://www.antigravity.google/docs/skills)

### Install for one project instead

Run at the project root; choose the command for the client:

```text
# Codex or Antigravity
git clone https://github.com/j-ts/model-prep.git .agents/skills/model-prep

# Claude Code
git clone https://github.com/j-ts/model-prep.git .claude/skills/model-prep
```

These use the same project paths on Windows, macOS and Linux. A shared `.agents/skills/model-prep` install covers Codex and Antigravity within that project. The global installs above are simpler when you want the skill for many model folders.

## Connect Blender and verify

Follow [tool setup](references/tools-setup.md) for Blender MCP, a direct Blender fallback, vector rendering and optional Bambu tools. Setup is separate from skill discovery.

Then ask your agent:

```text
Use model-prep. Report available Blender and SVG tools, then inspect my
provided model without changing it. Identify units, UVs, textures and parts.
```

Confirm it can read `SKILL.md` and its references. A successful read establishes discovery; an actual scene inventory establishes Blender access. Neither establishes slicing or physical printability.

## Use it

Codex example:

```text
$model-prep process /path/to/character.glb, use black, white and red.
Keep UVs and geometry unchanged. Preview the editable SVG first.
```

Claude Code / Antigravity examples:

```text
/model-prep process /path/to/ornament.obj, faithful contours, preserve UVs
/model-prep process /path/to/part.stl, use front.png and back.png as references
/model-prep resize /path/to/assembly.blend to 180 mm tall, check sliding fit
/model-prep split /path/to/assembly.glb for 220 x 220 x 250 mm, add keyed joints
/model-prep review contours on /path/to/model.blend, preview only
```

Provide/attach the actual files; file-picker syntax varies by client. On Windows, give full paths and quote those containing spaces. No printer volume is needed for artwork review. Colour count does not imply AMS availability. Corrections made in the delivered SVG remain authoritative on continuation.

## Update or remove

In the installed `model-prep` directory:

```text
git status --short
git pull --ff-only
```

If there are local edits, preserve/reconcile them first; do not force-reset. Keep model jobs outside the skill folder. To remove, move that specific `model-prep` folder out of the discovery directory after preserving local changes. No agent config or model data needs deletion.

## Validation and limits

Run from the repository root:

```text
python -m unittest discover -s tests -v
```

See [validation evidence and repeatable scenarios](docs/validation.md). The helper creates scaffolds and paired SVG presentations; it does not trace, approve, render, audit mesh colours or convert geometry. See [its exact input limits](references/artwork-review.md#svg-helper).

Installation paths were checked against primary documentation on **8 October 2026**. Cross-client live discovery, Blender colour transfer, slicer integration and physical prints have not been tested for this release. A successful helper test is not evidence for those operations.

MIT licensed. Original models and third-party tools keep their own licences.
