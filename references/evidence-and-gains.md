# Evidence tracing and defensible gains

Read for claim–code mapping, numeric extraction or ablation comparison.

## Evidence ledger

Use a row per material claim or result:

`Evidence/result ID | module ID(s) | claim/measurement + attribution level | paper version + page/section/equation/table/row | repository URL + SHA + file:lines + symbol | caller → callee → consumer | active config | evidence label | correspondence | limitation`

Use the overview's stable A/B/C/… module IDs. A whole-system result belongs to the system, not to each module; a joint result may reference multiple IDs without duplicating its credit. An evidence/result ID such as G1 is not a new module. Distinguish direct method predecessors, the paper's own baseline variants and empirical comparators. Do not insert an external target merely because it was used in another analysis.

Only cite a source location as inspected when its underlying contents were actually checked. Search snippets, README descriptions and references inside another document are indirect evidence, not verification of the referenced source.

A paper statement and code implementation are different evidence objects. For example, a rate objective in training does not show that a codec writes a decodable file. Trace the training path and the serialization/decode path separately. Inspect configuration defaults and overrides, entry points, feature flags, checkpoint dependencies and referenced submodules. A reachable static path supports implementation correspondence, not proof of actual runtime use in published experiments.

Pin source before giving exact line citations. Record local modifications when they affect interpretation. If access fails, report whether the missing item is the paper, supplement, repository, commit, submodule, config, checkpoint or results log. Do not reconstruct “verified” code from prose. Preserve unresolved paper/code disagreement rather than choosing the more convenient version.

## Original numbers before derived numbers

For every result capture:

- Baseline and candidate identity/version; exact original values, units and metric direction.
- Paper/supplement locator or reproduction log path and run identity.
- Dataset, split, preprocessing, scene/sample aggregation and evaluation implementation.
- Training budget, data access, hardware/timing boundary, checkpoint selection and seeds if reported.
- Operating point: quality constraint, rate/lambda, resolution, resource budget or other relevant condition.
- Changed controls and cost inclusions/exclusions.

Keep reported and reproduced results separate even when they agree. Missing uncertainty does not imply certainty. Digitized plot readings must be labeled approximate with extraction limitations; never silently give them the precision of a table.

## Comparability gate

A delta is meaningful only for a defined comparison. Classify:

- **Comparable:** relevant protocol and operating point matched; explain any remaining limitation.
- **Conditional:** a specific comparison is supported, but scope is restricted (for example one scene or a joint ablation).
- **Confounded:** material factors differ; preserve original results and explain the mismatch.
- **Unknown:** needed protocol details unavailable; preserve original results and leave the comparison unresolved.

**Hard gate:** for confounded or unknown comparisons, do not compute or report any derived delta (including a signed absolute change), percentage, ratio, speedup, ranking or module attribution. Calling arithmetic “descriptive” does not bypass this gate. State “not computed: comparison confounded/unknown” and what would resolve it. For conditional comparisons, compute only the supported, explicitly scoped comparison and retain its limitation. Apply this gate before the formulas below or any helper invocation.

A baseline from a different paper may have different evaluation code or accounting. Same metric label is insufficient. Do not rank compression methods using quality-mismatched sizes as if quality were held fixed. A rate–distortion curve can support matched-quality interpolation only within measured overlap, with the interpolation method disclosed; do not extrapolate an unmeasured advantage.

## Arithmetic and wording

Let `B` be the baseline value and `C` the candidate value.

- Raw signed change: `C - B`, in the metric's original units.
- Lower-is-better relative reduction, for meaningful positive `B`: `100 × (B - C) / B`.
- Higher-is-better relative increase, only for ratio-scale metrics with meaningful positive `B`: `100 × (C - B) / B`.
- Speedup for matched work: baseline elapsed time / candidate elapsed time; state that numerator and denominator explicitly.
- Compression factor must name its reference: e.g. uncompressed bytes / coded bytes, or baseline coded bytes / candidate coded bytes. These are not interchangeable.
- Accuracy expressed as a percentage: report percentage-point change first; relative-percent change is a separate quantity with its denominator identified.
- PSNR: report absolute dB change, not a percentage “PSNR improvement.” A dB difference is not a percentage quality improvement.
- Non-ratio scales, negative/zero baselines, saturating scores and losses with arbitrary offsets require metric-specific treatment; do not force relative percentages.

Illustrative arithmetic only: coded size 100 → 80 units is a 20% reduction and a 1.25× baseline-to-candidate ratio. PSNR 30 → 31 dB is +1 dB. These are not experimental evidence.

Any helper script is a calculator, not an evidence judge. Inspect its help/interface before invocation and keep input provenance beside its output. Never infer protocol equivalence or component attribution because a number was accepted by a script.

## Ablations and actual costs

A remove-one ablation estimates a difference conditional on the rest of the tested system. An add-one ablation has a different baseline. Interactions, retuning and retraining matter; neither permits summing separate gains into an expected whole-system gain. If multiple components changed, label the result joint, not attributed to each component. If a module has no independent ablation, explicitly say so; retain any applicable joint or whole-system evidence at that level, or mark no separate gain evidence. Do not invent a per-module gain merely to fill the overview. Module count and innovation count need not match, and neither determines how many gains can be measured.

Audit quality and benefit together with storage, runtime, memory and implementation costs. For compression distinguish:

1. Entropy estimate or differentiable rate proxy.
2. Quantized tensor size or nominal parameter precision.
3. Actual decodable bitstream size, including required metadata, codebooks, learned decoder parameters and side information.

State whether each cost is per-scene, amortized across scenes, shared/preinstalled or excluded. Report encoder and decoder time separately; specify whether disk I/O, preprocessing, setup and GPU synchronization are included. A module that saves bits but needs unavailable decoder context or unacceptable decode latency may be incompatible despite a favorable proxy.

## Bundled calculation helper

From the skill directory:

```bash
python scripts/compute_gains.py --help
python scripts/compute_gains.py --example
python scripts/compute_gains.py INPUT.json --output OUTPUT.json
```

Input is an object with a `comparisons` list. Each comparison requires `id`, `metric`, `metric_kind`, `baseline`, `candidate`, `direction`, `protocol_comparable`, `evidence_basis`, `changed_factors` and `confounds`. Each measurement requires `value`, `unit`, `source` and `value_basis` (`actual` or `normalized`). Obtain precise enum values and a complete example from the helper rather than inventing defaults.

The helper preserves original records and emits flags, gains or null, and an attribution note. It does not authenticate source strings. `rankable` means the submitted metadata passed arithmetic safeguards, not that independent scientific review certified the comparison. Manually verify every protocol/evidence field before using the result. Reported whole-model differences never become module effects through calculation; even a reported ablation still requires attribution review.

PSNR and SSIM receive absolute changes only. Positive bytes/latency/FPS values can receive explicitly directed ratios and percentages. Unit conversion is not automatic; units and value bases must match. Normalized values remain labeled normalized, not actual measured baselines. BD-rate cannot be derived from two scalar points and is rejected by this helper; it needs suitable full curves and a separately validated procedure. Missing/invalid metadata, known confounds or incomparable protocols prevent gains rather than silently weakening the comparison.
