# Dataset Screening 0.2

**Experiment name:** OysterBox Experiment 0.2 — Exploratory Feasibility Benchmark  
**Status:** screening protocol frozen before any candidate is scored

> The dataset is selected independently of OysterBox's performance.

## Purpose

Dataset Screening 0.2 governs selection of a real proteomics discovery/validation dataset for the exploratory feasibility benchmark. It is a data-governance operation, not a performance optimization step. No candidate may be scored while its screening decision, discovery cutoff, acquisition provenance, or validation-outcome separation remains unfrozen.

The first run is explicitly exploratory. Its purpose is to determine whether a genuinely leakage-safe discovery/validation boundary can be constructed, whether the evidence chain can be reproduced from real proteomic material, whether the frozen score shows useful discrimination, and whether a larger prospective benchmark is justified. It is not a validation of OysterBox.

## Selection-independence rule

Candidate discovery, screening, inclusion, exclusion, and clarification decisions must be completed without inspecting OysterBox performance on those candidates. Screening records must be committed before any candidate enters the scoring pipeline. A candidate selected because it produces a favorable OysterBox result invalidates the primary benchmark.

## Candidate screening criteria

Each candidate must be assessed against the following criteria and supported by a source record or an explicit `NEEDS_CLARIFICATION` decision.

| Criterion | Required evidence |
|---|---|
| Dataset identifier | Stable accession, DOI, repository ID, or equivalent |
| Repository/source | Public source URL and acquisition route |
| Publication license | License attached to the paper or publication record |
| Dataset license | Dataset-level redistribution and experimental-use terms, recorded separately from publication licensing |
| Acquisition date | Date acquired by OysterBox and source release date where available |
| Discovery evidence | Evidence available to the discovery-stage analysis |
| Discovery cutoff | Fixed date for information permitted to scoring |
| Validation source | Independent assay, cohort, or other prespecified source |
| Validation assay type | Orthogonal assay, targeted PRM/SRM, independent cohort, or other prespecified category |
| Validation-publication date | Date validation evidence became publicly available |
| Cohort overlap | None, partial, unknown, or same cohort; overlap must not be hidden by the word independent |
| Candidate-selection provenance | Counts and lineage for discovery-derived, literature-derived, and housekeeping candidates |
| Candidate-outcome artifact | Separate artifact identity and checksum; it must remain unavailable to scoring |
| Identifier mapping | Protein/peptide mapping method, version, and unresolved count |
| Sample metadata | Completeness of sample, study, batch, and experiment metadata |
| Processing provenance | Raw/processed files, software, parameters, and checksums |
| Independent validation | Whether samples, assay, cohort, and evidence are independent |
| Leakage assessment | Post-cutoff information and contamination review |
| Redistribution/hash status | Permission to store files or immutable checksums |
| Decision | `INCLUDE`, `EXCLUDE`, or `NEEDS_CLARIFICATION` |
| Decision basis | Machine-readable status for license, artifacts, cutoff, lineage, independence, mapping, metadata, and outcome separation |
| Reviewer rationale | Reproducible explanation for the decision |

## Provenance-first Candidate #2 rule

Candidate #2 must be selected for evidence-chain quality before biological interest. The screening order is therefore: identity-chain completeness; explicit sample/subject mapping; discovery/validation cohort separation; public discovery and validation material; accessible supplementary metadata; unambiguous discovery and validation timing; sealable validation outcomes; processing completeness; identifier completeness; and licensing or access compatibility. Biological attractiveness, reported effect size, number of findings, and any OysterBox result are not selection criteria.

The preferred Candidate #2 is deliberately ordinary: a candidate that is less exciting scientifically but more auditable is ranked above a biologically attractive candidate with unresolved identity or cohort provenance. This ranking is applied before any candidate is scored and must be recorded as a screening decision, not inferred retrospectively from performance.

A publication or repository statement that a validation cohort is “independent” is a claim requiring verification, not an identity-graph PASS. OysterBox must establish the Run → Sample → Subject → Cohort edges and calculate the discovery/validation intersection from authoritative metadata before cohort independence can be marked verified.

## Candidate evidence-search budget

Each provisional candidate receives a finite evidence-search budget. The predefined routes are the ProteomeXchange and PRIDE metadata, submission XML, SDRF and sample routes; the publisher full text and supplementary metadata; and linked publication repository records. If authoritative participant-level mapping and cohort separation cannot be established within three search rounds, the candidate is marked `NEEDS_CLARIFICATION` or `EXCLUDE` and the process moves to the next candidate. Performance must never influence exhaustion or continuation decisions.

## Decision procedure

Screen candidates using only the frozen criteria. Record evidence URLs, acquisition timestamps, file hashes, and unresolved questions in `provenance/DATASET_SCREENING_0.2.yaml` and candidate-specific records under `experiments/0.2/dataset_candidates/`.

A candidate may be marked `INCLUDE` only after the dataset identity, discovery cutoff, acquisition manifest checksum, validation-outcome separation checksum, licensing status, candidate-selection lineage, cohort-overlap status, decision, and machine-readable `decision_basis` are frozen. A promising structural candidate may be recorded as `PROVISIONAL_CANDIDATE`, but it remains `NEEDS_CLARIFICATION` until those conditions are verified. `EXCLUDE` and `NEEDS_CLARIFICATION` candidates are never passed to scoring.

After all screening decisions are committed, the included dataset may be acquired and scored using the frozen OysterBox 0.1 rubric. Validation outcomes remain in a separate controlled artifact until predictions are frozen and checksummed.

## Experiment 0.2 Benchmark Dataset v1

Once one candidate satisfies every screening gate, create a separate immutable benchmark-freeze record in `provenance/EXPERIMENT_0.2_BENCHMARK_v1.yaml`. This transition ends dataset selection. The record must name the selected dataset, freeze the discovery and validation artifact hashes separately, preserve the discovery cutoff, and state that the validation artifact was unavailable to OysterBox during prediction.

After the benchmark is frozen, OysterBox receives only the discovery artifact. Predictions must be checksummed before the validation artifact is released. A benchmark freeze is not permitted merely because a candidate looks promising; it requires a new audited decision record changing `NEEDS_CLARIFICATION` to `INCLUDE`.

## Required pre-scoring invariant

> OysterBox cannot score a dataset until its dataset identity, discovery cutoff, acquisition manifest, validation-outcome separation, and screening decision are frozen.

The executable enforcement is implemented in `provenance/dataset_screening.py`. The v0.1 scoring rubric is not modified by this governance layer.

## Candidate status vocabulary

`INCLUDE` means the candidate satisfies the protocol and is eligible for later scoring. `EXCLUDE` means a protocol requirement fails or cannot be demonstrated. `NEEDS_CLARIFICATION` means the evidence is incomplete and no score may be generated.

## Evidence-acquisition order

Evidence acquisition remains separate from scoring. First acquire discovery material and record an immutable file manifest with path, size, source URL, acquisition timestamp, license status, and SHA-256. Acquire validation/SRM material separately with a different manifest and checksum. Then reconcile discovery and validation subjects, freeze the information boundary, freeze protein-to-gene-to-peptide-to-transition mappings, and freeze the instrument/software/parameter/database processing chain.

Validation outcomes may be possessed as a sealed artifact hash without exposing the outcome file to OysterBox. Acquisition and exposure are different operations. The outcome file can be released only after the prediction artifact has been frozen and checksummed, and the release authorization has been recorded.

The current PXD007535 acquisition templates are under `experiments/0.2/acquisition/`; the sealed-outcome contract is under `experiments/0.2/validation_outcomes/`. All templates remain intentionally incomplete, so scoring remains blocked.

## Outcome of the first run

The result will be classified as one of: an infeasible boundary, a reproducible evidence-chain demonstration, an exploratory discrimination result, or a justified larger-benchmark proposal. Even a strong exploratory result will not establish clinical utility, causal biological relevance, or general predictive validity.
