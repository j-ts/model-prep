# Tool setup and capability discovery

Read this when preparing the environment or when a required capability is missing. The skill does not silently install software, replace existing agent configuration or start printer jobs. Reuse configured tools first; setup changes require the user's request/authorization.

## Blender control

Preferred route: a locally connected Blender MCP implementation exposing scene inspection and Blender Python execution. Discover actual tool names and installed Blender version, then run a read-only inventory. A configured server entry alone does not prove a connection.

For the community implementation formerly called `blender-mcp`, the current upstream is [mcp-for-blender](https://github.com/ahujasid/mcp-for-blender). It requires Blender 3+, Python 3.10+ and `uv`. Follow its current prerequisites, then:

```text
uvx mcp-for-blender setup
```

This interactive upstream setup selects clients and installs the add-on. Reopen Blender/client afterward. For manual setup:

```text
uvx mcp-for-blender install-addon
codex mcp add blender -- uvx mcp-for-blender
claude mcp add blender uvx mcp-for-blender
```

Run only the client command you need. Enable the Blender add-on and check its viewport-sidebar server. GUI clients may need an absolute `uvx` path. Keep the Blender socket local; it can execute Python. Set `DISABLE_TELEMETRY=true` in the MCP process environment if disabling upstream telemetry. The old `uvx blender-mcp` command remains a compatibility path. These are upstream setup instructions, not bundled dependencies or a claim of tested connectivity.

For Antigravity, use its **MCP Servers → Manage MCP Servers → View raw config** interface, or documented global `~/.gemini/config/mcp_config.json` / workspace `.agents/mcp_config.json`. Merge the entry into existing configuration without replacing other servers:

```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["mcp-for-blender"],
      "env": {"DISABLE_TELEMETRY": "true"}
    }
  }
}
```

Use `/mcp` in the CLI to inspect/reload. [Antigravity MCP documentation](https://www.antigravity.google/docs/mcp)

## Direct Blender fallback

If MCP is unavailable but local Blender and shell access exist, execute a small inspected Blender Python job against a **working copy**, saving to a new output. Resolve the installed executable and supported operators instead of guessing version-specific APIs. Disable auto-execution of embedded project scripts where supported, avoid source overwrite and preserve dependencies.

Blender UI scripting is also valid when available. With no Blender execution route, finish only file/appearance review that available tools can support and mark scene mutation blocked. Do not write a nominal `.blend` file or fake an inventory.

## SVG editing and rendering

The bundled helper needs only Python 3.10+. For user editing, open the actual saved SVG in Inkscape or another layer/path-capable vector editor. Use an available local SVG renderer/editor for visual inspection and PNG presentation; check the installed CLI help before constructing commands. The helper does not install a renderer. Keep the original raster embedded and avoid external asset URLs.

## Optional Bambu companion

[bambu-studio-ai](https://github.com/heyixuan2/bambu-studio-ai) can supply analysis, profile information, export and slicer handoff. Install it separately in the appropriate agent skill directory, using its current setup instructions. Its Python dependencies belong in an isolated environment; run its `scripts/doctor.py` to see available capabilities. Do not assume installing this skill also installs that companion.

Read installed `SKILL.md`, relevant references and tool `--help` before delegation. Profile/format behaviour can differ by version. For non-Bambu workflows, use the user's usable dimensions and target format without demanding printer connections or AMS configuration.

## Verification record

Record the tool/version, input artifact and observed result for any actual integration check. “Documented by upstream”, “capability verified on a prior job”, “this export checked”, “this slice inspected” and “physically trialled” are distinct evidence levels. Missing tools block only their dependent stages.
