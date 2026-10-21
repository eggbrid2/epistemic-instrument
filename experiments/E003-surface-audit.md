# E003 synthetic surface audit

Status: construction diagnostic; eight synthetic fixtures; no subject data

Date: 2026-10-21 (Asia/Shanghai)

## Scope

`E003-audit-surface.py` joins the public fixtures to the private oracle and asks
whether one shallow feature at a time can recover truth labels in-sample. Numeric
features receive the best decision stump; categorical features receive a
per-category majority rule. The audit includes presentation, generator family,
source length, line count, domain length, claim length, explanation word count,
and the count of numeral tokens in source.

This is deliberately not an alarm model. It uses oracle labels, has only eight
items, searches thresholds on the same items it scores, and estimates no
out-of-sample performance.

## Finding and repair

The first run found a construction artifact. Explanation word count alone scored
6/8 (`accuracy = 0.750`, `balanced accuracy = 0.667`), compared with a false-only
majority baseline of 5/8 (`accuracy = 0.625`, `balanced accuracy = 0.500`). The
four narrative explanations ranged from 22 to 28 words.

Because these are pre-data synthetic fixtures, the explanations were rewritten
to exactly 24 whitespace-delimited words each. The original diagnostic is
reported here rather than erased.

## Post-repair result

| Feature | Accuracy | Balanced accuracy |
|---|---:|---:|
| Majority baseline | 0.625 | 0.500 |
| Presentation | 0.625 | 0.500 |
| Generator family | 0.625 | 0.633 |
| Source characters | 0.625 | 0.633 |
| Source lines | 0.625 | 0.633 |
| Domain characters | 0.625 | 0.633 |
| Claim characters | 0.625 | 0.633 |
| Explanation words | 0.625 | 0.500 |
| Source numerals | 0.625 | 0.633 |

No audited single feature now exceeds majority accuracy. That is not a clean bill
of health. Affine-modulo items contain one true and three false claims, while the
rotation family contains two true and two false claims. Family identity therefore
changes the observed truth base rate from 25% to 50%; the balanced-accuracy shift
in the table reflects this imbalance even though raw accuracy does not improve.

## Second family

The new `rotate_boundary_weight` family operates on all 32 binary lists of length
five. It rotates a list, then conditionally writes one boundary bit. Its claim is
that Hamming weight is preserved. The oracle executes every input and
cross-checks it with a separately written list transformation.

The four items cross trigger bit (zero or one) with replacement bit (zero or one).
Truth requires equality of those two parameters, so neither trigger nor
replacement alone predicts the label. Narrative and neutral presentations each
contain one true and one false item. Unlike the first family, this family has no
modulus parameter, so the first family's modulus heuristic cannot transfer.

## Limits and decision

- Item IDs were excluded: a unique ID can memorize this fixed set but says
  nothing about a regenerated study packet.
- Raw word identities and semantic source features were not screened. Exhaustive
  feature mining on eight items would manufacture apparent predictors.
- Code semantics must predict truth in a solvable task; the target is accidental
  construction cues, not removal of the actual evidence.
- Both executable and reference oracles still share one author and one parameter
  manifest.
- The audit is descriptive and post-construction. It cannot authorize subject
  collection or support a generalization claim.

E003 remains mutable. Before freezing it, generator-family truth base rates need
balancing and the audit must be rerun on a substantially larger development set,
with a separately generated family held out from all rule selection.
