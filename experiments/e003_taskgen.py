#!/usr/bin/env python3
"""Synthetic task generator and exhaustive oracle for E003 design work."""

from __future__ import annotations

import itertools
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
        "family": "affine_mod_nondecreasing",
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
        "family": "affine_mod_nondecreasing",
        "a": 2,
        "b": 1,
        "modulus": 19,
        "domain_max": 8,
        "presentation": "narrative",
        "supporting_explanation": (
            "Unwrapped values rise by two from 1 through 17. Because the modulus "
            "is 19, no value reaches the wrap point, preserving adjacent output "
            "order."
        ),
        "presentation_intent": "matched_true",
    },
    {
        "item_id": "P-6F30",
        "family": "affine_mod_nondecreasing",
        "a": 7,
        "b": 3,
        "modulus": 23,
        "domain_max": 8,
        "presentation": "narrative",
        "supporting_explanation": (
            "A positive coefficient advances outputs by seven each step. The "
            "bounded domain is shorter than the modulus, so modular reduction "
            "cannot reverse adjacent order."
        ),
        "presentation_intent": "intended_high_disagreement_false",
    },
    {
        "item_id": "P-91D2",
        "family": "affine_mod_nondecreasing",
        "a": 2,
        "b": 1,
        "modulus": 17,
        "domain_max": 8,
        "presentation": "narrative",
        "supporting_explanation": (
            "Unwrapped values rise by two from 1 through 17. Because inputs stop "
            "at 8, no value exceeds the modulus, preserving adjacent output order "
            "throughout."
        ),
        "presentation_intent": "intended_stable_false",
    },
    {
        "item_id": "P-2B5D",
        "family": "rotate_boundary_weight",
        "length": 5,
        "trigger_bit": 1,
        "replacement_bit": 1,
        "presentation": "narrative",
        "supporting_explanation": (
            "Rotation preserves every bit. At the all-one boundary, writing one "
            "into the first position leaves the total number of one bits unchanged "
            "as expected."
        ),
        "presentation_intent": "matched_true",
    },
    {
        "item_id": "P-A104",
        "family": "rotate_boundary_weight",
        "length": 5,
        "trigger_bit": 1,
        "replacement_bit": 0,
        "presentation": "narrative",
        "supporting_explanation": (
            "Rotation preserves every bit. At the all-one boundary, normalizing "
            "the first position changes only representation and leaves the total "
            "number of one bits unchanged."
        ),
        "presentation_intent": "intended_stable_false",
    },
    {
        "item_id": "P-7D33",
        "family": "rotate_boundary_weight",
        "length": 5,
        "trigger_bit": 0,
        "replacement_bit": 0,
        "presentation": "neutral",
        "supporting_explanation": None,
        "presentation_intent": "neutral_true",
    },
    {
        "item_id": "P-E6A9",
        "family": "rotate_boundary_weight",
        "length": 5,
        "trigger_bit": 0,
        "replacement_bit": 1,
        "presentation": "neutral",
        "supporting_explanation": None,
        "presentation_intent": "neutral_false",
    },
]


def render_source(spec: dict[str, Any]) -> str:
    if spec["family"] == "affine_mod_nondecreasing":
        return (
            "def f(x):\n"
            f"    return ({spec['a']} * x + {spec['b']}) % {spec['modulus']}\n"
        )
    if spec["family"] == "rotate_boundary_weight":
        trigger = ", ".join([str(spec["trigger_bit"])] * spec["length"])
        return (
            "def f(bits):\n"
            "    out = bits[1:] + bits[:1]\n"
            f"    if bits == [{trigger}]:\n"
            f"        out[0] = {spec['replacement_bit']}\n"
            "    return out\n"
        )
    raise ValueError(f"unknown family: {spec['family']}")


def make_public_task(spec: dict[str, Any]) -> dict[str, Any]:
    if spec["family"] == "affine_mod_nondecreasing":
        domain = f"integers x with 0 <= x <= {spec['domain_max']}"
        claim = (
            "For every integer x with 0 <= x < "
            f"{spec['domain_max']}, f(x + 1) >= f(x)."
        )
    elif spec["family"] == "rotate_boundary_weight":
        domain = f"all binary lists bits of length {spec['length']}"
        claim = (
            f"For every binary list bits of length {spec['length']}, "
            "sum(f(bits)) == sum(bits)."
        )
    else:
        raise ValueError(f"unknown family: {spec['family']}")
    return {
        "item_id": spec["item_id"],
        "data_class": "synthetic_prototype",
        "language": "python",
        "source": render_source(spec),
        "domain": domain,
        "claim": claim,
        "presentation": spec["presentation"],
        "supporting_explanation": spec["supporting_explanation"],
    }


def _load_generated_function(spec: dict[str, Any]):
    namespace: dict[str, Any] = {}
    trusted_source = render_source(spec)
    exec(compile(trusted_source, "<e003-generated>", "exec"), {"__builtins__": {}}, namespace)
    return namespace["f"]


def _resolve_affine(spec: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    generated_function = _load_generated_function(spec)
    observed = []
    for x in range(spec["domain_max"] + 1):
        executed = generated_function(x)
        reference = (spec["a"] * x + spec["b"]) % spec["modulus"]
        if executed != reference:
            raise AssertionError(f"oracle disagreement for {spec['item_id']} at x={x}")
        observed.append(executed)
    counterexamples = [
        {"x": x, "f_x": left, "f_x_plus_1": right}
        for x, (left, right) in enumerate(zip(observed, observed[1:]))
        if right < left
    ]
    return counterexamples, "rendered execution cross-checked with direct arithmetic"


def _resolve_rotation(spec: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    generated_function = _load_generated_function(spec)
    counterexamples = []
    for values in itertools.product((0, 1), repeat=spec["length"]):
        bits = list(values)
        executed = generated_function(bits.copy())
        reference = bits[1:] + bits[:1]
        if bits == [spec["trigger_bit"]] * spec["length"]:
            reference[0] = spec["replacement_bit"]
        if executed != reference:
            raise AssertionError(f"oracle disagreement for {spec['item_id']} at bits={bits}")
        if sum(executed) != sum(bits):
            counterexamples.append(
                {
                    "bits": bits,
                    "f_bits": executed,
                    "sum_bits": sum(bits),
                    "sum_f_bits": sum(executed),
                }
            )
    return counterexamples, "rendered execution cross-checked with list transformation"


def resolve_spec(spec: dict[str, Any]) -> dict[str, Any]:
    if spec["family"] == "affine_mod_nondecreasing":
        counterexamples, oracle = _resolve_affine(spec)
        parameter_keys = ("a", "b", "modulus", "domain_max")
    elif spec["family"] == "rotate_boundary_weight":
        counterexamples, oracle = _resolve_rotation(spec)
        parameter_keys = ("length", "trigger_bit", "replacement_bit")
    else:
        raise ValueError(f"unknown family: {spec['family']}")
    return {
        "item_id": spec["item_id"],
        "family": spec["family"],
        "presentation_intent": spec["presentation_intent"],
        "truth_label": not counterexamples,
        "counterexamples": counterexamples,
        "parameters": {key: spec[key] for key in parameter_keys},
        "oracle": oracle,
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
        "observed_stability",
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
