# LoRA: a worked paper-to-code analysis

[简体中文](lora.zh-CN.md) | **English** · [Home](../README.en.md)

**Scope.** This example reads Hu et al.'s [LoRA, arXiv:2106.09685v2, 16 October 2021](https://arxiv.org/html/2106.09685v2), focusing on linear-weight adaptation and the official GPT-2 integration. Full fine-tuning is the starting comparison; adapters are latency comparators, not assumed architectural predecessors. Static source inspection on 2026-10-29 pins `microsoft/LoRA@c4593f060e6a368d7bb5af5273b8e42810cdef90`. This current snapshot is not certified as the code used in the original runs. No dependencies were installed and no models or experiments were run. Transfer and the paper's broader subspace studies are outside scope.

## Functional overview

| ID | Role | Attribution and change | Paper locator | Inspected source | Gain evidence |
|---|---|---|---|---|---|
| A | Pretrained backbone | Inherited representation; freeze its parameters instead of fully updating them | §2, §4.1 | [Layer constructor](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L90-L117), [parameter filtering](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/utils.py#L13-L30) | Parameter reduction jointly with B; no isolated accuracy credit |
| B | Low-rank task update | Paper-proposed update parameterization; matrix factorization itself is not claimed as new | §4.1, Eq. (3) | [Linear initialization and forward](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L119-L152) | Structural parameter counts; no reproduction here |
| C | Attention projection placement | Design choice plus grouped-projection engineering; inspected GPT-2 path adapts Q/V | §4.2, §7.1, Table 5 | [Attention construction](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/examples/NLG/src/model.py#L94-L102), [MergedLinear](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L155-L244) | G2: fixed-budget configuration comparison |
| D | Deployment merging and task-state saving | Linear deployment consequence plus implementation | §4.1, §4.2 | [Merge state machine](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L218-L244), [state filtering](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/utils.py#L33-L49) | G1: reported latency; inspected GPT-2 config disables merging |

Four functional responsibilities do not imply four innovations.

## A. Backbone and trainable-parameter boundary

The backbone retains the existing feature mapping while task changes use separate parameters. Its external projection interface stays intact.

Two different checks are necessary. `Linear.__init__` freezes that layer's original weight when `r>0` (`layers.py:109–114`), but that alone says nothing about every bias, normalization, or other model parameter. `mark_only_lora_as_trainable`, with default `bias='none'`, disables gradients for parameter names without `lora_` (`utils.py:13–30`). The inspected [training entry at lines 321–330](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/examples/NLG/src/gpt2_ft.py#L321-L330) loads the backbone, calls this filter only if `args.lora_dim>0`, and then creates the optimizer.

Thus `lora_dim=0` is not an enabled LoRA run. Selecting another bias policy changes the trainable boundary. Freezing does not remove backbone storage; gradients may still need to pass through frozen operations to earlier trainable adapters. It does not imply zero backward computation or zero activation memory. No isolated accuracy improvement is assigned to A.

## B. Formula, dimensions, initialization, and forward path

Expanding the scaling described alongside Eq. (3), the explanatory layer equation is:

$$h=W_0x+sBAx,\qquad s=\alpha/r.$$

Here `W₀` has shape `d×k`, `A` has shape `r×k`, and `B` has shape `d×r`. A maps into the bottleneck and B maps back to the output. The **update** is low-rank; neither the pretrained weight nor the final summed weight is thereby guaranteed low-rank.

The inspected [forward at lines 147–152](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L147-L152) uses row-batched tensors, so its update is `X Aᵀ Bᵀ`. It adds the branch only for positive rank while unmerged. Optional dropout acts on the update input, not the backbone branch.

### A concrete paper/code difference

The paper describes Gaussian A and zero B. The inspected [Linear initialization at lines 119–125](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L119-L125) uses Kaiming-uniform A and zero B. The zero-update starting condition agrees; the distribution does not. This inspection does not establish whether that difference affects performance.

Why avoid initializing both factors to zero? For one sample, output gradient `g`, and ignoring dropout, an explanatory derivation gives:

$$\nabla_B L=s\,g(Ax)^T,\qquad \nabla_A L=s\,B^Tg x^T.$$

With B zero and A nonzero, B can receive an initial update. With both zero, both gradients vanish. This is a mathematical explanation, not a new experiment or a reported measurement.

### Parameter accounting

A single bias-free projection changes from `dk` freely trainable weights to `r(k+d)` adapter parameters while retaining the frozen weight.

**Teaching assumption, not a paper experiment:** `d=k=4096`, `r=8` gives 65,536 adapter parameters versus 16,777,216 dense parameters, a count ratio of 1/256. This is not a measured file size, full-model compression ratio, memory reduction, or speedup. Backbone storage, other layers, numeric precision, optimizer state, and activations remain outside that count.

## C. Trace placement into actual consumers

The inspected GPT-2 path is:

```text
gpt2_ft.py: lora_dim / lora_alpha / lora_dropout
  → GPT2Config → GPT2LMModel
  → Attention.c_attn = MergedLinear
       enable_lora=[True, False, True]
  → Attention.forward → c_attn(x)
  → split into query, key, value
  → split_heads → _attn → merge_heads → c_proj
```

Configuration wiring is in [gpt2_ft.py:298–330](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/examples/NLG/src/gpt2_ft.py#L298-L330); consumers are in [model.py:140–181](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/examples/NLG/src/model.py#L140-L181). The mask and split order together verify Q/V updates and zero direct K update in this path. They do not imply unchanged K activations throughout training: upstream inputs can change.

`MergedLinear` packs factors for enabled blocks. Its grouped computation and `zero_pad` restore updates into the complete output layout, rather than permitting arbitrary mixing across Q/K/V updates; see [lines 177–216](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L177-L216). `fan_in_fan_out=True` handles the original projection's storage orientation.

Do not transfer B's explanatory operation order directly into this implementation. `Linear.forward` applies two successive low-rank projections; this `MergedLinear.forward` calls `merge_AB()` to construct the update matrix before multiplying the input. The trainable parameterization is still low-rank, but temporary matrices, operation order, and costs differ. Parameter counts alone cannot establish this path's FLOPs, memory, or training speed.

G2 changes placement and per-projection rank under a fixed overall budget. It is not an isolated estimate of adding Q at fixed rank. Nor does inspecting this GPT-2 path reproduce GPT-3 Table 5.

## D. Merging, checkpoints, and deployment

For a fixed task, with inference dropout inactive, linearity permits:

$$W_{\mathrm{deploy}}=W_0+sBA.$$

This permits the original-sized linear operation after merging. It does not establish that every integration enables merging or that training has no overhead.

The library [merge state machine at lines 218–244](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/layers.py#L218-L244) adds the update on evaluation and subtracts it on returning to training when `merge_weights=True`; the `merged` flag prevents repeated addition. However, inspected [GPT-2 Attention at lines 94–102](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/examples/NLG/src/model.py#L94-L102) explicitly sets **`merge_weights=False`**. Calling `eval()` alone will not merge that path, which retains the update branch. This is not identified as the original latency benchmark script; other export tools were not audited.

The [training save at lines 223–226](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/examples/NLG/src/gpt2_ft.py#L223-L226) calls `lora_state_dict`; the [helper at lines 33–49](https://github.com/microsoft/LoRA/blob/c4593f060e6a368d7bb5af5273b8e42810cdef90/loralib/utils.py#L33-L49) defaults to LoRA parameters only. A task checkpoint needs the matching backbone and layer configuration; it is not a standalone model. Merge setup cost and floating-point effects also remain. No numerical equivalence or timing test was performed here.

## System results and evidence ledger

These are original values from the [paper](https://arxiv.org/html/2106.09685v2), not results reproduced here.

| ID | Attribution level | Original values and conditions | Interpretation |
|---|---|---|---|
| G1, Table 1 | D deployment motivation; system forward comparison | GPT-2 medium, batch 1, length 128, RTX8000, 100 forward trials: Fine-Tune/LoRA 19.8±2.7 ms; Adapter-L 23.9±2.1 ms; Adapter-H 25.8±2.2 ms; lower is better | Comparable within that table's conditions. Fine-Tune/LoRA is a jointly presented row, not two separately exposed samples. No separate speed credit for A/B/C; raw timing logs were not inspected |
| G2, Table 5 | B+C; fixed-budget configuration comparison | GPT-3, 18M trainable parameters: WikiSQL validation accuracy Q-only at rank 8: 70.4%; Q+V at rank 4: 73.7%; table reports seed standard deviation around 0.5% | Conditional comparison of placement/rank configurations. Difference: **+3.3 percentage points**, not isolated Q/V effects or a universal result |
| S1, explanatory count | A+B; single-layer structure | Hypothetical 4096×4096, rank 8: 16,777,216 versus 65,536 parameters | Not a measured paper result or performance benchmark |

The G2 subtraction is an accuracy **percentage-point** change, not a 3.3% relative improvement. No relative accuracy growth or statistical significance is claimed. A shared budget supports this scoped configuration difference without isolating placement from rank.

## Conclusions, limits, and demonstrated depth

The example reaches shapes, gradients, enablement, callers and consumers, grouped Q/V placement, merge-state behavior, checkpoint boundaries, and evidence attribution. It preserves two concrete differences: initialization distribution, and merge support versus the disabled GPT-2 setting.

It does not prove that low rank suffices for every task, certify historical experiment execution from current code, or turn parameter savings into proportional memory or speed savings. Reproduction would require matched data, backbone, environment, scripts, settings, logs, seeds, and authorization. Field-wide novelty assessment would require reading the cited predecessors; this example identifies paper-proposed mechanisms without certifying first invention.

**Completed depth: paper mechanism → module boundaries → equations and dimensions → pinned source → calls and configuration → reported measurements → costs and evidence limits. Not performed: installation, training, runtime reproduction, or transfer research.**

Check: A–D match the overview; G1/G2/S1 are not duplicated as isolated module gains; cited source was inspected; missing evidence and unperformed work are labeled. This is original commentary, without copied upstream source or a full paper reproduction. Upstream materials retain their own licenses.
