"""Proteomics quality gate primitives."""
from __future__ import annotations
from collections import defaultdict
from ingestion.proteomics_csv import Measurement

def qc_pass_rate(measurements: list[Measurement]) -> float:
    if not measurements:
        raise ValueError("quality gate requires at least one measurement")
    return sum(item.qc_pass for item in measurements) / len(measurements)

def protein_qc_counts(measurements: list[Measurement]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for item in measurements:
        if item.qc_pass:
            counts[item.protein_id] += 1
    return dict(counts)
