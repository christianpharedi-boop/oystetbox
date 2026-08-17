# OysterBox Experiment 0.1

## 1. Question

Can the CoreSignal scientific-trust architecture transfer to proteomics while preserving provenance, integrity, quality gating, admission controls, reproducibility, and an auditable evidence chain?

## 2. Reused components

The experiment reuses the architecture of dataset registration, provenance metadata, content hashing, deterministic validation, quality gates, admission records, experiment manifests, and evidence-chain records. The implementation is intentionally transparent and domain-agnostic wherever possible.

## 3. Removed Earth-specific components

Earth-rotation observations, station/archive retrieval, geomagnetic workflows, Earth-specific time-series forecasting, and related source packages are excluded. Their absence is a test condition, not a claim that the original science was invalid.

## 4. Dataset

Experiment 0.1 uses `proteomics/dataset/fixture.csv`, a synthetic long-format measurement fixture. A real dataset may replace it only after a new registry entry records source, license, acquisition parameters, raw-file checksum, and preprocessing rules.

## 5. Finding definition

A protein finding is a protein-level record with a non-empty identifier, a measured value, a quality-passing sample count, and an evidence reference. The fixture findings are software test objects, not biological findings.

## 6. Validation-readiness rubric

The score is the arithmetic mean of six independently recorded dimensions, each on [0, 1]: measurement quality, reproducibility, statistical strength, biological coherence, independent evidence, and provenance completeness. Missing dimensions are not silently imputed; the score is blocked until all required fields exist.

## 7. Successful validation

Success requires that a pre-registered finding meets the readiness threshold, survives an independently reproduced analysis, and is supported by evidence not used to tune the scoring rubric. Experiment 0.1 does not contain such an independent biological validation.

## 8. Forbidden information

The scoring engine must not see future validation outcomes, post hoc labels, external confirmation acquired after scoring, or analyst-written conclusions. It receives only the six rubric dimensions and their provenance metadata.

## 9. Evaluation metrics

Primary metrics are score reproducibility, missing-field detection, integrity-check sensitivity, and agreement between independently recomputed scores. Biological predictive performance is not estimable from the synthetic fixture.

## 10. Pass/fail criteria

The software experiment passes if the pipeline rejects incomplete or tampered inputs, produces the same score on repeated runs, and preserves an auditable finding-to-evidence chain. The scientific transfer remains inconclusive until a real, independently validated dataset is run.
