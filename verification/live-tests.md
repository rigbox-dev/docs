# v0.13 live verification

Date: 2026-09-08. CLI built from revision `09bd402` (`0.13.0-rc.2`).
This is a release-candidate preview, not evidence of a stable release publication.

## Read-only preflight

- Existing authenticated account: successful (identity and credentials omitted).
- Fleet capacity: 10 of 20 workspace slots in use; available.
- Account usage: 3 of 10 workspaces, 5 of 10 running vCPUs.
- Test uses a new 512 MiB / 1 vCPU workspace only.

## Owned test resources

- Workspace: `ws-bv6413tn`, named `docs-v013-smoke-20260908-0255`.
- Fixture: Python HTTP service with no credentials or user data. Public route only
  exposes a version string and a disposable persistence marker.
- Marker sits outside managed app releases; this checks retained workspace data,
  not volume recovery, snapshots, or database migration compatibility.

## Results

Baseline failed; see the final result and cleanup evidence below.

## Other verification

- All 31 edited example manifests passed the v0.13 CLI parser and normalization.
- Deploy Action: 18 offline tests passed.
- GitHub console/Actions live integration was not run: no isolated test repository
  and workflow-dispatch authorization were supplied. No repository binding or
  workflow was created or modified.

## Final result: blocked by release directory permissions

The first release `apr-hs2ygg8s` reached `ready`, then failed activation with exit1
and app outcome `not_deployed`. The CLI reported:
`[Rigbox] Activation failed; previous releases restored`.

A second new workspace (`ws-kyvrdbxr`, `docs-v013-minimal-20260908-0634`) used the
standard-library command `python3 -m http.server 8080 --bind 0.0.0.0`, health path
`/`, and a 30-second timeout. This removes the custom handler and persistence
marker from the test. Release `apr-v7rejkff` again reached ready, then failed.

Read-only SSH verified `/usr/bin/python3` exists. The managed service journal
identified a failure before Python could execute:

```text
Changing to the requested working directory failed: Permission denied
Failed at step CHDIR spawning /bin/bash: Permission denied
Main process exited, code=exited, status=200/CHDIR
```

Directory inspection showed `/opt/rigbox/app-releases` and its `current` directory
owned by `root:root` with mode `0700`. This prevents the managed application user
from traversing the release path. No product code or server permission was changed
to work around the fault.

Redeploy, explicit stage/activate, failed application health recovery, rollback
with retained data, and multi-app lifecycle checks were **not run** after this
baseline failed. Image deployment was not expanded into a separate test; no image
compatibility claim is made.

## Cleanup completed

Both test workspaces were deleted successfully with `workspace rm`. A subsequent
workspace listing contained neither owned ID. The retry's automatically provisioned
data volume was `vol-cju1wzc7`. Separate removal while running was rejected with
`Stop the workspace before deleting a volume`; workspace deletion then completed.
No existing user workspace, app, or volume was selected for mutation.

Post-cleanup account usage matched preflight exactly: 3 workspaces, 5 running
vCPUs, 23,552 MiB total disk, and 8,192 MiB RAM.
