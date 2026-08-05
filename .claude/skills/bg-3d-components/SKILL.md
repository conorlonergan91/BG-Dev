---
name: bg-3d-components
description: Create 3D board game components — miniatures, tokens, dice, custom pieces, board inserts/trays, and boxes — using the Blender MCP (organic/aesthetic pieces + renders) and, for precision print-first parts, FreeCAD or OpenSCAD MCP. Use whenever you need 3D models, print-ready STL/3MF for prototyping, or rendered component/box art. Covers setup, incremental prompting, millimetre units, and manifold/print checks.
---

# 3D component pipeline

Two complementary tools:

- **Blender MCP** — organic/aesthetic pieces (miniatures, sculpted tokens), renders, and box art.
- **FreeCAD MCP / OpenSCAD MCP** — precision, dimension-critical, print-first parts (dice, tokens,
  inserts/trays, boxes). Parametric CAD is more print-reliable (manifold, unit-correct) than mesh
  modelling.

Standardize on **STL (or 3MF)** for printing and **glTF / PNG** for previews/renders.

## Setup (Blender MCP)

Configured in `.mcp.json` as `blender` = `uvx blender-mcp`. To use it:

1. Install `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Install Blender (3.0+) and the **Blender MCP addon** (`addon.py` from
   `github.com/ahujasid/blender-mcp`): Blender → Preferences → Add-ons → Install, enable
   "Interface: Blender MCP".
3. In Blender's 3D View sidebar (`N`) → **BlenderMCP** tab → **"Connect to Claude"** (starts the socket
   on `localhost:9876`).
4. Keep Blender **open and connected** for the whole session — the tools are live, not headless.

**FreeCAD/OpenSCAD MCP** are optional add-ons (e.g. `neka-nat/freecad-mcp`, `quellant/openscad-mcp`);
wire them into `.mcp.json` if you want parametric precision parts.

## Blender MCP tools (what you can do)

- `get_scene_info`, `get_object_info` — inspect the scene/objects.
- `get_viewport_screenshot` — **see your work and self-correct** (use between steps).
- `execute_blender_code` — run arbitrary `bpy` Python (the workhorse: modifiers, booleans, arrays,
  bevel/solidify, mesh edits, render, export STL/3MF/OBJ/glTF).
- `create_object` / `modify_materials` / `delete_object` — convenience wrappers.
- Asset generation: **PolyHaven** (free HDRIs/textures/models), **Sketchfab** (key), **Hyper3D Rodin**
  & **Hunyuan3D** (text/image-to-3D; keys). Generated meshes are display-quality, **not print-ready**.

## Best practices (game components)

- **Prompt incrementally, verify with screenshots.** One component/step at a time; call
  `get_viewport_screenshot` + `get_scene_info`, then continue. Don't ask for a whole boxed game at once.
- **Pin real-world dimensions in mm** ("a hex token 25 mm across, 3 mm thick"; "a D6 with 16 mm edges").
  Set scene units to **millimetres** up front and confirm object dimensions before export — wrong
  scale is the #1 printing failure.
- **Parametric/procedural via `execute_blender_code`** (primitives + booleans + arrays + modifiers) for
  tokens/dice/inserts/boxes — precise and repeatable. Reserve Hyper3D/Sketchfab for organic minis /
  look-dev, then clean/retopologize for printing.
- **Print-readiness before STL export:** ensure **manifold/watertight** (every edge shared by exactly
  two faces), apply modifiers, and add a **Triangulate** modifier for anything with n-gons. Use
  Blender's 3D-Print Toolbox (or a manifold check script).
- **Save the .blend before agent sessions** — `execute_blender_code` runs with no undo safety net.

## Gotchas

- Blender must be open + addon connected; one MCP client on the socket at a time.
- The **first command is often flaky** — retry.
- Heavy ops (esp. glTF export) can **time out** (`MCP error -32001`); break work into small steps and
  export via short scripts.
- AI-generated meshes are usually non-manifold / wrong-scale — fine for renders, risky for STL without
  cleanup.

## File formats

| Format | Use for |
|--------|---------|
| **STL** | 3D printing (minis, dice, tokens, inserts, boxes). Scale must be baked correctly. |
| **3MF** | Better modern print format (units/color/multi-object) if your slicer supports it. |
| **OBJ** | Textured exchange / painted display pieces. |
| **glTF/GLB** | Real-time/preview & web viewers (can hit export timeouts). Not for printing. |
| **PNG (render)** | Box art, component previews, rulebook imagery (`bpy.ops.render.render`). |

## Output contract

- Save models/renders under `games/<slug>/build/3d/` (gitignored) or `art/` for finished renders.
- Report dimensions (mm), whether the mesh passed manifold/triangulate checks, and the export format.
- If Blender MCP isn't connected, say exactly what the human must open/connect; produce a parametric
  spec (or OpenSCAD script) they can run instead where possible.
