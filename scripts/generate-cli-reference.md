# CLI reference maintenance

The committed `cli-reference/command-surface.json` is an offline Clap export from
CLI v0.13.0-rc.2, revision 09bd4024dd729ef31ae62f0f6985849974a9651d. Generate it with
`cargo run --example export_docs` from the CLI checkout. The exporter is a Cargo
example, not a production command.

From this documentation checkout:

```bash
python3 scripts/generate-cli-reference.py --source /tmp/rigbox-command-surface.json
python3 scripts/generate-cli-reference.py --check
```

The generator writes one page per canonical non-hidden command path and
`scripts/cli-navigation.json` for Mintlify navigation. It merges local/workspace
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
