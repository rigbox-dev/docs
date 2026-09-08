# Rigbox documentation

Rigbox documentation uses Mintlify. The documentation redesign was approved for publication on 2026-09-08. v0.13 commands currently require the release candidate; installation guides state this explicitly. See `verification/sources.json` for reviewed revisions and `verification/live-tests.md` for outstanding runtime verification.

## Preview

```bash
npx mintlify@4.2.375 dev --port 3000
```

Open http://localhost:3000/introduction. Publishing to `main` triggers the connected Mintlify deployment. Run validation and review changes before publishing.

## Structure

`docs.json` retains Mintlify's `mint` theme, Docs/API Reference tabs, a single visible sidebar, search, mobile navigation, breadcrumbs, and API playground. Nine always-visible sidebar sections separate app deployment, configuration, workspaces, AI, operations, examples, CLI lookup, and API integrations. Group overviews are explicit first links: Mintlify's `root` setting navigates on expansion, so it is deliberately normalized into a page by the navigation builder.

`style.css` keeps the sidebar at the edge and centers content in the remaining space. Homepage styles are scoped under `.rigbox-home`. Articles use a 720px column and a 208px outline on wide screens; API prose and samples share a wider centered container. Geist Sans/Mono, neutral surfaces, and restrained green work in light and dark appearance.

Existing routes and heading anchors are inventoried in `scripts/legacy-routes.json`. Keep extracted sections as short signposts at their original anchors. Each page has one canonical navigation location.

## Maintenance and verification

```bash
python3 scripts/generate-cli-reference.py --check
python3 scripts/build-navigation.py --check
python3 scripts/check-docs.py
npx mintlify@4.2.375 validate
npx mintlify@4.2.375 broken-links
```

Edit `scripts/build-navigation.py` for curated navigation, then run it without `--check`. CLI syntax comes from an offline Clap exporter in the CLI repository. Curated explanations/examples live separately in `cli-reference/command-notes.json`; see `scripts/generate-cli-reference.md` for export, regeneration, and offline command parsing. Never edit generated command pages directly.

Example tutorials use the examples repository as their runnable source. Its v0.13 corrections are published on `codex/examples-docs-v013`; tutorials link to the recorded source commit and clone that branch. The CLI's `documentation_example_manifests_normalize` test validates that checkout against the real manifest parser. This does not establish deployment success. Runtime, GitHub console, and GitHub Actions checks are separate release gates. Run `scripts/check-related-repositories.sh` with `RIGBOX_DOCS_CLI_DIR` and `RIGBOX_DOCS_EXAMPLES_DIR` exported to verify the related checkouts offline; use the CLI’s required Rust toolchain (tested with `RUSTUP_TOOLCHAIN=1.95.0`).

## API definitions

API pages name their specification explicitly:

```mdx
---
title: List Workspaces
openapi: /openapi/rigbox-api.json GET /api/v1/workspaces
---
```

Do not add top-level `openapi` to `docs.json`: Mintlify 4.2.375's file categorizer misidentifies that configuration as an API specification. Explicit page references resolve the strict validation warning. Native endpoints and playground contracts remain unchanged. App-release and volume definitions are copied from the recorded server specification. Builds/image-release routes absent from that specification remain covered by CLI guides; do not invent generated API definitions.

The existing `sync-openapi.yml` workflow updates production specs. Review its output against the targeted release before incorporating it into the docs; newly split specifications also need deliberate refresh and coverage review. Contract changes belong in the server source, not hand edits to documentation schemas.
