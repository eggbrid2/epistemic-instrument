#!/usr/bin/env python3
"""Validate frozen E002 design and print normative values; collect no responses."""

import json
import math
from pathlib import Path


DESIGN_PATH = Path(__file__).with_name("E002-design.json")


def posterior(prior: float, p_e_a: float, p_e_b: float) -> float:
    numerator = prior * p_e_a
    return numerator / (numerator + (1.0 - prior) * p_e_b)


design = json.loads(DESIGN_PATH.read_text(encoding="utf-8"))
assert design["status"] == "design_frozen_no_responses"
assert len(design["cases"]) == 8
assert set(design["conditions"]) == {"neutral", "story"}

seen = set()
for case in design["cases"]:
    assert case["id"] not in seen
    seen.add(case["id"])
    numeric = [value for key, value in case.items() if key != "id"]
    assert all(0.0 < value < 1.0 for value in numeric)

    lr1 = case["e1_given_HA"] / case["e1_given_HB"]
    lr2 = case["e2_given_HA"] / case["e2_given_HB"]
    assert lr1 > 1.0
    assert lr2 < 1.0

    p1 = posterior(
        case["prior_HA"], case["e1_given_HA"], case["e1_given_HB"]
    )
    p2 = posterior(p1, case["e2_given_HA"], case["e2_given_HB"])
    print(
        f"{case['id']}: p1*={p1:.6f} p2*={p2:.6f} "
        f"normative_delta={math.log(lr2):.6f}"
    )

print("PASS: 8 cases, 2 conditions, 16 planned independent responses")
