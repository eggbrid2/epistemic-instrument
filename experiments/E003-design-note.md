# E003 design note — Alarm is not a verdict

Status: mutable design sketch; not preregistered; no data collected

Created: 2026-10-21 (Asia/Shanghai)

## Question

Can a pre-outcome instrument combining numeric confidence, independent-sample
instability, and challenge response identify wrong explanations better than any
single signal—especially when the wrong explanation is stable and coherent?

This question contains two different jobs that must not be collapsed:

1. **Alarm:** decide whether to escalate a claim before its truth is known.
2. **Verdict:** determine whether the claim is actually correct after contact with
   an independent outcome channel.

E003 will evaluate alarms. It will not call an alarm a truth detector.

## Chosen bridge domain

The first E003 iteration should use bounded executable programs rather than live
world forecasts.

Each item contains source code, a bounded input domain, a behavioral claim, and a
coherent explanation supporting that claim. The subject judges whether the claim
is true. After all subject outputs are frozen, exhaustive execution over the
domain supplies the external label.

Preferred claim form:

> For every input in domain D, function F satisfies property P.

False items contain at least one executable counterexample. True items pass an
independently implemented exhaustive oracle.

Why choose this domain first:

- outcomes are unambiguous and immediately reproducible;
- the subject can inspect evidence but cannot replace the execution oracle;
- stable false explanations can be constructed around rare edge cases;
- delayed real-world outcomes introduce source choice, ambiguity, and waiting
  costs before the measurement pipeline itself is known to work.

Cost: this is a controlled micro-world, not evidence that the instrument works on
politics, medicine, science, or personal decisions. A future experiment must test
a genuinely prospective outcome channel under a new ID.

## Required item classes

Items are paired by code, domain size, explanation length, and apparent
difficulty.

1. **Stable-true control:** correct claim with a coherent supporting explanation.
2. **Stable-false narrative:** false claim with a coherent explanation that
   overlooks a rare but deterministic counterexample.
3. **Unstable-false control:** false claim with several salient contradictions,
   expected to produce disagreement across samples.
4. **Neutral presentation control:** the same claim without the supporting
   narrative, used to estimate narrative influence.

“Stable” is a prediction about response distribution, not a property assigned
after seeing results. The eventual preregistration must define it using a
development set and then hold thresholds fixed.

## Subject protocol

All subject calls require fresh contexts with no repository access. The same
instance may not see a paired item.

### Stage 0 — initial judgment

Return:

- binary verdict: `TRUE` or `FALSE`;
- numeric confidence that the verdict is correct, strictly between 0 and 1;
- explanation with a fixed word cap;
- one observation that would falsify the verdict.

### Stage 1 — independent samples

Collect `K` fresh-context verdicts at fixed sampling settings. Do not expose any
sample to another subject instance. For a binary claim, verdict entropy is a
transparent special case of discrete semantic-cluster entropy; explanation-level
clustering is secondary and must not silently replace verdict entropy.

### Stage 2 — challenge without new evidence

Show the Stage 0 response a fixed neutral instruction to search for a decisive
counterexample, then obtain a revised verdict and confidence. The challenge adds
no facts.

A flip is **challenge fragility**, not correction. Without the oracle label it is
impossible to know whether the change repairs or damages the answer.

### Stage 3 — external resolution

Freeze all responses, then execute the independent exhaustive oracle. Preserve
the full counterexample for false claims and complete test evidence for true
claims. Oracle failures make the item unresolved; they are not guessed or
manually repaired after outcome inspection.

## Pre-outcome alarm signals

- `q0`: Stage 0 confidence that its own verdict is correct.
- `H_vote`: entropy of independent binary verdicts.
- `flip`: whether the challenge changes the verdict.
- `delta_q`: absolute and signed confidence change under challenge.
- optional `H_explanation`: entropy over explanation meanings, scored separately
  because entailment clustering adds another model and error surface.

The combined alarm rule is deliberately unspecified in this design note. It must
be selected on development generator families and frozen before evaluation on
held-out families. Fitting and evaluating on random items from the same generator
would exaggerate generalization.

## Post-outcome measures

### Alarm quality

- Brier score for `q0` and revised confidence;
- AUROC and AUPRC for detecting an incorrect verdict;
- selective risk at fixed coverage levels;
- false-negative rate specifically on the stable-false class;
- performance by held-out generator family, not only pooled performance.

### Correction accounting

Report all four transitions:

- incorrect → correct;
- correct → incorrect;
- incorrect → incorrect;
- correct → correct.

Net accuracy change is secondary. A method that repairs five answers and damages
five others has not demonstrated reliable correction.

### Narrative effect

For paired narrative/neutral items, report differences in initial error,
confidence, entropy, and transition category. Do not infer causality if pairing or
presentation order is broken.

## Equal-inference-cost baseline

The candidate procedure consumes one initial call, `K` independent samples, and a
challenge/revision call. Its primary baseline receives the same number of calls
and approximately the same token budget but uses all calls for independent
sampling followed by majority vote and vote-share confidence—no critique prompt.

Additional baselines:

- constant confidence based on development-set accuracy;
- generator-family difficulty estimate that ignores the subject's response;
- Stage 0 confidence alone;
- verdict entropy alone.

The combined instrument must improve held-out triage over these baselines, not
merely correlate with item difficulty.

## Independence requirements

Four roles must be separated where possible:

1. task/narrative constructor;
2. subject producing judgments;
3. oracle implementation and execution;
4. analyst choosing no post-outcome thresholds.

Data from this continuing agent in any subject role is labeled contaminated and
cannot update project hypotheses. A second language model is not automatically an
independent judge if it shares training data, prompts, or failure modes.

## Failure modes that could invalidate E003

- **Mutation artifacts:** false programs or narratives contain stylistic clues.
- **Oracle bugs:** the alleged reality channel encodes the same mistaken
  assumption as the claim generator.
- **Difficulty leakage:** stable-false items are simply harder than controls.
- **Correlated samples:** fresh calls repeat one training-induced misconception,
  producing misleadingly low entropy.
- **Prompt suggestibility:** challenge flips measure compliance rather than error
  recognition.
- **Narrative imbalance:** additional text consumes attention or context, so the
  effect is not coherence specifically.
- **Threshold overfitting:** alarm weights are tuned on evaluation families.
- **Role contamination:** constructor knowledge reaches subjects or annotators.
- **Scope inflation:** success on bounded programs is described as open-world
  truth detection.

## Minimum success criterion candidate

Not yet frozen. A defensible criterion will require all of the following on
held-out generator families:

- combined alarm improves selective risk over equal-cost majority sampling;
- stable-false false-negative rate is lower than entropy-only triage;
- confidence adds information beyond generator-family difficulty;
- correction produces more incorrect-to-correct than correct-to-incorrect
  transitions;
- results survive removal of explanation-level semantic scoring.

If any criterion is adopted, its numerical threshold and sample size must be set
before subject collection. This note authorizes no data collection.

## Next design problem

Create a tiny task-generator/oracle prototype with no subject calls. It should
produce matched true, intended-stable-false, intended-unstable-false, and neutral
variants, and prove truth labels by exhaustive execution. “Stable” remains an
untested prediction until independent samples exist. The prototype is
infrastructure, not E003 data.
