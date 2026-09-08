#!/usr/bin/env bash
# Offline validation only. Run from the documentation checkout.
set -euo pipefail
: "${RIGBOX_DOCS_CLI_DIR:?Set RIGBOX_DOCS_CLI_DIR to the reviewed CLI checkout}"
: "${RIGBOX_DOCS_EXAMPLES_DIR:?Set RIGBOX_DOCS_EXAMPLES_DIR to the reviewed examples checkout}"
docs_dir="$(pwd)"
cd "$RIGBOX_DOCS_CLI_DIR"
cargo run --example export_docs -- --validate-examples "$docs_dir/scripts/cli-examples.json"
cargo test documentation_example_manifests_normalize -- --ignored --nocapture
