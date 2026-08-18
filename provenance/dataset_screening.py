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
    "decision_basis",
    "reviewer_rationale",
)

AUDIT_REQUIRED_GATES = (
    "dataset_identity",
    "publication_license",
    "dataset_license",
    "discovery_artifact",
    "discovery_cutoff",
    "validation_source",
    "candidate_lineage",
    "cohort_independence",
    "identifier_mapping",
    "metadata_completeness",
    "processing_provenance",
    "validation_artifact",
    "validation_outcome_separation",
    "leakage_control",
    "artifact_hashes",
)

DECISION_BASIS_FIELDS = (
    "dataset_license",
    "discovery_artifact",
    "validation_artifact",
    "cutoff",
    "candidate_lineage",
    "cohort_independence",
    "identifier_mapping",
    "metadata_completeness",
    "validation_outcome_separation",
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
    basis = candidate.get("decision_basis")
    if not isinstance(basis, Mapping):
        errors.append("decision_basis must be a mapping")
    else:
        for field in DECISION_BASIS_FIELDS:
            if not basis.get(field):
                errors.append(f"missing decision-basis field: {field}")
    return errors


def validate_audit(audit: Mapping[str, object]) -> list[str]:
    """Return audit errors; unresolved gates prevent benchmark admission."""
    errors = []
    if audit.get("decision") != "NEEDS_CLARIFICATION":
        errors.append("PXD007535 audit decision must remain NEEDS_CLARIFICATION until all gates pass")
    if audit.get("scoring_allowed") is not False:
        errors.append("scoring_allowed must remain false while audit gates are unresolved")
    gates = audit.get("gates")
    if not isinstance(gates, Mapping):
        return errors + ["audit gates must be a mapping"]
    for gate in AUDIT_REQUIRED_GATES:
        if gate not in gates:
            errors.append(f"missing audit gate: {gate}")
        elif gates[gate].get("status") != "PASS":
            errors.append(f"unresolved audit gate: {gate}")
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
