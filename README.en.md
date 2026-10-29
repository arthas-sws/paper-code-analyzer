# Paper Code Analyzer

[简体中文](README.md) | **English**

Decompose a research paper into functional modules and explain each module's provenance, mechanism, implementation, and supported gains.

This is an AI assistant skill: instructions, report templates, references, and a Python arithmetic helper. It is not a standalone paper-analysis application.

## What it does

1. Start with a module overview, then expand the same IDs in matching sections.
2. Distinguish inherited components, newly proposed components, modifications, and engineering implementation against the paper's own predecessors and baselines.
3. Explain inputs, outputs, equations, state, constraints, and coupling.
4. Map mechanisms to inspected commits, files, symbols, active call paths, and configurations; mark missing evidence.
5. Preserve original measurements and protocols, check comparability before arithmetic, and retain joint and whole-system gains at their supported attribution level.

Transfer, replacement, and target adaptation are optional extensions activated only by an explicit request. Missing ablations or inaccessible code are valid findings.

## Get started

Download or clone this repository into a new directory. In a host that supports skill import, import the directory containing `SKILL.md` with its relative structure intact. Import controls and available tools depend on the host.

For a manual installation into an existing custom skills directory, copy into a **new, nonexistent** `paper-code-analyzer` subdirectory. If that name already exists, stop and choose a backup or separate test environment. Do not overwrite an installed version.

Example request:

> Use paper-code-analyzer to analyze this paper and its official implementation. Start with a functional module overview, then use matching IDs to explain predecessors/baselines, equations, source correspondence, and gain evidence. Mark unverified evidence. Paper: [link or file]. Code: [link]. Write in English.

For a focused question:

> Explain only the quantization module: its inputs and outputs, training versus encoding behavior, and verified code correspondence.

Switching documentation language does not replace the original skill files.

## Guides

- [Workflow and analysis method](docs/workflow.en.md) · [中文](docs/workflow.zh-CN.md)
- [Synthetic evidence example](examples/evidence-example.md)
- [Contributing](CONTRIBUTING.md)
- [References and provenance](docs/provenance.md)

## Contents

The original entry point is `SKILL.md`; `agents/` contains UI metadata, `assets/` contains an icon and report templates, `references/` covers evidence, transfer, and optional 3DGS checks, and `scripts/compute_gains.py` provides arithmetic. Bilingual READMEs, `docs/`, `examples/`, and contribution guidance are publication additions. `SOURCE_MANIFEST.json` records original file hashes.

## Requirements and limits

The host must be able to read the paper, supplements, and source. Browsing, PDF reading, and repository access depend on host tools; this package provides none of those services and requires no API key configuration. Missing tools must be reported as evidence limitations. Full analysis behavior across hosts has not been tested.

The arithmetic helper uses only Python's standard library. Its CLI and representative numeric boundaries were checked with Python 3.13; other Python versions were not verified during this packaging work.

```bash
python scripts/compute_gains.py --help
python scripts/compute_gains.py --example
python scripts/compute_gains.py INPUT.json --output OUTPUT.json
```

The helper cannot authenticate sources, establish protocol equivalence, or certify causality. `rankable` only means declared inputs passed arithmetic checks. Research is read-only by default; installing dependencies, executing paper-repository code, training, or modifying projects requires separate authorization.

## Snapshot and license

This snapshot was supplied by the user on 2026-10-29. All nine original files are byte-identical; publication documentation is added separately. See `SOURCE_MANIFEST.json`. No upstream version number was supplied.

This project is licensed under the [MIT License](LICENSE), with copyright attributed to `arthas-sws`. Use, modification, redistribution, and commercial use are permitted with preservation of the copyright and license notice. Papers, analyzed repositories, and host tools retain their own terms.
