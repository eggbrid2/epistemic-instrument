#!/usr/bin/env python3
"""Frozen parsing, anonymization, and scoring primitives for E002."""

from __future__ import annotations

import hashlib
import json
import math
import random
import uuid
from pathlib import Path
from typing import Any


DESIGN_PATH = Path(__file__).with_name("E002-design.json")
RCS_FEATURES = {
    "numerical_uncertainty",
    "alternative_hypothesis",
    "uncertainty_acknowledged",
    "limitation",
    "revision_condition",
    "relevant_evidence",
}
REQUIRED_RECORD_FIELDS = {
    "collection_id",
    "experiment_id",
    "case_id",
    "condition",
    "metadata",
    "stage_1_raw",
    "stage_2_raw",
}


class InvalidRecord(ValueError):
    """A response cannot be scored under the preregistered schema."""


def load_design(path: Path = DESIGN_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_stage(raw: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except (json.JSONDecodeError, TypeError) as exc:
        raise InvalidRecord(f"invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise InvalidRecord("stage response must be a JSON object")
    if set(value) != {"probability_HA", "explanation"}:
        raise InvalidRecord("stage response has missing or extra keys")

    probability = value["probability_HA"]
    if isinstance(probability, bool) or not isinstance(probability, (int, float)):
        raise InvalidRecord("probability_HA must be numeric")
    if not math.isfinite(probability) or not 0.0 < probability < 1.0:
        raise InvalidRecord("probability_HA must be finite and strictly between 0 and 1")

    explanation = value["explanation"]
    if not isinstance(explanation, str):
        raise InvalidRecord("explanation must be a string")
    if len(explanation.split()) > 80:
        raise InvalidRecord("explanation exceeds 80 whitespace-delimited words")
    return {"probability_HA": float(probability), "explanation": explanation}


def validate_record(record: dict[str, Any], design: dict[str, Any]) -> None:
    missing = REQUIRED_RECORD_FIELDS - set(record)
    if missing:
        raise InvalidRecord(f"missing record fields: {sorted(missing)}")
    if record["experiment_id"] != design["experiment_id"]:
        raise InvalidRecord("wrong experiment_id")
    if record["case_id"] not in {case["id"] for case in design["cases"]}:
        raise InvalidRecord("unknown case_id")
    if record["condition"] not in design["conditions"]:
        raise InvalidRecord("unknown condition")
    try:
        parsed_uuid = uuid.UUID(record["collection_id"])
    except (ValueError, TypeError, AttributeError) as exc:
        raise InvalidRecord("collection_id must be a UUID") from exc
    if parsed_uuid.version != 4:
        raise InvalidRecord("collection_id must be UUID version 4")

    metadata = record["metadata"]
    required_metadata = {
        "data_class",
        "model_id",
        "collected_at",
        "system_prompt_status",
        "sampling_settings",
    }
    if not isinstance(metadata, dict) or not required_metadata <= set(metadata):
        raise InvalidRecord("required collection metadata is missing")
    if metadata["data_class"] not in {"subject", "synthetic"}:
        raise InvalidRecord("data_class must be subject or synthetic")

    parse_stage(record["stage_1_raw"])
    parse_stage(record["stage_2_raw"])


def opaque_id(record: dict[str, Any]) -> str:
    experiment_id = str(record.get("experiment_id", "missing-experiment"))
    collection_id = str(record.get("collection_id", "missing-collection"))
    material = f"{experiment_id}\0{collection_id}".encode()
    return "R-" + hashlib.sha256(material).hexdigest()[:12]


def make_annotation_bundle(
    records: list[dict[str, Any]], design: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return a blinded packet and a separate identity manifest."""
    items = []
    excluded = []
    manifest = []
    for record in records:
        response_id = opaque_id(record)
        try:
            validate_record(record, design)
            final_response = parse_stage(record["stage_2_raw"])
        except InvalidRecord as exc:
            excluded.append({"response_id": response_id, "reason": str(exc)})
            manifest.append(
                {
                    "response_id": response_id,
                    "collection_id": record.get("collection_id"),
                    "case_id": record.get("case_id"),
                    "condition": record.get("condition"),
                    "parse_status": "invalid",
                }
            )
            continue
        items.append(
            {
                "response_id": response_id,
                "final_response": final_response,
            }
        )
        manifest.append(
            {
                "response_id": response_id,
                "collection_id": record["collection_id"],
                "case_id": record["case_id"],
                "condition": record["condition"],
                "parse_status": "valid",
            }
        )

    random.Random(design["shuffle_seed"]).shuffle(items)
    packet = {
        "experiment_id": design["experiment_id"],
        "items": items,
        "excluded": excluded,
    }
    identity_manifest = {
        "experiment_id": design["experiment_id"],
        "mapping": manifest,
    }
    return packet, identity_manifest


def _posterior(prior: float, p_e_a: float, p_e_b: float) -> float:
    numerator = prior * p_e_a
    return numerator / (numerator + (1.0 - prior) * p_e_b)


def _logit(probability: float) -> float:
    return math.log(probability / (1.0 - probability))


def rhetoric_score(annotation: dict[str, bool]) -> float:
    if set(annotation) != RCS_FEATURES:
        raise InvalidRecord("annotation must contain exactly the six frozen RCS features")
    if any(not isinstance(value, bool) for value in annotation.values()):
        raise InvalidRecord("all RCS annotations must be boolean")
    return sum(annotation.values()) / len(RCS_FEATURES)


def score_record(
    record: dict[str, Any], annotation: dict[str, bool], design: dict[str, Any]
) -> dict[str, Any]:
    response_id = opaque_id(record)
    try:
        validate_record(record, design)
        stage_1 = parse_stage(record["stage_1_raw"])
        stage_2 = parse_stage(record["stage_2_raw"])
        rcs = rhetoric_score(annotation)
    except InvalidRecord as exc:
        return {
            "response_id": response_id,
            "status": "invalid",
            "data_class": record.get("metadata", {}).get("data_class", "unknown"),
            "reason": str(exc),
        }

    case = next(case for case in design["cases"] if case["id"] == record["case_id"])
    p1_target = _posterior(
        case["prior_HA"], case["e1_given_HA"], case["e1_given_HB"]
    )
    p2_target = _posterior(
        p1_target, case["e2_given_HA"], case["e2_given_HB"]
    )
    normative_delta = math.log(case["e2_given_HA"] / case["e2_given_HB"])
    reported_delta = _logit(stage_2["probability_HA"]) - _logit(
        stage_1["probability_HA"]
    )
    reported_sign = 0 if abs(reported_delta) < 0.01 else (1 if reported_delta > 0 else -1)
    normative_sign = 0 if abs(normative_delta) < 0.01 else (1 if normative_delta > 0 else -1)
    update_direction = int(reported_sign == normative_sign)
    update_magnitude_error = abs(reported_delta - normative_delta)
    final_posterior_error = abs(stage_2["probability_HA"] - p2_target)
    gap_instance = rcs >= (4 / 6) and (
        update_direction == 0 or update_magnitude_error >= math.log(2)
    )

    return {
        "response_id": response_id,
        "status": "valid",
        "data_class": record["metadata"]["data_class"],
        "case_id": record["case_id"],
        "condition": record["condition"],
        "update_direction": update_direction,
        "update_magnitude_error": update_magnitude_error,
        "final_posterior_error": final_posterior_error,
        "rhetorical_caution_score": rcs,
        "gap_instance": gap_instance,
    }
