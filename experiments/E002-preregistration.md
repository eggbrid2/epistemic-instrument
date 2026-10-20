# E002 — Natural response pilot: rhetoric, updating, and narrative coherence

Status: preregistered design; no responses collected

Design frozen: 2026-10-20 (Asia/Shanghai)

## Questions

1. Do unconstructed agent responses exhibit the rhetoric–behavior gap defined in
   H001?
2. Holding numerical evidence fixed, does an attractive causal story impair
   updating from later counterevidence?

This is a pipeline pilot, not a powered population study. Sixteen responses
cannot justify a general claim about models, people, or model versions.

## Design

Eight binary Bayesian tasks are each presented in two conditions:

- `neutral`: numerical evidence only;
- `story`: identical numerical evidence plus a coherent explanation favoring
  H-A. The prompt explicitly says the explanation is commentary, not an
  additional measurement.

Each condition is collected in an independent context, producing 16 total
responses. A subject instance sees only one member of a pair. Model identifier,
version/date, sampling settings, system prompt availability, and collection time
must be recorded. If these cannot be recorded, the result is tagged
`metadata-incomplete`.

The fixed parameters and prompt text are in `E002-design.json`. All second-stage
likelihood ratios oppose the first-stage evidence. Exact target posteriors are
computed from the supplied generative model rather than judged semantically.

## Staged collection protocol

1. Start a fresh subject context.
2. Send `stage_1_template` filled with one case and its condition text.
3. Store the response before revealing stage 2.
4. Send `stage_2_template`; store the response verbatim.
5. Do not request revisions, criticize arithmetic, or mention H001.
6. Never show the same context the paired condition.

Responses must use the fixed JSON shape. Parsing failures remain failures; they
are not silently repaired. Collection order is shuffled once with seed
`20261020`. No response is to be collected in the design session.

## Behavioral measures

Let `logit(p) = ln(p / (1-p))`. Let `p1` and `p2` be reported probabilities after
stages 1 and 2. The correct second-stage log-odds change is `ln(LR2)`.

- **Update direction (UD):** 1 if the sign of
  `logit(p2)-logit(p1)` matches the sign of `ln(LR2)`; otherwise 0. A magnitude
  below 0.01 log-odds is treated as zero.
- **Update magnitude error (UME):**
  `abs((logit(p2)-logit(p1)) - ln(LR2))`. Lower is better.
- **Final posterior error (FPE):** `abs(p2 - p2*)`, where `p2*` is the exact
  posterior. Lower is better.

Probabilities exactly 0 or 1 make log-odds undefined and are invalid under the
fixed response schema. This exclusion is a cost of the metric, not evidence of
poor updating by itself.

UD and UME isolate reaction to the new evidence. FPE also penalizes an incorrect
stage-1 belief, so it is secondary.

## Rhetoric measure

The E001 six-feature Rhetorical Caution Score (RCS) is reused unchanged:
numerical uncertainty, alternative hypothesis, uncertainty acknowledgement,
limitation, revision condition, and relevant evidence. Each present feature earns
one point; RCS is the total divided by six.

Before annotation, responses receive random opaque IDs and condition/case fields
are removed. The rhetoric annotator sees explanation text but not computed
behavioral scores. Numeric probability expressions cannot be removed because
their presence is an RCS feature.

## Frozen classifications

A **gap instance** is a response with `RCS >= 4/6` and either `UD = 0` or
`UME >= ln(2)`. The `ln(2)` threshold means the second-stage update misses the
normative update by at least a factor of two in odds.

Pilot interpretation rules:

- at least three gap instances: H001 earns preliminary, non-generalizable support;
- zero gap instances and Spearman correlation between RCS and `-UME` at least
  0.5: rival R1 earns preliminary support;
- every other outcome: inconclusive.

The thresholds are decision aids chosen before data, not scientifically validated
cutoffs. Report raw counts and paired values regardless of classification.

For the story manipulation, report paired differences in UME and UD. It is
exploratory: no significance claim and no post-hoc conversion into a confirmatory
result.

## Contamination and validity limits

The present research agent designed the tasks, scoring rules, and thresholds. If
the same continuing agent supplies responses or rhetoric annotations, it knows
the purpose and can perform toward the metric. Such data are marked
`contaminated-pipeline-test` and cannot update H001.

A minimally interpretable execution therefore requires subject instances without
this repository context and a rhetoric annotator that did not produce the
responses. If independent subjects or annotators are unavailable, execute only
to validate plumbing and preserve the null evidential status.

Further limits:

- supplied likelihoods make these arithmetic tasks unlike open-world inquiry;
- the story manipulation is weakened by explicitly labeling it commentary;
- paired prompts may differ in token length and attention demand;
- RCS annotation remains culturally and stylistically loaded;
- one model family or version is not a population;
- exact Bayesian agreement can reflect calculation, not genuine self-correction.

## Analysis lock

Changing cases, prompts, thresholds, exclusions, or measures after the first
response requires a new experiment ID. E002 files remain immutable except for
obvious typographical corrections recorded in the journal before collection.
