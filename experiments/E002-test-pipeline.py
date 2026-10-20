#!/usr/bin/env python3
"""Exercise E002 pipeline with synthetic data only."""

import json
import math
from pathlib import Path

from e002_pipeline import load_design, make_annotation_bundle, score_record


FIXTURE_PATH = Path(__file__).with_name("fixtures") / "E002-synthetic-fixtures.json"

design = load_design()
payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
assert payload["notice"].startswith("SYNTHETIC")
fixtures = payload["fixtures"]
records = [fixture["record"] for fixture in fixtures]

packet, manifest = make_annotation_bundle(records, design)
assert len(packet["items"]) == 3
assert len(packet["excluded"]) == 1
assert len(manifest["mapping"]) == 4
assert all("case_id" not in item and "condition" not in item for item in packet["items"])
assert all(record["metadata"]["data_class"] == "synthetic" for record in records)

for fixture in fixtures:
    result = score_record(fixture["record"], fixture["annotation"], design)
    expected = fixture["expected"]
    assert result["status"] == expected["status"], fixture["name"]
    assert result["data_class"] == "synthetic", fixture["name"]
    if result["status"] == "invalid":
        print(f"PASS {fixture['name']}: rejected as invalid")
        continue
    assert result["update_direction"] == expected["update_direction"], fixture["name"]
    assert result["gap_instance"] is expected["gap_instance"], fixture["name"]
    if "ume" in expected:
        assert math.isclose(result["update_magnitude_error"], expected["ume"], abs_tol=1e-12)
    if "fpe" in expected:
        assert math.isclose(result["final_posterior_error"], expected["fpe"], abs_tol=1e-12)
    print(
        f"PASS {fixture['name']}: UD={result['update_direction']} "
        f"UME={result['update_magnitude_error']:.6f} "
        f"FPE={result['final_posterior_error']:.6f} "
        f"RCS={result['rhetorical_caution_score']:.6f} "
        f"gap={result['gap_instance']}"
    )

print("PASS: annotation bundle hides case/condition and preserves one exclusion")

damaged = dict(records[0])
del damaged["collection_id"]
damaged_packet, damaged_manifest = make_annotation_bundle([damaged], design)
assert not damaged_packet["items"]
assert len(damaged_packet["excluded"]) == 1
assert damaged_manifest["mapping"][0]["parse_status"] == "invalid"
print("PASS: missing identity field is preserved as an invalid exclusion")
