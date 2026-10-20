# Research charter

## Core question

How can an intelligent agent detect that a coherent, appealing explanation is
false or seriously incomplete?

## Working thesis

The dangerous property is not simply "bias." It is the combination of narrative
coherence, weak contact with discriminating evidence, and insufficient penalties
for failed predictions. This is a hypothesis, not a conclusion.

## Candidate outputs

- a compact diagnostic protocol;
- a benchmark made of deceptive-but-plausible explanations;
- a prediction and calibration ledger;
- experiments comparing debiasing interventions;
- a tool that makes contradiction and model drift visible.

## Success criteria

The project succeeds only if at least one method performs better than a clearly
specified baseline on unseen cases, or if the investigation produces a strong
negative result that rules out a plausible method.

## Known hazards

- optimizing measurable proxies instead of truth-seeking;
- hindsight bias when scoring predictions;
- selecting only convenient or entertaining cases;
- mistaking contrarianism for correction;
- collecting anecdotes without a denominator;
- allowing the evaluator and evaluated model to share the same blind spots;
- turning uncertainty labels into performative precision;
- losing reproducibility through private or encrypted records.
