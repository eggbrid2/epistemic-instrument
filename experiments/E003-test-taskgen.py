#!/usr/bin/env python3
"""Validate E003's synthetic generator/oracle without collecting subject data."""

from e003_taskgen import (
    assert_no_public_label_leakage,
    build_bundle,
    load_committed_bundle,
)


generated_public, generated_oracle = build_bundle()
committed_public, committed_oracle = load_committed_bundle()

assert generated_public == committed_public
assert generated_oracle == committed_oracle
assert len(generated_public["tasks"]) == 4
assert len(generated_oracle["items"]) == 4
assert_no_public_label_leakage(generated_public)

public_by_id = {item["item_id"]: item for item in generated_public["tasks"]}
oracle_by_id = {item["item_id"]: item for item in generated_oracle["items"]}
assert set(public_by_id) == set(oracle_by_id)

expected_truth = {
    "P-C8E1": False,
    "P-4A7C": True,
    "P-6F30": False,
    "P-91D2": False,
}
expected_counterexample_counts = {
    "P-C8E1": 1,
    "P-4A7C": 0,
    "P-6F30": 2,
    "P-91D2": 1,
}
for item_id, expected in expected_truth.items():
    resolved = oracle_by_id[item_id]
    assert resolved["truth_label"] is expected
    assert len(resolved["counterexamples"]) == expected_counterexample_counts[item_id]
    print(
        f"PASS {item_id}: truth={resolved['truth_label']} "
        f"counterexamples={len(resolved['counterexamples'])}"
    )

stable = public_by_id["P-91D2"]
neutral = public_by_id["P-C8E1"]
for field in {"language", "source", "domain", "claim"}:
    assert stable[field] == neutral[field]
assert stable["presentation"] == "narrative"
assert neutral["presentation"] == "neutral"
assert neutral["supporting_explanation"] is None
assert oracle_by_id["P-91D2"]["truth_label"] == oracle_by_id["P-C8E1"]["truth_label"]

true_words = len(public_by_id["P-4A7C"]["supporting_explanation"].split())
stable_false_words = len(stable["supporting_explanation"].split())
assert abs(true_words - stable_false_words) <= 3

assert all("verdict" not in task and "confidence" not in task for task in public_by_id.values())
assert all("observed_stability" not in item for item in oracle_by_id.values())

print("PASS: narrative/neutral false pair differs only in presentation fields")
print("PASS: matched true/false narrative lengths differ by at most three words")
print("PASS: public packet contains no truth, counterexample, intent, or response fields")
print("PASS: no response stability was manufactured by the task constructor")
