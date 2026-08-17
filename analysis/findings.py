"""Construct auditable protein-level findings from admitted measurements."""
from collections import defaultdict
from ingestion.proteomics_csv import Measurement
from quality.qc import protein_qc_counts

def protein_findings(measurements: list[Measurement]) -> list[dict]:
    grouped: dict[str, list[Measurement]] = defaultdict(list)
    for item in measurements:
        grouped[item.protein_id].append(item)
    counts = protein_qc_counts(measurements)
    findings = []
    for protein_id, items in sorted(grouped.items()):
        passing = [item for item in items if item.qc_pass]
        if not passing:
            continue
        findings.append({"protein_id": protein_id, "qc_pass_samples": counts[protein_id], "mean_intensity": sum(i.intensity for i in passing) / len(passing), "evidence_chain": ["dataset:fixture", f"protein:{protein_id}"]})
    return findings
