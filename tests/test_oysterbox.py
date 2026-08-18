import csv
import hashlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from admission.admit import admit_dataset
from analysis.findings import protein_findings
from ingestion.proteomics_csv import parse_csv
from integrity.hash_file import sha256_file
from quality.qc import protein_qc_counts, qc_pass_rate
from scoring.validation_readiness import DIMENSIONS, validation_readiness
from provenance.dataset_screening import score_eligibility, validate_acquisition_state, validate_audit


class OysterBoxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = ROOT / "proteomics/dataset/fixture.csv"
        cls.measurements = parse_csv(cls.dataset)

    def test_frozen_specification_and_derivation_record_exist(self):
        spec = (ROOT / "docs/OYSTERBOX_EXPERIMENT_0.1.md").read_text(encoding="utf-8")
        derivation = (ROOT / "provenance/CORESIGNAL_DERIVATION.md").read_text(encoding="utf-8")
        self.assertIn("OysterBox Experiment 0.1", spec)
        self.assertIn("c29254c483b5cb0d5bcaea86c3e47b7eb727ff15", derivation)
        self.assertIn("original Git history is retained", derivation)

    def test_baseline_record_matches_fixture_and_declared_commit(self):
        baseline = (ROOT / "provenance/OYSTERBOX_0.1_BASELINE.yaml").read_text(encoding="utf-8")
        digest = hashlib.sha256(self.dataset.read_bytes()).hexdigest()
        self.assertIn("status: frozen_engineering_baseline", baseline)
        self.assertIn("baseline_commit: df9c14ada1013a7c6b2e2a73df7ba57893a640cc", baseline)
        self.assertIn(f"sha256: {digest}", baseline)
        self.assertIn("weights_frozen: true", baseline)

    def test_experiment_0_2_protocol_has_leakage_controls_and_baselines(self):
        protocol = (ROOT / "docs/OYSTERBOX_EXPERIMENT_0.2.md").read_text(encoding="utf-8")
        for required in [
            "Primary validation outcome",
            "Information boundary and leakage policy",
            "before the validation-outcome file is made available",
            "study-grouped AUROC",
            "AUPRC",
            "measurement quality alone",
            "No weight tuning",
            "missing outcomes",
            "would not establish clinical utility",
        ]:
            self.assertIn(required, protocol)

    def test_dataset_screening_gate_blocks_unfrozen_or_nonincluded_candidates(self):
        base = {
            "dataset_identifier": "example",
            "source": "public repository",
            "publication_license": "permitted",
            "dataset_license_status": "VERIFIED",
            "acquisition_date": "2026-01-01",
            "discovery_evidence": "discovery file",
            "discovery_cutoff": "2025-01-01",
            "validation_source": "independent assay",
            "validation_assay_type": "TARGETED_SRM",
            "validation_publication_date": "2026-01-02",
            "discovery_cohort_description": "discovery cohort",
            "validation_cohort_description": "independent cohort",
            "cohort_overlap_status": "NONE",
            "candidate_selection_provenance": "discovery-derived",
            "candidate_outcome_artifact": "separate outcome file",
            "identifier_mapping": "UniProt release",
            "sample_metadata_completeness": "complete",
            "processing_provenance_completeness": "complete",
            "independent_validation_status": "independent",
            "leakage_assessment": "passed",
            "redistribution_or_hash_status": "hashed",
            "decision": "INCLUDE",
            "screening_status": "FINAL_INCLUDED",
            "decision_basis": {
                "dataset_license": "VERIFIED",
                "discovery_artifact": "HASHED",
                "validation_artifact": "HASHED",
                "cutoff": "FROZEN",
                "candidate_lineage": "VERIFIED",
                "cohort_independence": "VERIFIED",
                "identifier_mapping": "VERIFIED",
                "metadata_completeness": "VERIFIED",
                "validation_outcome_separation": "VERIFIED",
            },
            "reviewer_rationale": "screened independently",
            "acquisition_manifest_sha256": "a" * 64,
            "validation_outcome_separation_sha256": "b" * 64,
        }
        self.assertTrue(score_eligibility(base).score_eligible)
        with self.assertRaises(ValueError):
            score_eligibility({**base, "decision": "NEEDS_CLARIFICATION"})
        with self.assertRaises(ValueError):
            score_eligibility({key: value for key, value in base.items() if key != "discovery_cutoff"})
        with self.assertRaises(ValueError):
            score_eligibility({**base, "decision_basis": {"dataset_license": "VERIFIED"}})

    def test_pxd007535_is_provisional_and_unscored(self):
        candidate = (ROOT / "experiments/0.2/dataset_candidates/PXD007535.yaml").read_text(encoding="utf-8")
        decision = (ROOT / "experiments/0.2/decisions/PXD007535.yaml").read_text(encoding="utf-8")
        ledger = (ROOT / "provenance/DATASET_SCREENING_0.2.yaml").read_text(encoding="utf-8")
        self.assertIn("decision: NEEDS_CLARIFICATION", candidate)
        self.assertIn("screening_status: PROVISIONAL_CANDIDATE", candidate)
        self.assertIn("dataset_license_status: PARTIALLY_RESOLVED", candidate)
        self.assertIn("performance_inspected: false", decision)
        self.assertIn("outcome_labels_exposed_to_oysterbox: false", decision)
        self.assertIn("eligible_for_scoring: false", ledger)
        self.assertIn("scoring_permitted: false", ledger)
        benchmark = (ROOT / "provenance/EXPERIMENT_0.2_BENCHMARK_v1.yaml").read_text(encoding="utf-8")
        self.assertIn("status: NOT_FROZEN", benchmark)
        self.assertIn("selected_dataset: null", benchmark)
        self.assertIn("validation_artifact_visible_to_scoring: false", benchmark)

    def test_pxd007535_audit_is_complete_but_blocked(self):
        import re
        audit_text = (ROOT / "experiments/0.2/decisions/PXD007535_AUDIT.yaml").read_text(encoding="utf-8")
        self.assertIn("audit_status: COMPLETE_WITH_UNRESOLVED_GATES", audit_text)
        self.assertIn("decision: NEEDS_CLARIFICATION", audit_text)
        self.assertIn("scoring_allowed: false", audit_text)
        self.assertIn("dataset_license:\n    status: PARTIALLY_RESOLVED", audit_text)
        self.assertIn("discovery_artifact:\n    status: PENDING_HASH", audit_text)
        self.assertIn("validation_outcome_separation:\n    status: PENDING", audit_text)
        self.assertIn("next_operations:", audit_text)

        # The audit validator is exercised with the unresolved state represented explicitly.
        audit = {"decision": "NEEDS_CLARIFICATION", "scoring_allowed": False, "gates": {
            "dataset_identity": {"status": "PASS"},
            "publication_license": {"status": "PASS"},
            "dataset_license": {"status": "UNVERIFIED"},
        }}
        errors = validate_audit(audit)
        self.assertTrue(any("dataset_license" in error for error in errors))
        self.assertTrue(any("missing audit gate" in error for error in errors))

    def test_acquisition_and_exposure_boundary_remains_blocked(self):
        discovery = {"status": "NOT_ACQUIRED", "manifest_sha256": None}
        validation = {"status": "NOT_ACQUIRED", "manifest_sha256": None}
        boundary = {"status": "NOT_FROZEN", "discovery_cutoff": None, "validation_artifact_contents_visible_to_scoring": False}
        sealed = {"exposure_state": "SEALED", "outcome_contents_available_to_scoring": False, "prediction_artifact_sha256_required_before_release": True}
        errors = validate_acquisition_state(discovery, validation, boundary, sealed)
        self.assertTrue(any("discovery artifact is not acquired" in error for error in errors))
        self.assertTrue(any("information boundary is not frozen" in error for error in errors))

        released = {**sealed, "exposure_state": "RELEASED"}
        errors = validate_acquisition_state({"status": "ACQUIRED", "manifest_sha256": "d" * 64}, {"status": "SEALED", "manifest_sha256": "v" * 64}, {"status": "FROZEN", "discovery_cutoff": "2018-04-02", "validation_artifact_contents_visible_to_scoring": False}, released)
        self.assertTrue(any("validation outcomes are not sealed" in error for error in errors))

    def test_partial_pxd007535_acquisition_is_recorded_but_blocked(self):
        discovery = (ROOT / "experiments/0.2/acquisition/PXD007535_discovery_manifest.yaml").read_text(encoding="utf-8")
        validation = (ROOT / "experiments/0.2/acquisition/PXD007535_validation_manifest.yaml").read_text(encoding="utf-8")
        sealed = (ROOT / "experiments/0.2/validation_outcomes/PXD007535_SEALED_OUTCOME_ARTIFACT.yaml").read_text(encoding="utf-8")
        source_notes = (ROOT / "acquisition/manifests/PXD007535_source_notes.md").read_text(encoding="utf-8")
        self.assertIn("status: PARTIALLY_ACQUIRED", discovery)
        self.assertIn("cc6a705d3059335c92d5f91a910aaa36f9f4d1f40adccec2c415c973f3f5cbb6", discovery)
        self.assertIn("status: PARTIALLY_ACQUIRED", validation)
        self.assertIn("f07c71858713af7e8d1e67e4c899525a13e33935fc0261a1d2c5ca7ca4c5b264", validation)
        self.assertIn("outcome_contents_exposed_to_scoring: false", validation)
        self.assertIn("exposure_state: SEALED", sealed)
        self.assertIn("outcome_contents_available_to_scoring: false", sealed)
        self.assertIn("have not been acquired", source_notes.lower())

    def test_targeted_audit_gates_remain_explicitly_blocked(self):
        licensing = (ROOT / "acquisition/manifests/PXD007535_licensing_evidence.md").read_text(encoding="utf-8")
        artifact_sets = (ROOT / "experiments/0.2/acquisition/PXD007535_artifact_set_definition.yaml").read_text(encoding="utf-8")
        cohorts = (ROOT / "experiments/0.2/acquisition/PXD007535_cohort_reconciliation.yaml").read_text(encoding="utf-8")
        boundary = (ROOT / "experiments/0.2/acquisition/PXD007535_information_boundary.yaml").read_text(encoding="utf-8")
        self.assertIn("PRE_JUNE_2018_EMBL_EBI_TERMS_OF_USE", licensing)
        self.assertIn("original_data_owner_restrictions: NOT_VERIFIED", licensing)
        self.assertIn("status: PENDING_CLASSIFICATION", artifact_sets)
        self.assertIn("candidate_validation_files_by_filename: 3", artifact_sets)
        self.assertIn("status: BLOCKED_CONFLICTING_REPORTED_COUNTS", cohorts)
        self.assertIn("count: 66", cohorts)
        self.assertIn("count: 67", cohorts)
        self.assertIn("overlap_status: UNKNOWN", cohorts)
        self.assertIn("status: NOT_FROZEN", boundary)
        self.assertIn("validation_artifact_contents_visible_to_scoring: false", boundary)

    def test_parser_and_quality_gate(self):
        self.assertEqual(len(self.measurements), 6)
        self.assertAlmostEqual(qc_pass_rate(self.measurements), 5 / 6)
        self.assertEqual(protein_qc_counts(self.measurements), {"P001": 3, "P002": 2})

    def test_integrity_and_admission(self):
        digest = sha256_file(self.dataset)
        record = admit_dataset(self.dataset, self.measurements, digest)
        self.assertTrue(record["admitted"])
        with self.assertRaises(ValueError):
            admit_dataset(self.dataset, self.measurements, "0" * 64)

    def test_findings_have_evidence_chain(self):
        findings = protein_findings(self.measurements)
        self.assertEqual([item["protein_id"] for item in findings], ["P001", "P002"])
        for finding in findings:
            self.assertGreaterEqual(len(finding["evidence_chain"]), 2)

    def test_transparent_score(self):
        dimensions = {name: 0.8 for name in DIMENSIONS}
        result = validation_readiness(dimensions)
        self.assertAlmostEqual(result.score, 0.8)
        with self.assertRaises(ValueError):
            validation_readiness({name: 0.5 for name in DIMENSIONS if name != "independent_evidence"})
        with self.assertRaises(ValueError):
            validation_readiness({**dimensions, "statistical_strength": 1.1})


if __name__ == "__main__":
    unittest.main()
