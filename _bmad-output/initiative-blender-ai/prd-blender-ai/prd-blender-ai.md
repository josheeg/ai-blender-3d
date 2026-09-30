---
title: blender-ai PRD
created: 2026-09-30
updated: 2026-09-30
status: final
---

# PRD: blender-ai

## 0. Document Purpose

This PRD captures the scope, features, and definition of done for blender-ai, an AI-to-Blender interface that generates 3D game assets and 3D-printable scenes from natural-language prompts. It is for the product manager (John), the system architect (Winston), the UX designer (Sally), and the engineering lead (Amelia), and any downstream agent implementing tickets. It builds on the AGENTS.md and pyproject.toml in the repository root — those define the runtime and contribution rules. This PRD drives UX, architecture, and ticketing.

## 1. Vision

blender-ai lets a 3D artist or game developer describe a model in natural language ("a ruined stone tower with ivy, low-poly for games") and get back a Blender-ready asset — either a low-poly game model (GLTF with UVs) or a manifold, print-ready mesh (STL/OBJ). Today the creator switches between an AI chat and Blender, copies meshes, hand-fixes topology, and re-imports — a multi-step, error-prone loop that kills iteration speed. blender-ai inserts an MCP server between the AI and Blender so the generator stays conversational (including interactive party-mode prompt refinement) while the deliverable stays Blender-native. Result: one prompt, one valid asset, ready for the game engine or printer, in under ten minutes.

## 2. Target User

### 2.1 Jobs To Be Done

- **Functional:** When I have a vague idea for a game asset or 3D print, I want to iterate on it in plain language so I don't need to model it by hand.
- **Emotional:** I want to feel like I'm directing Blender, not babysitting a generator that produces broken topology.
- **Contextual:** I'm working inside Blender on a project; I want the tool there, not in a browser.

### 2.2 Non-Users (v1)

- Teams needing batch asset generation across a render farm.
- End consumers of a game or print — the tool serves creators, not players.
- Users without a local Blender install (cloud-only creators are v2).

### 2.3 Key User Journeys

- **UJ-1. Maya turns a text brief into a game asset inside Blender.**
  - **Persona + context:** Maya, indie gamedev working solo on a Unity prototype. She's iterating daily and needs low-poly assets with clean UVs.
  - **Entry state:** Blender 4.x open, Blender Meshroom add-on scene loaded, blender-ai side panel visible. She has an active collection named "Assets".
  - **Path:** She opens the side panel, types "low-poly wooden crate with a metal handle, game-ready, clean UVs", clicks Generate. The panel streams a low-res preview, then offers Regenerate, Refine (party-mode prompts), or Accept. She accepts.
  - **Climax:** A new object appears in her Assets collection: a manifold mesh with UVs unwrapped and assigned to a "GameAsset" collection.
  - **Resolution:** Maya drags the object into her Unity scene. The model imports cleanly, no non-manifold fixes required.
  - **Edge case:** If the generator returns non-manifold geometry, the panel flags it and offers "Fix topology" or "Regenerate".

- **UJ-2. Dana needs a 3D-printable scene from a prompt.**
  - **Persona + context:** Dana, tabletop miniature designer. She wants a printable base for a miniature, manifold, minimum wall thickness 2mm.
  - **Entry state:** Blender open with the 3D Print Toolbox add-on enabled, millimeter scene units.
  - **Path:** In the side panel, she selects "Print-ready mode", types "hexagonal dungeon tile, 50mm base, manifold, 2mm walls", clicks Generate.
  - **Climax:** The mesh validates in the 3D Print Toolbox with zero errors; Export STL appears.
  - **Resolution:** Dana prints the tile directly — first-time success.

## 3. Glossary

- **Game asset** — A 3D model optimized for real-time engines: low-poly, manifold, UV unwrapped, assigned to a collection. Contrast with **Print-ready asset**.
- **Print-ready asset** — A 3D model validated for physical manufacturing: fully manifold, no self-intersections, wall thickness within printer constraints.
- **MCP server** — The model-context-protocol server that mediates between the AI and Blender's Python API.
- **UVs** — UV-unwrapped texture coordinates; required for game assets, optional for print assets.
- **Low-poly** — Under a poly budget (v1: <2k faces) to keep game engines performant.
- **Manifold** — A mesh with no non-manifold edges, suitable for 3D printing.

## 4. Features

### 4.1 Prompt-to-Asset Pipeline

**Description:** The core feature: a user submits a natural-language prompt and receives a Blender object that meets the quality bar for the chosen output mode (game asset / print-ready). Realizes UJ-1, UJ-2. Supports refinement loops via party-mode prompt iteration. Uses Glossary terms exactly.

[ASSUMPTION: The AI model behind the MCP server returns a Blender-ready mesh (e.g. BMesh operations or a Python script), not a raw point cloud that needs reconstruction.]

**Functional Requirements:**

#### FR-1: Generate asset from prompt

User can submit a natural-language prompt and receive a Blender object matching the chosen output mode (game asset or print-ready). Realizes UJ-1, UJ-2.

**Consequences (testable):**
- A mesh object named after the asset appears in the active collection.
- Game assets have <2k faces; print-ready assets validate as manifold in the 3D Print Toolbox.
- The panel reports a status ("Generating", "Ready", "Error") with a timestamp.

#### FR-2: Refine the result

User can request refinements via follow-up prompts (party-mode interaction) and get an updated mesh without leaving Blender.

**Consequences (testable):**
- A new "Refine" field appears after generation; submitting a prompt re-runs the generator.
- History of generations is tracked in the session log.

**Out of Scope:**
- Training or fine-tuning the model itself.

### 4.2 Output Mode Selector

**Description:** The user picks whether the asset targets real-time engines (game asset) or 3D printing (print-ready). Realizes UJ-1 (game), UJ-2 (print).

#### FR-3: Switch output mode

User can toggle between "Game Asset" and "Print-Ready" before generation; the validation criteria and export format change accordingly.

**Consequences (testable):**
- Game mode exports GLTF with UVs; print mode exports STL with manifold validation.
- The panel updates the export button label and format dynamically.

## 5. Non-Goals (Explicit)

- This product is *not* a full Blender modeling suite — it's a generation tool.
- It will *not* edit existing meshes in v1 (generation only).
- It is *not* a web app or mobile app.
- `[NON-GOAL for MVP]` No batch/bulk generation across multiple prompts.
- `[NON-GOAL for MVP]` No custom model fine-tuning.

## 6. MVP Scope

### 6.1 In Scope

- Blender side-panel with prompt input and "Generate" button.
- One-click generation of a game asset (low-poly, UVs) or print-ready mesh (manifold).
- Export to GLTF (game) or STL (print).
- Error handling: flag non-manifold geometry with a retry offer.
- Party-mode refinement of an in-progress asset.

### 6.2 Out of Scope for MVP

- Batch processing of >1 asset. `[NOTE FOR PM]` Emotionally load-bearing — many creators want "generate my whole level." Revisit for v2.
- Cloud/model-server integration; local inference only. `[NOTE FOR PM]` Revisit when latency becomes a blocker.
- Multi-user collaboration.

## 7. Success Metrics

- **SM-1 (primary):** 90% of prompts produce a valid mesh that passes the chosen quality gate (GLTF+UVs for game, manifold for print) within 10 minutes, measured over 100 test prompts. Validates FR-1.
- **SM-2 (secondary):** 70% of generated assets are accepted without a refinement request on first delivery. Validates FR-2.
- **SM-C1 (counter-metric):** Do not optimize for prompt length or generation speed at the cost of mesh validity. `[NOTE FOR PM]` A 30-second broken mesh is less valuable than a 90-second valid one.

## 8. Open Questions

1. **Model backend:** Local LLM/MCP server (Ollama/ComfyUI) or external API? Affects FR-1 testability and the dependency policy in AGENTS.md.
2. **Blender version target:** Does the side panel require the latest Blender, or support 3.6 LTS? [ASSUMPTION: v1 targets Blender 4.x.]
3. **Prompt party mode scope:** How far does the interactive refinement go? (a single follow-up, or full agent conversation?)

## 9. Assumptions Index

- Inline assumption from §4.1 — The AI returns a Blender-ready mesh via the MCP server, not a raw point cloud requiring reconstruction.
- §6.1 — Local inference is sufficient for v1 performance (10-minute SLA).
- §6.2 — Cloud/model-server integration is out of scope for v1.
- §8 — Blender 4.x is the target version for v1.

---

*[This is a draft PRD. Review, refine, and finalize before handing off to UX and architecture.]*