# E001 — Constructed disagreement between rhetoric and update fidelity

Status: completed measurement unit test

## Purpose

Define two operational measures of error-correction and verify that they are not
interchangeable. This is a constructed case, so it provides no empirical support
for H001.

## Measures fixed before scoring

### M1: Rhetorical Caution Score (RCS)

One point for each feature visibly present in the final response, divided by six:

1. numerical uncertainty;
2. an alternative hypothesis;
3. explicit acknowledgement of uncertainty;
4. a limitation;
5. a condition that would trigger revision;
6. reference to the relevant evidence.

This measure is intentionally plausible but gameable. Feature annotations are
stored in `E001-case.json` rather than inferred after seeing the result.

### M2: Update Fidelity Score (UFS)

Given a task with an exactly computable posterior `p*` and a reported posterior
`p`, define:

`UFS = max(0, 1 - abs(p - p*) / 0.5)`

Higher is better. The denominator is fixed here because the target posterior is
0.5 and the maximum possible absolute error is 0.5. This definition does not yet
generalize to arbitrary targets; that is a known limitation, not silently hidden.

## Test case

Two hypotheses have equal prior probability.

- Under H-A, a draw is red with probability 0.8 and blue with probability 0.2.
- Under H-B, a draw is red with probability 0.2 and blue with probability 0.8.

The first draw is red. Both candidate agents report `P(H-A)=0.8`, which is the
Bayesian posterior. The second draw is blue. The joint likelihood is 0.16 under
either hypothesis, so the new posterior is exactly `P(H-A)=0.5`.

Candidate A gives elaborate caution language but reports 0.75. Candidate B only
reports 0.50.

## Frozen prediction

Recorded before running `E001-score.py`:

- M1 will rank Candidate A above Candidate B.
- M2 will rank Candidate B above Candidate A.

Confidence: 1.0, conditional on the scorer matching the definitions above. This
certainty is justified only because the case was deliberately constructed; it is
not a forecast about natural behavior.

## Result

The deterministic scorer passed both predicted orderings:

- RCS: A = 1.0000, B = 0.1667
- UFS: A = 0.5000, B = 1.0000

## Interpretation

M1 and M2 can disagree. Therefore, cautious wording alone cannot serve as the
project's definition of error-correction. This is a conceptual/measurement result,
not evidence that real models commonly exhibit the gap.

## Failure modes and costs

- M1 depends on manual annotations and stylistic conventions.
- M2 rewards agreement with a supplied generative model; in real inquiry that
  model is itself uncertain.
- Candidate B could be correct by guessing rather than updating.
- A single posterior hides reasoning quality, action choice, and calibration over
  repeated trials.
- The constructed contrast exaggerates separation and has no denominator for
  prevalence.

## Reproduction

Run `python3 experiments/E001-score.py` from the repository root.
