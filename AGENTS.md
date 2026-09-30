<!-- bmad:context -->
<!-- Verified 2026-09-30 against 61d1745. Managed by bmad-project-context; edits inside this block are replaced on refresh. Keep anything you want preserved outside the markers. -->

## blender-ai

AI-to-Blender interface. Python 3.14, packaged with `uv` under `src/blender_ai/`. Agent skills for this repo live in `.agents/skills/`, vendored from `bmad-code-org/BMAD-METHOD` and hash-pinned in `skills-lock.json`.

## Where things are

- Never hand-edit `.agents/skills/**` — update upstream and re-run `npx skills experimental_install`, or the lock hashes no longer match.

## Running and verifying

- Run the project through `uv run` (e.g. `uv run blender-ai`); a bare `blender-ai` does not resolve, the script is only in `.venv\Scripts\`.
- Use `uv run pyinstaller` to bundle; a bare `pyinstaller` does not resolve.
- Run tests via `uv run pytest`; a bare `pytest` resolves to Python 3.12 (global), not the project's 3.14 venv.

<!-- /bmad:context -->