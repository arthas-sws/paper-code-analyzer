---
name: paper-code-analyzer
description: "Decompose research papers into functional modules, distinguish inherited/new/modified components against the paper's own predecessors and baselines, map mechanisms to verified source, and audit gains/costs. 用于论文模块拆解、创新归属、公式机制讲解、代码对应与消融收益核对；默认先给模块总览表，再按对应编号展开。仅在明确要求迁移或指定适配目标时追加跨领域替代与验证方案。"
---

# 论文与代码分析 / Paper Code Analyzer

Explain **what parts a paper's method contains, what each part changes relative to its own starting point, how it works, where it is implemented, and what evidence supports its effect**. Make the method's structure visible before summarizing its results. Treat transfer as a separate, explicitly requested extension—not the purpose of every paper analysis.

## Scope and mode

- Default to **paper analysis**: the paper's own method, direct predecessors, actual comparison baselines and ablation variants. Distinguish an architectural predecessor from an empirical comparator; they need not be the same method. Do not assign a universal target baseline.
- **HAC++ is not a default target.** A previously reviewed HAC++ report may illustrate depth or organization only. Do not import its architecture, vocabulary, constraints or comparisons into a different paper or research path. Include HAC++ only if relevant primary evidence makes it a predecessor/comparator, or the user explicitly requests it as a transfer target.
- Enable **optional transfer mode** only when the current request explicitly asks for cross-domain mechanisms, replacement, migration or adaptation to a target. Long-term research interests, earlier work on another method, and this skill's technical name do not authorize transfer analysis.
- Match depth to the immediate question. For a full paper analysis use the table-first report below. For a narrow mechanism, code or gains question answer that question; do not force a full report, unrelated modules or transfer search.
- If only a paper is available, analyze it and mark missing code/supplement evidence. Do not ask for an unrelated target baseline. In transfer mode, ask for target details only when necessary; otherwise keep candidates/seams explicitly conditional.
- Default to read-only research. Inspect supplied papers, accessible repositories, configurations and existing results. Do not install dependencies, execute repository code, run training/experiments, modify a baseline or rewrite the user's paper without authorization. Reading source is not permission to run it.
- Use the user's language while retaining searchable technical terms and identifiers. State blockers as action, target, reason and unresolved evidence.
- For a large collection, propose a bounded queue or representative sample rather than automatically processing the entire library. Complementary skills may help, but do not replace primary evidence.

## Default full-report structure: scope → table → matching sections → results and limits

Use [assets/paper-report-outline.md](assets/paper-report-outline.md). **Begin with a brief scope statement and a functional module overview table**, not an executive recommendation, whole-system scorecard or transfer verdict.

In the scope statement identify the paper/version, its own method lineage/comparison scope, and the main evidence availability. Then provide:

| ID | Functional module / role | Attribution | Change from its own starting point | Paper location | Pinned code, call path and configuration | Gain evidence or its absence |
|---|---|---|---|---|---|---|
| A, B, C, … | Role first; paper's name second | Inherited / newly proposed / modified / engineering implementation; cite basis | Predecessor/baseline behavior → this paper's change; or explicitly unchanged/unknown | Section, equation, algorithm, table | Inspected repository@SHA, path/symbol, caller → consumer, enablement; or unverified | Isolated / conditional / joint / whole-system only / no separate evidence |

- Derive module boundaries and count from the method, not from the number of advertised contributions. A/B/C are identifiers, **not a required three-module count**. Include inherited components needed to understand the method, but do not promote every helper function to a module. Module count is not innovation count.
- Keep one stable ID set across overview, body and evidence/gain ledgers. Use sections **A. [module]**, **B. [module]**, etc. Expand every overview row; do not silently introduce, omit or renumber modules. Distinguish any submodules with hierarchical IDs when useful.
- In each section follow **own baseline/predecessor → change and attribution → inputs/outputs/formulas/mechanism → code/call/configuration → gains/costs/limits**. Use [assets/module-card.md](assets/module-card.md) selectively. Make engineering details and inherited mechanisms visible without declaring them novel.
- Put the whole-system result summary **after** the module sections. Keep whole-system and joint results at their actual attribution level; do not distribute them among modules. Place overall conclusions, limitations and unresolved evidence at the end, followed only by a concise consistency check.
- Do not invent an independent gain for each module. “No independent ablation; only joint/whole-system evidence” is a useful result. An inherited component may have no separately measured gain in this paper.
- Keep the overview readable: use short locators or evidence IDs that resolve to exact details in the matching section/ledger. Never substitute generic repository links for verified source locations.

## 1. Establish the evidence boundary and actual comparison frame

Record paper title/version, main paper and supplement availability, repository URL, exact inspected commit SHA and relevant configurations. Record direct predecessors and the paper's actual comparison/ablation baselines with their roles. Add a target baseline/version only in explicitly requested transfer mode. Mark forks, dirty changes, unavailable submodules and paper/code version divergence.

Keep these labels separate throughout:

| Label | Meaning |
|---|---|
| Paper claim | What authors assert; not implementation verification or established novelty |
| Code evidence | Behavior visible in inspected, pinned source and its reachable call path |
| Reported result | Authors' original measurement and protocol; not a run performed here |
| Own reproduction | Result actually executed here, with logs/configuration/seeds |
| Transfer hypothesis | Proposed adaptation or expected effect, not a finding |
| Unverified | Necessary evidence missing, inaccessible or inconsistent |

Read [evidence-and-gains.md](references/evidence-and-gains.md) for tracing and every numeric comparison. A README, search snippet, cited filename or inaccessible link is a lead, not proof that the underlying paper/code was inspected. Cite only locations actually checked; label indirect descriptions as such.

## 2. Decompose by function and establish attribution

Read the method's data flow before enumerating innovations. Choose coherent boundaries with identifiable inputs, outputs and responsibilities: **selector, predictor, residual transform, quantizer, entropy model, allocator, aggregator, scheduler**, or another precise role. Separate transform, quantization, probability estimation and bitstream coding when their interfaces and costs differ.

For each module:

1. Identify what the direct predecessor or the paper's own baseline already did. If unavailable, state what the paper reports and what remains unverified; do not substitute a familiar method.
2. Explain exactly what is unchanged, added, removed or modified, including the previous behavior and new behavior. Attribute borrowed mechanisms to their sources. Separate an author's novelty claim from independently checked provenance.
3. Label the component inherited, newly proposed by this paper, modified, or engineering implementation as supported. Use mixed labels for mixed components. “Newly proposed” is not a guarantee of field-wide novelty.
4. Describe its functional contract below. Do not collapse a multi-part method into a results summary, or inflate ordinary implementation details into innovations.

### Functional contract

Preserve material details; omit irrelevant fields rather than filling them speculatively:

- **Problem and role:** concrete redundancy, uncertainty, allocation or other bottleneck; why the boundary exists.
- **Inputs → outputs:** symbols, semantics, shapes/types/units, variable cardinality, ordering and stochasticity.
- **State:** learned parameters, caches, statistics, shared dictionaries and initialization/update rules.
- **Mechanism and objective:** stepwise operation, relevant source equations with symbols explained, optimized/constrained quantities and gradient/optimization boundaries. Do not force a formula onto an engineering mechanism or present an explanatory formula as a paper equation.
- **Lifecycle:** training, preprocessing, encoding, decoding, inference and updates that actually apply.
- **Hard constraints:** information available at each stage, causality, symmetry/invariance/equivariance, differentiability, precision, latency and memory.
- **Coupling:** representation, losses, joint training, upstream/downstream modules and decoder-side information.
- **Cost boundary:** compute, parameters, temporary memory, transmitted/stored bits, side information, and setup/retraining where material.
- **Interface boundary:** what callers and consumers require. Develop a replacement seam/adapter only when transfer is requested.

For relevant Gaussian-splatting or anchor-compression tasks read [3dgs-anchor-notes.md](references/3dgs-anchor-notes.md). Its inspection questions do not imply that another paper uses anchors, HAC++ or the same coding path.

## 3. Match each mechanism to active implementation

For each material module/claim:

1. Locate its definition, equation or algorithm in the paper/supplement.
2. Inspect implementing symbols and record `repository@SHA:path:start-end`.
3. Trace **caller → implementation → downstream consumer** and enabling configuration. Separate active paths, unused helpers, alternate variants and training-only proxies; inspect defaults and overrides.
4. Mark correspondence verified, partial, contradicted or unverified, with the reason.

Do not invent line numbers or source behavior from a README, filename or search snippet. If missing, name the exact file/submodule/configuration needed. Static reachability supports implementation correspondence, not proof of execution in the published run. Preserve paper/code disagreements.

## 4. Audit gains and costs at the supported attribution level

Transcribe original values with metric/unit/direction, dataset/split, quality/rate operating point, comparator, exact table/row locator and evidence basis. Distinguish standalone ablations, joint changes and whole-system comparisons; record changed controls and uncertainty.

Apply the comparability gate in [evidence-and-gains.md](references/evidence-and-gains.md) **before arithmetic**. For confounded or unknown comparisons, preserve original values and reasons only: **do not calculate or report any derived delta, percentage, ratio, speedup, ranking or module credit**, even as “descriptive arithmetic.” For conditional comparisons, restrict claims to the tested condition. Do not assume protocol equivalence because metric names match.

Ablations support effects under their actual controls. Never sum separate component gains or infer an isolated effect from a joint/whole-system result. For modules without isolating evidence, state the absence explicitly. Describe intended effects as mechanism explanations, not measured improvements.

Use `scripts/compute_gains.py` only after reading its help/interface and validating inputs. It is an arithmetic helper, not a source/comparability/causality judge. Keep reported results separate from actual reproductions. Account for full costs and failed/tradeoff cases, not benefits alone.

## 5. Optional: search for cross-domain mechanisms

**Skip this section and section 6 unless the current request explicitly activates transfer mode.** Do not append them to ordinary paper analysis for completeness.

Read [transfer-search.md](references/transfer-search.md). First define the requested target's functional contract and hard constraints, using its own verified source where available. Search by the abstract problem and information structure rather than architecture fashion; check close target-domain prior art as well.

Keep only a useful evidence-backed shortlist, with no fixed candidate count. For each candidate record source mechanism/attribution, primary evidence, assumption match/mismatch, adapters/retraining/decoder changes, benefit **hypothesis**, full extra costs, negative conditions, target-domain prior use and search/novelty limits. Source-domain gains are not target effect estimates. Prefer a supported negative finding over forced recommendations; never present renamed borrowing as novelty.

## 6. Optional: design the smallest informative falsification

For the best-supported requested candidate specify:

1. Hypothesis, bottleneck and observation that would reject the proposal.
2. Verified target integration seam, or explicitly provisional interfaces if source is missing.
3. Unchanged baseline versus replacement with matched data, budget and operating points; adapter-only control when relevant.
4. Quality/benefit, complete costs, failure cases, seeds/uncertainty, and applicable leakage/round-trip checks.
5. User-specified acceptable tradeoff, or a clearly proposed—not accepted—decision threshold.
6. Resources, missing inputs and required authorization; stop at the plan unless execution is authorized.

Prefer a cheap diagnostic before full benchmarking. Do not replace end-to-end outcomes with unlabeled proxies or describe a planned experiment as completed.

## Output checks and completion

Before sending a full report, check that the overview, matching sections and claim/gain ledgers use the same module IDs; joint results name all relevant IDs without duplicated attribution. Check that exact source statements, formulas, call paths and numbers are backed by inspected material or clearly labeled unverified/indirect. End with a concise check such as `核对：表格—正文—证据编号一致；未核验项已标明。` only when true; otherwise state the remaining mismatch.

When assessing coverage of this skill, separate **core paper-analysis coverage** (scope/baselines, overview and matching sections, attribution/contracts, source mapping, gains/costs and limits) from **optional transfer coverage** (search, target adaptation and falsification). Mark unrequested optional stages “not applicable,” not failed or incomplete. Judge narrow answers against their requested scope, not the full-report template.

Chat is enough for small tasks. Save reusable artifacts only when useful/requested and follow the user's destination conventions. Stop when the requested scope is evidenced, a defensible negative answer is established, or progress needs missing material/authorization. Do not automatically expand into a whole-library audit or experiments.
