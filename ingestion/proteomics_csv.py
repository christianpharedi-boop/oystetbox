"""Minimal deterministic parser for normalized proteomics measurements."""
from __future__ import annotations
import csv
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Measurement:
    protein_id: str
    sample_id: str
    intensity: float
    qc_pass: bool
    biological_evidence: float
    independent_evidence: float

def parse_csv(path: Path) -> list[Measurement]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        required = {"protein_id", "sample_id", "intensity", "qc_pass", "biological_evidence", "independent_evidence"}
        if set(rows.fieldnames or []) != required:
            raise ValueError("dataset columns do not match the frozen normalized schema")
        return [Measurement(row["protein_id"], row["sample_id"], float(row["intensity"]), bool(int(row["qc_pass"])), float(row["biological_evidence"]), float(row["independent_evidence"])) for row in rows]
