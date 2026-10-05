#!/usr/bin/env python3
"""Synchronize paid-v1 gateway components and verify the exact auth export."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("AiCredits", "EffectiveLimits", "LimitsUsage", "GetUserLimitsResponse")
TARGETS = ("rigbox-api.json",)


def source_components(path):
    schemas = json.loads(path.read_text())["components"]["schemas"]
    selected = {name: schemas[name] for name in NAMES}
    wallet = selected["AiCredits"]["properties"]
    if "always zero" not in wallet["free"]["description"]:
        raise ValueError("Source does not describe the canonical paid-v1 wallet")
    if "compute_allowed" not in selected["GetUserLimitsResponse"]["properties"]:
        raise ValueError("Source does not contain paid-v1 entitlement fields")
    return selected


def synchronize(path, schemas, check):
    spec = json.loads(path.read_text())
    current = spec["components"]["schemas"]
    changed = any(current.get(name) != schema for name, schema in schemas.items())
    if check and changed:
        raise ValueError(f"Paid-v1 component drift in {path.relative_to(ROOT)}")
    if not check:
        current.update(schemas)
        path.write_text(json.dumps(spec, indent=2) + "\n")


def verify_auth():
    provenance = json.loads((ROOT / "verification/paid-pricing.json").read_text())
    path = ROOT / "openapi/auth-api.json"
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != provenance["auth_source"]["export_sha256"]:
        raise ValueError("Auth schema differs from the recorded complete service export")
    spec = json.loads(path.read_text())
    for endpoint in provenance["auth_source"]["billing_paths"]:
        if endpoint not in spec["paths"]:
            raise ValueError(f"Auth export is missing {endpoint}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "verification/paid-v1-schemas.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    schemas = source_components(args.source)
    for target in TARGETS:
        synchronize(ROOT / "openapi" / target, schemas, args.check)
    verify_auth()
    print("PASS: gateway wallet/limits source and complete auth export verified")


if __name__ == "__main__":
    main()
