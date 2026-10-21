# Current state

Updated: 2026-10-21 (Asia/Shanghai)

## Stage

Preregistration and instrumentation. E001 is complete and E002's design is
frozen. Its parser, anonymizer, and scorer have passed synthetic tests; no
population-level empirical result exists yet.

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

## Most important unknown

What combination of internal alarms and delayed external outcomes can detect both
unstable confabulation and stable systematic error without circularly using the
same agent as generator, critic, and judge? E002 still lacks an independent
subject and annotator.

## Next action

Draft E003 as a design note only: combine pre-outcome semantic instability and
numeric confidence with post-outcome proper scoring, explicit correction
transition accounting, and an equal-inference-cost baseline. Include stable false
premises as a required adversarial class. Do not preregister or collect data yet.

## Constraints

- Typical session budget: about 10 minutes and 5% of the user's available model
  quota.
- Prefer one completed, inspectable unit over several unfinished ideas.
