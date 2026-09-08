# v0.13 preview review

Date: 2026-09-08. Preview: http://localhost:3000/introduction. Initial preview review; publication subsequently authorized by the user.

## Static and offline checks

- Strict Mintlify 4.2.375 build validation passed. The prior `/docs.json` OpenAPI warning was resolved by explicit specification paths in API frontmatter and removing the ambiguous top-level config key.
- Mintlify broken-links passed.
- 357 pages have unique canonical navigation entries; local links, legacy routes/anchors, and OpenAPI references passed `scripts/check-docs.py`.
- 149 generated command pages match the committed Clap export, covering 142 local and 108 workspace command paths. 274 curated command invocations passed offline Clap parsing after regeneration.
- 31 example manifests passed the reviewed CLI parser and project normalization. 18 deploy Action offline tests passed. These are syntax/source checks, not successful runtime deployments.

## Browser checks

The homepage, nested dependency guide, manifest reference, deepest CLI page (`app/env/set`), frontend/API example, and app-release API endpoint were rendered at 390, 768, 1024, 1440, and 2200 CSS pixels in both light and dark appearance. All 60 combinations had no document-level horizontal overflow or missing pages; dimensions are in `responsive-results.json`. Representative screenshots were visually inspected across mobile/tablet/desktop layouts. Code and API samples intentionally scroll internally.

Verified in the preview: edge-aligned rail, centered article/API containers, 720px article column and 208px outline at wide desktop, native mobile header, full nested breadcrumbs, active CLI ancestors, unrelated branches initially collapsed, separate overview links, group expansion without navigation, native area selection by keyboard (subsequently replaced with an always-visible sidebar at user request), heading anchors, and code copying (clipboard matched the homepage command exactly). The native API Try it form opens with authorization and path inputs; no API request was submitted through the playground.

Search opens its native dialog but explicitly reports **Not available on local preview**. Search results must be checked in a hosted preview before publication. Native theme switching was tested in both directions. Default/system appearance continues to use Mintlify's native control; OS preference changes were not separately automated. Text and neutral/accent contrast were visually reviewed; this was not a complete WCAG audit.

## Release gates still open

See `live-tests.md`: two isolated incremental releases prepared successfully, then activation failed before the application started (`200/CHDIR`, permission denied in managed release directories). Both disposable workspaces were removed and usage returned to its baseline.

Successful first deploy, redeploy, staging/activation, failed-health recovery, app rollback retaining data, multi-app selection, and image deployment still require live verification. Console GitHub and GitHub Actions end-to-end scenarios (including private repositories, subdirectories, credentials, and failures) remain unverified. Third-party agent/provider installations were not run. Builds/image-release APIs absent from the reviewed server spec were not fabricated.

The reviewed CLI is 0.13.0-rc.2. Publication requires stable CLI availability, server readiness, compatible Action, completed live checks, hosted search review, and user review of this preview.

## Publication update

The user explicitly authorized publication after the preview review, requested a single visible sidebar, and removed the upgrade guide. The banner and upgrade page were removed; version requirements remain explicit because the current stable CLI is v0.12.68 and v0.13.0-rc.2 is a prerelease. This publication does not assert that the outstanding runtime checks passed. The corrected example manifests are available on the linked examples branch.
