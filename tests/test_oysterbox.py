import csv
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
