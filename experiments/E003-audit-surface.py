#!/usr/bin/env python3
"""Describe shallow truth-label leakage in E003's synthetic prototype.

This is a construction audit, not an alarm model. It intentionally uses the
private oracle and must never be run on subject-visible packets.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Any, Callable

from e003_taskgen import load_committed_bundle


Feature = tuple[str, str, Callable[[dict[str, Any], dict[str, Any]], Any]]

FEATURES: tuple[Feature, ...] = (
    ("presentation", "categorical", lambda public, oracle: public["presentation"]),
    ("family", "categorical", lambda public, oracle: oracle["family"]),
    ("source_chars", "numeric", lambda public, oracle: len(public["source"])),
    ("source_lines", "numeric", lambda public, oracle: len(public["source"].splitlines())),
    ("domain_chars", "numeric", lambda public, oracle: len(public["domain"])),
    ("claim_chars", "numeric", lambda public, oracle: len(public["claim"])),
    (
        "explanation_words",
        "numeric",
        lambda public, oracle: len((public["supporting_explanation"] or "").split()),
    ),
    (
        "source_numerals",
        "numeric",
        lambda public, oracle: len(re.findall(r"\d+", public["source"])),
    ),
)


def accuracy(predictions: list[bool], labels: list[bool]) -> float:
    return sum(predicted == actual for predicted, actual in zip(predictions, labels)) / len(labels)


def balanced_accuracy(predictions: list[bool], labels: list[bool]) -> float:
    recalls = []
    for label in (False, True):
        indices = [index for index, actual in enumerate(labels) if actual is label]
        recalls.append(sum(predictions[index] is label for index in indices) / len(indices))
    return sum(recalls) / 2


def best_categorical_rule(values: list[Any], labels: list[bool]) -> tuple[list[bool], str]:
    counts: dict[Any, Counter[bool]] = defaultdict(Counter)
    for value, label in zip(values, labels):
        counts[value][label] += 1
    mapping = {
        value: count.most_common(1)[0][0]
        for value, count in counts.items()
    }
    predictions = [mapping[value] for value in values]
    rendered = ", ".join(f"{value!r}->{mapping[value]}" for value in sorted(mapping, key=str))
    return predictions, rendered


def best_numeric_stump(values: list[int], labels: list[bool]) -> tuple[list[bool], str]:
    unique = sorted(set(values))
    thresholds = [(left + right) / 2 for left, right in zip(unique, unique[1:])]
    candidates: list[tuple[float, float, list[bool], str]] = []
    for threshold in thresholds:
        for low_prediction in (False, True):
            predictions = [low_prediction if value <= threshold else not low_prediction for value in values]
            candidates.append(
                (
                    accuracy(predictions, labels),
                    balanced_accuracy(predictions, labels),
                    predictions,
                    f"value <= {threshold:g} -> {low_prediction}",
                )
            )
    for constant in (False, True):
        predictions = [constant] * len(labels)
        candidates.append(
            (
                accuracy(predictions, labels),
                balanced_accuracy(predictions, labels),
                predictions,
                f"constant -> {constant}",
            )
        )
    _, _, predictions, rule = max(candidates, key=lambda candidate: (candidate[0], candidate[1]))
    return predictions, rule


def main() -> None:
    public, oracle = load_committed_bundle()
    public_by_id = {item["item_id"]: item for item in public["tasks"]}
    rows = [(public_by_id[item["item_id"]], item) for item in oracle["items"]]
    labels = [item["truth_label"] for _, item in rows]
    majority = Counter(labels).most_common(1)[0][0]
    baseline = [majority] * len(labels)

    print(f"items={len(labels)} true={sum(labels)} false={len(labels) - sum(labels)}")
    print(
        f"majority={majority} accuracy={accuracy(baseline, labels):.3f} "
        f"balanced_accuracy={balanced_accuracy(baseline, labels):.3f}"
    )
    print("feature\taccuracy\tbalanced_accuracy\trule")
    for name, kind, extractor in FEATURES:
        values = [extractor(public_item, oracle_item) for public_item, oracle_item in rows]
        if kind == "categorical":
            predictions, rule = best_categorical_rule(values, labels)
        else:
            predictions, rule = best_numeric_stump(values, labels)
        print(
            f"{name}\t{accuracy(predictions, labels):.3f}\t"
            f"{balanced_accuracy(predictions, labels):.3f}\t{rule}"
        )

    print("\nitem_id\tlabel\tpresentation\tfamily\tsource_chars\texplanation_words")
    for public_item, oracle_item in rows:
        explanation_words = len((public_item["supporting_explanation"] or "").split())
        print(
            f"{public_item['item_id']}\t{oracle_item['truth_label']}\t"
            f"{public_item['presentation']}\t{oracle_item['family']}\t"
            f"{len(public_item['source'])}\t{explanation_words}"
        )


if __name__ == "__main__":
    main()
