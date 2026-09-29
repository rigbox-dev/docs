# CLI reference maintenance

The committed `cli-reference/command-surface.json` describes CLI revision
1880d04137a5f0bb323170fe5ef0e634b7570f03 (version string 0.13.0-rc.4). It was not
produced by the exporter: that revision was not built for documentation, so the file
was reconstructed from the `--help` output of a build of it (local mode, and workspace
mode via `RIGBOX_WORKSPACE_CONFIG`), with global options taken from the revision's
`tests/snapshots/help_snapshots__*_root.snap` and argument metadata that help text
does not show (ids, actions, conflicts, groups, hidden aliases) carried over from the
previous export of v0.13.0-rc.2 (09bd4024dd729ef31ae62f0f6985849974a9651d). The
reconstruction reproduced all 182 commands whose help had not changed byte for byte
before it was applied to the rest. Replace it with a real export when that revision,
or a release containing it, is exported.

Generate the export with `cargo run --example export_docs` from the CLI checkout. The
exporter is a Cargo example, not a production command.

From this documentation checkout:

```bash
python3 scripts/generate-cli-reference.py --source /tmp/rigbox-command-surface.json
python3 scripts/generate-cli-reference.py --check
```

The generator writes one page per canonical non-hidden command path and
`scripts/cli-navigation.json` as a command hierarchy inventory (individual commands are intentionally excluded from the sidebar). It merges local/workspace
surfaces by canonical path; each mode retains its own usage and flag table.
Clap's auto-generated help-routing tree is omitted to avoid duplicate command
pages. Aliases link to the canonical command.

`cli-reference/command-notes.json` holds independently maintained descriptions
and example commands. Generation never overwrites it. Adding a command without
examples fails. After reviewing an export update, add its examples, regenerate,
and run the CLI's offline parser against the generated sample inventory:

```bash
cargo run --example export_docs -- --validate-examples /path/to/rigbox-docs/scripts/cli-examples.json
```

This validates command syntax without executing operations or requiring account
credentials. It does not establish backend acceptance, resource availability, or
runtime success. Examples use uppercase placeholders for resource identifiers.
The generator's `--check` detects changed or extra generated pages and stale
navigation/sample inventories. To detect drift against a new CLI source, run
`--source /tmp/new-export.json --check`; the export metadata also changes when the
source revision changes.

Public Clap introspection exposes conflicts and required groups. Conditional
requirements without public getters remain represented by authoritative help and
usage; the exporter metadata explicitly records this limit. Do not invent rules
from human-readable usage. CLI parser tests are the final syntax check.
