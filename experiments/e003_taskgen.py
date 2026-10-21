#!/usr/bin/env python3
"""Synthetic task generator and independent exhaustive oracle for E003 design."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PUBLIC_PATH = Path(__file__).with_name("fixtures") / "E003-synthetic-public.json"
ORACLE_PATH = Path(__file__).with_name("fixtures") / "E003-synthetic-oracle.json"

PUBLIC_KEYS = {
    "item_id",
    "data_class",
    "language",
    "source",
    "domain",
    "claim",
    "presentation",
    "supporting_explanation",
}

PROTOTYPE_SPECS = [
    {
        "item_id": "P-C8E1",
        "a": 2,
        "b": 1,
        "modulus": 17,
        "domain_max": 8,
        "presentation": "neutral",
        "supporting_explanation": None,
        "presentation_intent": "neutral_pair",
    },
    {
        "item_id": "P-4A7C",
        "a": 2,
        "b": 1,
        "modulus": 19,
        "domain_max": 8,
        "presentation": "narrative",
        "supporting_explanation": (
            "The unwrapped values rise by two from 1 through 17. Since the modulus "
            "is 19, no value reaches the wrap point, so each adjacent output "
            "preserves the order."
        ),
        "presentation_intent": "matched_true",
    },
    {
        "item_id": "P-6F30",
        "a": 7,
        "b": 3,
        "modulus": 23,
        "domain_max": 8,
        "presentation": "narrative",
        "supporting_explanation": (
            "The positive coefficient advances outputs by seven at every step. "
            "The bounded domain is shorter than the modulus, so modular reduction "
            "cannot reverse the adjacent order."
        ),
        "presentation_intent": "intended_high_disagreement_false",
    },
    {
        "item_id": "P-91D2",
        "a": 2,
        "b": 1,
        "modulus": 17,
        "domain_max": 8,
        "presentation": "narrative",
        "supporting_explanation": (
            "The unwrapped values rise by two from 1 through 17. Since inputs stop "
            "at 8, no value exceeds the modulus, so each adjacent output preserves "
            "the order."
        ),
        "presentation_intent": "intended_stable_false",
    },
]


def render_source(spec: dict[str, Any]) -> str:
    return (
        "def f(x):\n"
        f"    return ({spec['a']} * x + {spec['b']}) % {spec['modulus']}\n"
    )


def make_public_task(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "item_id": spec["item_id"],
        "data_class": "synthetic_prototype",
        "language": "python",
        "source": render_source(spec),
        "domain": f"integers x with 0 <= x <= {spec['domain_max']}",
        "claim": (
            "For every integer x with 0 <= x < "
            f"{spec['domain_max']}, f(x + 1) >= f(x)."
        ),
        "presentation": spec["presentation"],
        "supporting_explanation": spec["supporting_explanation"],
    }


def resolve_spec(spec: dict[str, Any]) -> dict[str, Any]:
    """Cross-check trusted rendered execution against a direct arithmetic oracle."""
    namespace: dict[str, Any] = {}
    trusted_source = render_source(spec)
    exec(compile(trusted_source, "<e003-generated>", "exec"), {"__builtins__": {}}, namespace)
    generated_function = namespace["f"]

    observed = []
    for x in range(spec["domain_max"] + 1):
        executed = generated_function(x)
        reference = (spec["a"] * x + spec["b"]) % spec["modulus"]
        if executed != reference:
            raise AssertionError(f"oracle disagreement for {spec['item_id']} at x={x}")
        observed.append(executed)

    counterexamples = []
    for x, (left, right) in enumerate(zip(observed, observed[1:])):
        if right < left:
            counterexamples.append({"x": x, "f_x": left, "f_x_plus_1": right})

    return {
        "item_id": spec["item_id"],
        "presentation_intent": spec["presentation_intent"],
        "truth_label": not counterexamples,
        "counterexamples": counterexamples,
        "parameters": {
            "a": spec["a"],
            "b": spec["b"],
            "modulus": spec["modulus"],
            "domain_max": spec["domain_max"],
        },
        "oracle": "trusted rendered execution cross-checked with direct arithmetic",
    }


def build_bundle() -> tuple[dict[str, Any], dict[str, Any]]:
    public = {
        "notice": "SYNTHETIC PROTOTYPE TASKS — NOT E003 SUBJECT DATA",
        "tasks": [make_public_task(spec) for spec in PROTOTYPE_SPECS],
    }
    oracle = {
        "notice": "PRIVATE SYNTHETIC ORACLE MANIFEST — KEEP FROM SUBJECTS",
        "items": [resolve_spec(spec) for spec in PROTOTYPE_SPECS],
    }
    return public, oracle


def assert_no_public_label_leakage(public: dict[str, Any]) -> None:
    forbidden_fragments = {
        "truth_label",
        "counterexample",
        "presentation_intent",
        "matched_true",
        "stable_false",
        "high_disagreement",
    }
    for task in public["tasks"]:
        if set(task) != PUBLIC_KEYS:
            raise AssertionError(f"unexpected public schema for {task.get('item_id')}")
        serialized = json.dumps(task, sort_keys=True).lower()
        leaked = sorted(fragment for fragment in forbidden_fragments if fragment in serialized)
        if leaked:
            raise AssertionError(f"public task {task['item_id']} leaks {leaked}")
        if "verdict" in task or "confidence" in task:
            raise AssertionError("subject response fields must not exist in fixtures")


def load_committed_bundle() -> tuple[dict[str, Any], dict[str, Any]]:
    return (
        json.loads(PUBLIC_PATH.read_text(encoding="utf-8")),
        json.loads(ORACLE_PATH.read_text(encoding="utf-8")),
    )
