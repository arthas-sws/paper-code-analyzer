#!/usr/bin/env python3
"""Evidence-aware, descriptive arithmetic; never authenticates sources or proves causality.

Reads one JSON file; emits JSON to stdout or an explicit --output file. No network,
unit conversions, baseline normalization, aggregation, or two-point BD-rate estimates.
Use --example for the complete input schema. Missing metadata blocks headline gains.
"""
import argparse
import json
import math
from pathlib import Path
import sys

KINDS = {"psnr_db", "ssim", "latency", "bytes", "fps", "other", "bd_rate"}
UNITS = {
    "psnr_db": {"dB"}, "ssim": {"1", "unitless", "dimensionless"},
    "latency": {"s", "ms", "us", "µs", "ns"},
    "bytes": {"B", "bytes", "kB", "KB", "MB", "GB", "TB", "KiB", "MiB", "GiB", "TiB"},
    "fps": {"fps", "frames/s"},
}
BASES = {"reported_whole_model", "reported_ablation", "reproduced", "mechanism_only"}
EXAMPLE = {"comparisons": [{
    "id": "latency-example", "metric": "inference latency", "metric_kind": "latency",
    "baseline": {"value": 20, "unit": "ms", "source": "table 2, baseline row", "value_basis": "actual"},
    "candidate": {"value": 15, "unit": "ms", "source": "table 2, candidate row", "value_basis": "actual"},
    "direction": "lower", "protocol_comparable": True,
    "evidence_basis": "reported_ablation", "changed_factors": ["module X"], "confounds": []
}]}


def numeric(value):
    try:
        return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)
    except OverflowError:
        return False


def inspect(record):
    """Return one report; invalid records remain visible rather than being dropped."""
    flags = []
    out = {"original": record, "flags": flags, "rankable": False, "gains": None,
           "attribution": {"causality_certified": False,
                           "note": "Insufficient evidence metadata; no module-level causal credit."}}
    if not isinstance(record, dict):
        flags.append("record_not_object")
        return out
    for key in ("id", "metric"):
        if not isinstance(record.get(key), str) or not record[key].strip():
            flags.append("missing_or_invalid_" + key)
    kind = record.get("metric_kind")
    if not isinstance(kind, str) or kind not in KINDS:
        flags.append("missing_or_invalid_metric_kind")
        kind = None
    direction = record.get("direction")
    if direction not in ("higher", "lower"):
        flags.append("missing_or_invalid_direction")
    expected = {"psnr_db": "higher", "ssim": "higher", "latency": "lower", "bytes": "lower", "fps": "higher"}.get(kind) if isinstance(kind, str) else None
    if expected and direction in ("higher", "lower") and direction != expected:
        flags.append("direction_conflicts_with_metric_kind")
    protocol = record.get("protocol_comparable")
    if not isinstance(protocol, bool):
        flags.append("missing_or_invalid_protocol_comparable")
    elif not protocol:
        flags.append("protocol_not_comparable")
    evidence = record.get("evidence_basis")
    if not isinstance(evidence, str) or evidence not in BASES:
        flags.append("missing_or_invalid_evidence_basis")
        evidence = None
    if evidence == "mechanism_only":
        flags.append("mechanism_only_not_empirical_gain_evidence")
    for key in ("changed_factors", "confounds"):
        value = record.get(key)
        if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
            flags.append("missing_or_invalid_" + key)
    measurements = []
    for side in ("baseline", "candidate"):
        value = record.get(side)
        if not isinstance(value, dict):
            flags.append("missing_or_invalid_" + side)
            measurements.append({})
            continue
        measurements.append(value)
        if not numeric(value.get("value")):
            flags.append(side + "_value_missing_or_nonfinite_or_nonnumeric")
        for key in ("unit", "source"):
            if not isinstance(value.get(key), str) or not value[key].strip():
                flags.append(side + "_missing_or_invalid_" + key)
        if value.get("value_basis") not in ("actual", "normalized"):
            flags.append(side + "_missing_or_invalid_value_basis")
    baseline, candidate = measurements
    if baseline.get("unit") != candidate.get("unit"):
        flags.append("unit_mismatch_no_conversion")
    if baseline.get("value_basis") != candidate.get("value_basis"):
        flags.append("actual_normalized_basis_mismatch")
    if kind in UNITS:
        for side, measurement in (("baseline", baseline), ("candidate", candidate)):
            unit = measurement.get("unit")
            if not isinstance(unit, str) or unit not in UNITS[kind]:
                flags.append(side + "_unit_not_supported_for_metric_kind")
    if kind == "bd_rate":
        flags.append("bd_rate_requires_rate_distortion_curves_not_two_values")
    b, c = baseline.get("value"), candidate.get("value")
    if numeric(b) and numeric(c):
        if kind in ("latency", "bytes", "fps") and (b <= 0 or c <= 0):
            flags.append("ratio_requires_strictly_positive_values")
        if kind == "ssim" and not (-1 <= b <= 1 and -1 <= c <= 1):
            flags.append("ssim_outside_minus_one_to_one")
    factors, confounds = record.get("changed_factors"), record.get("confounds")
    if isinstance(confounds, list) and confounds:
        flags.append("declared_confounds_preclude_ranking")
    if isinstance(factors, list) and isinstance(confounds, list):
        potentially_eligible = (not flags and evidence in ("reported_ablation", "reproduced") and len(factors) == 1 and not confounds)
        out["attribution"] = {
            "causality_certified": False,
            "potentially_eligible_for_module_attribution_review": potentially_eligible,
            "note": ("One declared changed factor and no declared confounds; inspect controls, source, and protocol before any module attribution. This is not causal certification."
                     if potentially_eligible else "Descriptive comparison only; evidence/changed factors/confounds do not establish isolated module credit.")}
    if flags:
        return out
    delta = c - b
    gains = {"candidate_minus_baseline": delta,
             "direction_adjusted_improvement": delta if direction == "higher" else -delta,
             "unit": baseline["unit"], "value_basis": baseline["value_basis"],
             "baseline_input_value": b,
             "baseline_is_input_not_renormalized": True}
    if kind in ("latency", "bytes"):
        gains["cost_reduction_percent"] = (b - c) / b * 100
        gains["baseline_over_candidate_ratio"] = b / c
        if kind == "latency":
            gains["speedup"] = b / c
    elif kind == "fps":
        gains["throughput_increase_percent"] = (c - b) / b * 100
        gains["candidate_over_baseline_ratio"] = c / b
    if any(not numeric(v) for v in gains.values() if isinstance(v, (float, int)) and not isinstance(v, bool)):
        flags.append("arithmetic_result_nonfinite")
        out["attribution"]["potentially_eligible_for_module_attribution_review"] = False
        return out
    out.update(rankable=True, gains=gains)
    return out


def analyze(data):
    if not isinstance(data, dict) or not isinstance(data.get("comparisons"), list):
        raise ValueError('input must be an object with a "comparisons" list')
    return {"schema_version": 1,
            "limitations": "Rankable means arithmetically comparable under declared metadata only. Sources, protocol claims, authenticity, novelty, statistical significance and causality are not validated. Never sum gains across comparisons.",
            "comparisons": [inspect(row) for row in data["comparisons"]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="Input JSON file (never modified)")
    parser.add_argument("--output", help="Explicit output JSON path; replaces that file if it exists")
    parser.add_argument("--example", action="store_true", help="Print complete example input and exit")
    args = parser.parse_args()
    if args.example:
        print(json.dumps(EXAMPLE, indent=2))
        return 0
    if not args.input:
        parser.error("input is required unless --example is used")
    try:
        if args.output and (Path(args.output).resolve() == Path(args.input).resolve() or
                            (Path(args.output).exists() and Path(args.input).samefile(args.output))):
            raise ValueError("output must not overwrite the input file")
        def reject_constant(value):
            raise ValueError("nonstandard JSON numeric constant: " + value)
        def finite_float(value):
            parsed = float(value)
            if not math.isfinite(parsed):
                raise ValueError("JSON number exceeds finite floating-point range: " + value)
            return parsed
        data = json.loads(Path(args.input).read_text(encoding="utf-8"), parse_constant=reject_constant, parse_float=finite_float)
        result = analyze(data)
        rendered = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except (OSError, ValueError, OverflowError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
