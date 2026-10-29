# Constraint-led cross-domain mechanism search

Read only when the current request explicitly asks for cross-domain mechanisms, replacement, migration or target adaptation, and after extracting the source and requested target functional contracts. Do not infer this mode from long-term interests or previous HAC++ work. Default paper analysis is complete without this workflow.

If the user requests transfer without enough target evidence, offer conditional candidates and identify the missing interface/version; do not fabricate a target or verified integration seam. Keep the paper's own predecessor/comparator analysis separate from the requested transfer target.

## Search construction

Start with a domain-neutral sentence:

> Given [observable input and state], produce [required output] to reduce [bottleneck], while respecting [information, symmetry, resource and lifecycle constraints].

Separate hard constraints from preferences. Translate the sentence into several searchable formulations, including synonyms for the problem and its information structure. Search complementary communities because they may solve the same function under different names. Example problem families, not mandatory destinations:

| Abstract problem | Potentially complementary fields | Critical compatibility check |
|---|---|---|
| Redundant unordered spatial elements | point-cloud coding, mesh simplification, sensor sampling | permutation behavior, geometry distortion, selection metadata |
| Predict a symbol from known context | image/video codecs, language models, time-series forecasting | decoder availability, causal ordering, sequential cost |
| Allocate limited bits or computation | rate–distortion optimization, scheduling, adaptive computation | cost observability, joint objective, optimization overhead |
| Represent correlated latent vectors | transform coding, vector quantization, low-rank models | dictionary cost, distribution shift, inverse/decoder cost |
| Select a useful subset | sparse modeling, active learning, coreset construction | task-specific utility, reconstruction needs, selection cost |

Example query pattern: `"conditional entropy" "unordered point" "causal decoding"`, then adapt vocabulary using primary sources. An exact keyword match is not sufficient evidence that the mechanism fits.

## Search provenance and novelty limits

Record search date, databases/web sources, meaningful query families, screened scope and primary source links. Retrieve the original method rather than relying on a review's characterization. Follow relevant references and later adaptations when needed to resolve close prior work. Inspect available implementations before making code-level assertions.

Also search the target domain for the same function and equivalent mechanisms, including differently named prior art. Distinguish:

- **Known source mechanism:** verified origin/description, properly attributed.
- **Known target-domain use:** prior adaptation found; cite it and identify any remaining proposed difference.
- **Novelty unproven:** no close use found within documented search coverage; this is not a novelty guarantee.
- **Unsupported:** evidence too weak to assess the mechanism or transfer.

Do not call a proposal novel solely because it comes from another field, has a new acronym, or combines known blocks. Do not omit source attribution to make an adaptation look original. Reuse of implementation additionally requires checking license, notices and compatibility before copying; conceptual inspiration does not authorize copying unlicensed source or skill text.

## Candidate comparison

For each retained mechanism write:

`functional match | source evidence | target prior art | hard constraint compatibility | adapter | training/decoder coupling | predicted benefit | full extra cost | failure condition | decisive test | novelty status`

Do not assign a precise numerical gain without a target experiment. Published gains from the source domain are evidence of behavior there, not transferable effect sizes. Rank by compatibility, evidence and testability rather than novelty rhetoric. Explain rejected candidates when their failure teaches a useful boundary; for example, a bidirectional predictor is unsuitable for a one-pass causal decoder unless a valid side-information or multi-pass design is costed.

## Adaptation versus replacement

A replacement must satisfy the target seam's contract or make all required interface changes explicit. Check:

- Is a permutation/order assumption introduced? Can encoder and decoder reconstruct the same order?
- Does a learned dictionary or context require transmission, synchronization or retraining?
- Does the candidate use labels, future values, originals or full-resolution features unavailable at inference/decode time?
- Are rate/quality/latency objectives actually aligned? Is the metric a proxy with a known mismatch?
- Does training relax a discrete operation in a way that fails at actual inference?
- Can adapter overhead or retuning explain the observed effect?

A plan should name the smallest diagnostic that can reject the central assumption, then a controlled baseline/replacement comparison if the diagnostic passes. Keep recommendations conditional where target interfaces are unknown. When every plausible candidate violates a hard constraint, report that result and specify the constraint relaxation needed—not a forced winner.
