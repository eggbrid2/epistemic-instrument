# Primary-method scan: self-correction and uncertainty without a known generator

Accessed: 2026-10-21 (Asia/Shanghai)

Scope: methods, controls, and failure modes. Claims below describe the cited
experiments; they are not evidence for this project's H001.

## 1. Huang et al. — intrinsic self-correction

Primary source: Jie Huang et al., *Large Language Models Cannot Self-Correct
Reasoning Yet*, ICLR 2024. [arXiv:2310.01798](https://arxiv.org/abs/2310.01798)

### Design extracted

- Defines intrinsic correction as revision without human, tool, or oracle
  correctness feedback.
- Uses staged trials: initial answer, model-generated critique/feedback, revised
  answer.
- Evaluates on labeled reasoning benchmarks including GSM8K, CommonSenseQA, and
  HotpotQA.
- Separates transitions into no change, incorrect-to-correct,
  correct-to-incorrect, and incorrect-to-incorrect instead of reporting only
  final accuracy.
- Compares correction/debate with self-consistency at an equivalent number of
  model responses, exposing inference-cost confounding.
- Tests whether putting the informative correction instruction directly into the
  initial prompt removes apparent gains, exposing weak-initial-prompt confounding.
- Contrasts intrinsic trials with oracle-gated correction to identify where
  correctness labels are doing the work.

### Transferable method

Any claimed correction benefit should report both directions of change, compare
against an equal-call sampling baseline, and control for information added by the
revision prompt. “Accuracy after revision” alone is insufficient.

### Limits for this project

Benchmark answer keys still provide the final truth anchor. The design evaluates
whether correction works, not whether an agent can discover an unknown real-world
truth with no later adjudication. Results from named model versions also should
not be assumed to describe current systems.

## 2. Kadavath et al. — P(True), P(IK), and multiple samples

Primary source: Saurav Kadavath et al., *Language Models (Mostly) Know What They
Know*, 2022. [arXiv:2207.05221](https://arxiv.org/abs/2207.05221)

### Design extracted

- Generates an answer, then asks a model to assign `P(True)` to that proposed
  answer using a True/False formulation.
- Measures discrimination and calibration with Brier score, AUROC, calibration
  curves, and expected calibration error rather than judging confidence prose.
- Shows the evaluator several independently sampled candidate answers in one
  condition, making disagreement visible before it judges a target answer.
- Trains `P(IK)` (“probability I know”) from repeated answer samples and tests
  transfer across tasks, source-material availability, and helpful/distracting
  hints.
- Partially tests the “question difficulty, not self-knowledge” rival by comparing
  models with distinct pretraining distributions on questions where their success
  differs.

### Transferable method

Separate answer generation from answer evaluation; elicit a numeric probability;
score it across many resolved items; and test whether the signal is model-specific
rather than merely a generic difficulty estimate. Alternative samples can improve
evaluation but consume additional inference and require an equal-cost baseline.

### Limits for this project

Correctness labels are required to validate calibration. Formatting and few-shot
examples materially affect calibration. A model may estimate how difficult a
question is without detecting its own particular error. The paper also notes that
models do not inherently know whether evaluated tokens were authored by
themselves or supplied by someone else.

## 3. Lin et al. — verbalized probability

Primary source: Stephanie Lin, Jacob Hilton, and Owain Evans, *Teaching Models to
Express Their Uncertainty in Words*, 2022.
[arXiv:2205.14334](https://arxiv.org/abs/2205.14334)

### Design extracted

- Fine-tunes a model to emit an answer plus a numerical or categorical confidence
  without requiring access to output logits.
- Uses CalibratedMath task families with held-out question types to test
  distribution shift.
- Uses mean squared error/Brier score, calibration deviation, and calibration
  curves; separates answer accuracy from confidence quality.
- Compares verbalized confidence with logit-derived methods, a constant baseline,
  hand-built difficulty heuristics, and a representation probe.

### Transferable method

Replace stylistic “caution” scores with explicit probabilities and proper scoring
over repeated resolved predictions. Hold out entire task types, and compare
against cheap difficulty heuristics before attributing confidence to genuine
self-monitoring.

### Limits for this project

The method requires many labeled outcomes and supervised fine-tuning. Aggregate
calibration does not establish that a single explanation is truthful, and a
calibrated agent can still be confidently wrong on a particular case.

## 4. Farquhar et al. — semantic entropy

Primary source: Sebastian Farquhar et al., *Detecting hallucinations in large
language models using semantic entropy*, Nature 630, 625–630 (2024).
[DOI:10.1038/s41586-024-07421-0](https://doi.org/10.1038/s41586-024-07421-0)

### Design extracted

- Samples multiple answers to the same question.
- Clusters answers by meaning using entailment rather than treating paraphrases as
  different answers.
- Computes entropy over semantic clusters; a discrete variant works without token
  probabilities or model internals.
- Tests error detection with AUROC and selective-answering performance across
  multiple datasets and model families, including out-of-distribution settings.

### Transferable method

Semantic instability is an observable warning signal that can be computed at
deployment without knowing the correct answer or the task's generative process.
It is a candidate trigger for “seek external evidence” rather than a truth test.

### Limits for this project

The method targets confabulations: wrong answers whose meanings vary under
sampling. It is validated against labeled correctness even though labels are not
needed for deployment. Inference from the paper's definition: a stable,
systematic false belief may have low semantic entropy and evade detection.
Entailment clustering introduces another model and another error surface, and
multiple samples add cost.

## Cross-paper synthesis

No scanned method establishes open-world truth with no eventual external anchor.
They instead provide three separable capabilities:

1. **Correction accounting:** did revision improve or damage a labeled answer?
2. **Confidence calibration:** do numeric confidence levels match long-run outcomes?
3. **Instability detection:** do independent samples disagree in meaning before a
   truth label is available?

The third can operate without current ground truth, but it detects instability,
not falsity. A low-entropy, highly confident, consistently repeated explanation
can still be wrong. Therefore an epistemic instrument needs both an internal alarm
and a later reality channel; neither cautious prose nor self-consistency is a
substitute for external contact.

## Candidate controls for a successor experiment

- Record correct-to-incorrect and incorrect-to-correct transitions separately.
- Match correction methods to baselines with equal calls/tokens.
- Compare revision prompts with the same information placed in the initial prompt.
- Collect numeric confidence before and after evidence; score only after outcomes
  resolve.
- Compare self-confidence to question-difficulty and constant baselines.
- Sample semantic alternatives and treat entropy as an escalation trigger, not a
  correctness verdict.
- Include deliberately stable false premises to measure the entropy method's
  expected blind spot.
