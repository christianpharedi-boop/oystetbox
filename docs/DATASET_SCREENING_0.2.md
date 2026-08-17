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
| License | License or documented permission for experimental use |
| Acquisition date | Date acquired by OysterBox and source release date where available |
| Discovery evidence | Evidence available to the discovery-stage analysis |
| Discovery cutoff | Fixed date for information permitted to scoring |
| Validation source | Independent assay, cohort, or other prespecified source |
| Validation-publication date | Date validation evidence became publicly available |
| Identifier mapping | Protein/peptide mapping method, version, and unresolved count |
| Sample metadata | Completeness of sample, study, batch, and experiment metadata |
| Processing provenance | Raw/processed files, software, parameters, and checksums |
| Independent validation | Whether samples, assay, cohort, and evidence are independent |
| Leakage assessment | Post-cutoff information and contamination review |
| Redistribution/hash status | Permission to store files or immutable checksums |
| Decision | `INCLUDE`, `EXCLUDE`, or `NEEDS_CLARIFICATION` |
| Reviewer rationale | Reproducible explanation for the decision |

## Decision procedure

Screen candidates using only the frozen criteria. Record evidence URLs, acquisition timestamps, file hashes, and unresolved questions in `provenance/DATASET_SCREENING_0.2.yaml` and candidate-specific records under `experiments/0.2/dataset_candidates/`.

A candidate may be marked `INCLUDE` only after the dataset identity, discovery cutoff, acquisition manifest checksum, validation-outcome separation checksum, and decision are frozen. `EXCLUDE` and `NEEDS_CLARIFICATION` candidates are never passed to scoring.

After all screening decisions are committed, the included dataset may be acquired and scored using the frozen OysterBox 0.1 rubric. Validation outcomes remain in a separate controlled artifact until predictions are frozen and checksummed.

## Required pre-scoring invariant

> OysterBox cannot score a dataset until its dataset identity, discovery cutoff, acquisition manifest, validation-outcome separation, and screening decision are frozen.

The executable enforcement is implemented in `provenance/dataset_screening.py`. The v0.1 scoring rubric is not modified by this governance layer.

## Candidate status vocabulary

`INCLUDE` means the candidate satisfies the protocol and is eligible for later scoring. `EXCLUDE` means a protocol requirement fails or cannot be demonstrated. `NEEDS_CLARIFICATION` means the evidence is incomplete and no score may be generated.

## Outcome of the first run

The result will be classified as one of: an infeasible boundary, a reproducible evidence-chain demonstration, an exploratory discrimination result, or a justified larger-benchmark proposal. Even a strong exploratory result will not establish clinical utility, causal biological relevance, or general predictive validity.
