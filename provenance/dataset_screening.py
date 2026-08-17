"""Governance checks for the Experiment 0.2 dataset-scoring boundary."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping

REQUIRED_FIELDS = (
    "dataset_identifier",
    "source",
    "publication_license",
    "dataset_license_status",
    "acquisition_date",
    "discovery_evidence",
    "discovery_cutoff",
    "validation_source",
    "validation_assay_type",
    "validation_publication_date",
    "discovery_cohort_description",
    "validation_cohort_description",
    "cohort_overlap_status",
    "candidate_selection_provenance",
    "candidate_outcome_artifact",
    "identifier_mapping",
    "sample_metadata_completeness",
    "processing_provenance_completeness",
    "independent_validation_status",
    "leakage_assessment",
    "redistribution_or_hash_status",
    "decision",
    "screening_status",
    "reviewer_rationale",
)

FROZEN_FIELDS = (
    "dataset_identifier",
    "discovery_cutoff",
    "acquisition_manifest_sha256",
    "validation_outcome_separation_sha256",
    "decision",
)

@dataclass(frozen=True)
class ScreeningDecision:
    dataset_identifier: str
    decision: str
    score_eligible: bool


def validate_candidate(candidate: Mapping[str, object]) -> list[str]:
    errors = []
    for field in REQUIRED_FIELDS:
        value = candidate.get(field)
        if value is None or value == "":
            errors.append(f"missing required field: {field}")
    if candidate.get("decision") not in {"INCLUDE", "EXCLUDE", "NEEDS_CLARIFICATION"}:
        errors.append("decision must be INCLUDE, EXCLUDE, or NEEDS_CLARIFICATION")
    return errors


def score_eligibility(candidate: Mapping[str, object]) -> ScreeningDecision:
    errors = validate_candidate(candidate)
    if errors:
        raise ValueError("dataset screening is incomplete: " + "; ".join(errors))
    missing_frozen = [field for field in FROZEN_FIELDS if not candidate.get(field)]
    if missing_frozen:
        raise ValueError("dataset scoring is blocked; unfrozen fields: " + ", ".join(missing_frozen))
    if candidate["decision"] != "INCLUDE":
        raise ValueError(f"dataset scoring is blocked by decision: {candidate['decision']}")
    return ScreeningDecision(str(candidate["dataset_identifier"]), "INCLUDE", True)
