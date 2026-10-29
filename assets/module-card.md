## [A]. [Functional module / paper-specific name]

Use the same ID as the overview and evidence/gain ledger. Copy only relevant fields; unknown is a valid value. This card belongs after the overview, not before it. Do not treat every module as novel or independently gain-producing.

### 1. Own baseline → change and attribution
- Role and bottleneck: [what responsibility this module has]
- Starting point: [direct predecessor / paper's own baseline and source; distinguish from empirical comparators]
- Before → after: [existing behavior → concrete change; or unchanged/unknown]
- Attribution: [inherited / newly proposed by this paper / modified / engineering implementation; source and uncertainty]
- Paper locator: [version, section/equation/algorithm/page]

### 2. Inputs/outputs and mechanism
- Inputs → outputs: [symbols, semantics, shape/type/units, ordering/cardinality]
- Operation/formula: [steps; source equation and defined symbols, or labeled explanatory formulation]
- State and initialization/update:
- Objective and optimization/gradient boundary:
- Lifecycle: [train/preprocess/encode/decode/infer/update]
- Hard constraints: [available information, causality, symmetry, precision, resources]
- Coupling and interface: [representation, losses, training, callers/consumers, decoder state]

### 3. Code correspondence
- Inspected implementation: [repository URL@SHA, path:lines, symbols; or missing evidence]
- Reachable path: [caller → module → consumer; entry point]
- Configuration: [enabling flag/default/override; train versus encode/decode/inference variants]
- Correspondence: [verified / partial / contradicted / unverified + reason]
- Evidence boundary: [paper claim / code evidence; static source inspection is not runtime reproduction]

### 4. Gain evidence, costs and limits
| Result ID / module IDs | Basis and attribution level | Comparator → variant | Metric/unit/direction | Original values | Protocol/controls | Locator | Comparability |
|---|---|---|---|---|---|---|---|
| [G1 / A, …] | [reported/reproduced; isolated/conditional/joint/whole-system] | | | | | | [comparable/conditional/confounded/unknown] |

- Derived change **only if comparable or supported under a stated condition**: [formula, denominator, limits]. For confounded/unknown rows, keep original values only—no derived deltas, ratios, percentages, ranking or module credit.
- Missing isolation: [e.g. no independent ablation; only joint/whole-system evidence; do not allocate that result to this module]
- Full cost boundary: [compute, parameters, memory, bytes/side information, setup/retraining; measured versus unreported]
- Attribution/uncertainty and failure conditions:

### Optional extension — only for an explicitly requested transfer
- Target contract and verified/provisional replacement seam:
- Candidate mechanism, source citation and target-domain prior art:
- Contract match, adapter, retraining and decoder/inference changes:
- Benefit hypothesis, extra costs and negative conditions:
- Novelty status and search coverage:
- Minimal falsification: [rejection observation, baseline/replacement controls, protocol, full costs and uncertainty]
- Decision criterion: [user-specified or proposed]
- Resources/authorization and unresolved item: [action | target | reason | status]
