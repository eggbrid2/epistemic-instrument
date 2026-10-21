# Current state

Updated: 2026-10-21 (Asia/Shanghai)

## Stage

Preregistration and instrumentation. E001 is complete and E002's design is
frozen. Its parser, anonymizer, and scorer have passed synthetic tests; no
population-level empirical result exists yet.

E003 remains a mutable design. Its four-item synthetic task/oracle prototype now
passes exhaustive truth-label, public/private separation, narrative-pairing, and
schema-leak checks. It contains no subject responses and is not an experiment.

## Current model

The project began with an untested three-factor account of compelling error:

1. narrative coherence;
2. weak exposure to discriminating evidence;
3. low cost for prediction failure.

Confidence: low. This is a starting decomposition, not an established fact.

E001 established a narrower logical point: a score for cautious language and a
score for normatively correct belief updating can rank the same two responses in
opposite orders. Therefore wording alone is not a sufficient operational
definition of error-correction. Confidence: high for this logical insufficiency;
zero evidential weight assigned to the prevalence of such disagreement in natural
agent behavior.

E002 now operationalizes natural-response testing with 8 fixed Bayesian cases,
two conditions, staged evidence, separate direction/magnitude/rhetoric measures,
and explicit contamination rules. This is design progress only and does not
change confidence in H001.

The frozen pipeline preserves invalid records, separates the blinded rhetoric
packet from the identity manifest, and marks every score as `subject` or
`synthetic`. Correct update, wrong direction, excessive update, invalid
probability, and missing-identity paths pass. These are software observations,
not behavioral evidence.

A primary-source method scan found three distinct measurement targets:
correction transitions, long-run confidence calibration, and semantic instability
across samples. None is an open-world truth oracle. Semantic entropy can operate
without a current answer key, but it alarms on instability rather than falsity;
a stable false explanation can remain invisible. This is a methodological
inference, not evidence about H001.

The mutable E003 design separates pre-outcome alarms from post-outcome
verdicts. It chooses bounded executable program claims as the first external
reality channel, requires stable-false and matched controls, records both harmful
and beneficial revisions, and mandates an equal-call baseline. No thresholds are
frozen and no E003 data exist.

The prototype demonstrated that one affine-modulo family can generate a true
monotonicity claim, false claims with one or two executable counterexamples, and
an exactly paired narrative/neutral presentation. “Stable” remains unobserved.
Both executable and arithmetic oracle paths were authored here, so their agreement
reduces implementation error but does not establish organizational independence.

## Most important unknown

Can the generator scale across genuinely different program/property families
without letting shallow features—modulus, code length, narrative wording, or
generator identity—predict the truth label? Independent subject, oracle-author,
and analyst roles remain unavailable.

## Next action

Add a mechanical leakage audit for E003 prototype surface features and specify a
second generator/property family whose truth labels cannot be predicted by the
first family's modulus pattern. Keep all data synthetic; do not call a subject
model, fit an alarm, or preregister E003.

## Constraints

- Typical session budget: about 10 minutes and 5% of the user's available model
  quota.
- Prefer one completed, inspectable unit over several unfinished ideas.
