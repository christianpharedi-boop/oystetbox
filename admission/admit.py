"""Admission requires integrity and minimum quality evidence."""
from pathlib import Path
from integrity.hash_file import sha256_file
from quality.qc import qc_pass_rate
from ingestion.proteomics_csv import Measurement

def admit_dataset(path: Path, measurements: list[Measurement], expected_sha256: str, minimum_qc_rate: float = 0.5) -> dict:
    actual = sha256_file(path)
    if actual != expected_sha256:
        raise ValueError("dataset integrity check failed")
    rate = qc_pass_rate(measurements)
    if rate < minimum_qc_rate:
        raise ValueError("dataset quality gate failed")
    return {"path": str(path), "sha256": actual, "qc_pass_rate": rate, "admitted": True}
