# H001 — Rhetoric–behavior gap

Status: live, untested

## Claim

Language that displays uncertainty is a weak proxy for genuine error-correction.
When diagnostic counterevidence arrives, some agents will produce strong
epistemic rhetoric while changing their quantitative belief less appropriately
than agents using terse language.

This claim concerns a possible population-level regularity. The constructed case
in E001 cannot establish it.

## Rival hypotheses

- **R1 — alignment:** explicit uncertainty language usually accompanies better
  belief revision because both arise from the same internal monitoring process.
- **R2 — prompt artifact:** any gap is caused by response-format instructions,
  not a stable property of the agent.
- **R3 — annotation artifact:** human or model raters reward particular phrases,
  making the rhetoric score invalid before behavior is even compared.

## Falsification condition

On a preregistered, unseen set of sequential-evidence tasks, a fixed rhetoric
score must fail to predict update fidelity after controlling for task difficulty,
or predict it materially less well than a behavioral baseline. H001 should be
retired if rhetoric reliably predicts update fidelity out of sample and the
effect survives prompt and rater perturbations.

## Current evidence

None. E001 is a measurement unit test, not evidence about real agents.
