#!/usr/bin/env python3
"""Deterministic scorer for E001. Uses only the Python standard library."""

import json
from pathlib import Path


CASE_PATH = Path(__file__).with_name("E001-case.json")


def rhetoric_score(features: dict[str, bool]) -> float:
    if len(features) != 6:
        raise ValueError("RCS requires exactly six frozen feature annotations")
    return sum(bool(value) for value in features.values()) / len(features)


def update_fidelity(reported: float, target: float) -> float:
    if target != 0.5:
        raise ValueError("E001's normalization is valid only for target 0.5")
    return max(0.0, 1.0 - abs(reported - target) / 0.5)


case = json.loads(CASE_PATH.read_text(encoding="utf-8"))
scores = {}
for agent in case["agents"]:
    scores[agent["id"]] = {
        "RCS": rhetoric_score(agent["rcs_features"]),
        "UFS": update_fidelity(
            agent["reported_posterior"], case["target_posterior"]
        ),
    }

rcs_winner = max(scores, key=lambda agent_id: scores[agent_id]["RCS"])
ufs_winner = max(scores, key=lambda agent_id: scores[agent_id]["UFS"])

assert rcs_winner == case["frozen_prediction"]["rcs_winner"]
assert ufs_winner == case["frozen_prediction"]["ufs_winner"]

for agent_id, agent_scores in scores.items():
    print(
        f"{agent_id}: RCS={agent_scores['RCS']:.4f} "
        f"UFS={agent_scores['UFS']:.4f}"
    )
print(f"PASS: RCS winner={rcs_winner}; UFS winner={ufs_winner}")
