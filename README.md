# Rigbox Documentation

API documentation for [Rigbox](https://rigbox.dev), hosted at [docs.rigbox.dev](https://docs.rigbox.dev) via [Mintlify](https://mintlify.com).

## How it works

```
Rust services (utoipa annotations)
        │
        │  generates OpenAPI JSON at runtime
        ▼
api.rigbox.dev/api-docs/openapi.json
        │
        │  fetched weekly by CI, saved as static files
        ▼
This repo
├── openapi/rigbox-api.json      ← 80 endpoints (main API)
├── openapi/auth-api.json        ← 12 endpoints (access control)
├── docs.json                    ← Mintlify config + navigation
├── api-reference/**/*.mdx       ← 98 pages, each points to a spec operation
└── *.mdx                        ← Hand-written prose pages
        │
        │  push to main → Mintlify auto-builds
        ▼
docs.rigbox.dev  ←  CNAME → cname.mintlify.app
```

### API reference pages

Most pages use `openapi:` frontmatter to auto-generate content from the spec:

```mdx
---
title: Create Workspace
openapi: POST /api/workspaces
description: Provision a new workspace with custom resources.
---
```

Mintlify matches the operation against `openapi/rigbox-api.json` or `openapi/auth-api.json` and renders request/response schemas, code examples, and a "Try It" playground.

A few endpoints without utoipa annotations use manual `api:` frontmatter with hand-written params and examples (api-keys, capacity, images, reconcile, visibility, status).

### Prose pages

- `introduction.mdx` — Platform overview and architecture
- `authentication.mdx` — Auth methods (API keys, JWTs, session tokens)
- `quickstart.mdx` — Deploy your first workspace in 5 steps
- `sandbox-api-surface.mdx` — Which APIs power sandbox.rigbox.dev
- `clawd-api-surface.mdx` — Which APIs power clawd.rigbox.dev
- `clawd-runtime-services.mdx` — Managed AI proxy service contracts

## Updating the docs

| What changed | What to do |
|---|---|
| New endpoint in Rust | Add utoipa annotation → deploy → CI auto-syncs spec → create `.mdx` page → add to `docs.json` nav |
| Endpoint behavior changed | Update description in `openapi/*.json` → push |
| Prose needs updating | Edit the `.mdx` file → push |
| New integration guide | Create `.mdx` → add to `docs.json` nav → push |

## OpenAPI spec sync

The static spec files are kept in sync with production via the `sync-openapi.yml` GitHub Action. It runs weekly and on-demand, fetching fresh specs from `api.rigbox.dev`, preserving any hand-written descriptions, and opening a PR if there are changes.

**Manual trigger:** Go to Actions → Sync OpenAPI Specs → Run workflow.

### How description preservation works

The utoipa-generated specs don't include `description` fields on endpoints — those are added manually in this repo. The sync workflow merges new spec data while keeping existing descriptions intact, so hand-written docs aren't overwritten.

## Local development

```bash
npx mintlify dev
```

This starts a local preview server at `http://localhost:3000`.

## DNS

`docs.rigbox.dev` is a CNAME in Cloudflare pointing to `cname.mintlify.app`. No Caddy or VPS configuration needed — Mintlify handles hosting and TLS.
