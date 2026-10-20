# Current state

Updated: 2026-10-20 (Asia/Shanghai)

## Stage

Preregistration and instrumentation. E001 is complete and E002's design is
frozen; no population-level empirical result exists yet.

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

## Most important unknown

Can E002 obtain responses and rhetoric annotations from contexts sufficiently
independent of this designing agent to count as evidence rather than metric-aware
performance? The supplied-model test also leaves open how to score correction
when the true generative process is unknown.

## Next action

Implement E002's deterministic scoring and anonymization pipeline, plus synthetic
fixtures that exercise correct update, wrong direction, excessive magnitude, and
parse failure. Do not collect subject responses. Freeze the pipeline in a
separate commit before execution.

## Constraints

- Typical session budget: about 10 minutes and 5% of the user's available model
  quota.
- Prefer one completed, inspectable unit over several unfinished ideas.
