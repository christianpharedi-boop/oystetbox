"""Transparent validation-readiness scoring for OysterBox Experiment 0.1."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping

DIMENSIONS = ("measurement_quality", "reproducibility", "statistical_strength", "biological_coherence", "independent_evidence", "provenance_completeness")

@dataclass(frozen=True)
class ReadinessScore:
    dimensions: Mapping[str, float]
    score: float


def validation_readiness(dimensions: Mapping[str, float]) -> ReadinessScore:
    missing = [name for name in DIMENSIONS if name not in dimensions]
    if missing:
        raise ValueError(f"missing scoring dimensions: {', '.join(missing)}")
    values = [float(dimensions[name]) for name in DIMENSIONS]
    if any(value < 0 or value > 1 for value in values):
        raise ValueError("all scoring dimensions must be between 0 and 1")
    return ReadinessScore(dict(dimensions), sum(values) / len(values))

if __name__ == "__main__":
    example = {name: 0.8 for name in DIMENSIONS}
    result = validation_readiness(example)
    print(f"validation_readiness={result.score:.3f}")
