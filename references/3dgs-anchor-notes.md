# Optional notes: 3D Gaussian splatting and anchor compression

Use only for relevant 3DGS/anchor tasks. Analyze the paper's own representation, predecessors and actual baselines; do not assume HAC++ is its target, baseline or architectural template. A prior HAC++ analysis may illustrate report depth/organization only. These are inspection questions, not verified claims about any particular paper or repository. Obtain the exact paper version, source commit and configuration before mapping mechanisms. Do not assume paths or architectural details from a method name.

## Disambiguate “anchor redundancy”

Ask which redundancy is evidenced:

- Spatially duplicated or low-utility anchors.
- Correlation among anchor features, attributes, offsets or scales.
- Predictable conditional distributions that an entropy model can exploit.
- View-dependent/reconstruction-irrelevant capacity.
- Excess precision or poor bit allocation.

These suggest different seams: selector/pruner, predictor/residual transform, quantizer, entropy model or allocator. Deleting an anchor is not the same operation as coding its attributes more efficiently. A denser representation can sometimes code more efficiently; fewer parameters alone does not establish a smaller bitstream.

## Trace both rendering and coding

Identify the actual stored representation and how it produces rendered Gaussians. Trace anchors, associated features/attributes, offsets, neural components and any view-dependent computation only where present in the inspected system. Verify shapes, cardinality and grouping rather than importing them from another implementation.

For the coding path inspect:

- Which tensors are encoded, reconstructed or predicted, and which are excluded from accounting.
- Quantization rules at training and actual encode/decode time.
- Entropy context and whether all conditioning values are decoder-available.
- Spatial ordering, multilevel/coarse-to-fine dependencies and the cost of maintaining them.
- Encoder/decoder access to coordinates, occupancy, hash/grid state, learned networks, dictionaries, masks and metadata.
- Actual coder and serialization entry points, output files and round-trip reconstruction evidence.

A training estimate of `-log2 p` is not an actual bitstream measurement. A context model that sees original rather than reconstructed attributes may leak unavailable information. Any decoder-shared state must be transmitted, deterministically reconstructed, or explicitly treated as preinstalled with a justified accounting boundary.

## Quality and rate controls

Compare scene-wise PSNR/SSIM/LPIPS with actual stored bytes at matched evaluation settings, render resolution and test views. Keep the metric directions explicit: higher PSNR/SSIM is usually favorable; lower LPIPS is favorable under the chosen implementation. Report PSNR changes in dB, not percentages.

Record per-scene versus averaged values and weighting. Do not compare an average ratio to a ratio of averages without identifying the distinction. Account for model/shared-network storage, side information and metadata. Separate encoding time, decoding time, rendering throughput and peak memory. Verify rate/quality tuning and training budgets rather than attributing all differences to a replacement module.

## Optional transfer families, not default analysis or recommendations

Use this section only when the current request explicitly asks for transfer or target adaptation; otherwise omit candidate search and adaptation plans.

- Geometry or point-cloud mechanisms may offer permutation-aware selection/context, but can introduce expensive ordering or spatial indexing.
- Image/video coding may offer prediction, quantization or context mechanisms, but assumptions about regular grids and causal neighborhoods may fail.
- Vector quantization or transform coding may reduce feature redundancy, but codebook and decoder costs can dominate small scenes.
- Resource-allocation methods may adjust precision or anchor budgets, but require a utility signal aligned with held-out rendering quality.

For each, return to the generic contract and target-domain prior-art search. A minimal test should measure real rate–distortion and applicable time/memory costs; reject candidates that improve a proxy while worsening the user's actual deployment tradeoff.
