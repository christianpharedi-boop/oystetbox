# Experiment 0.2 reconciliation-only pass

## Purpose

This phase resolves dataset identity and cohort provenance before any OysterBox score is computed. It is not a benchmark run and does not rank proteins.

The pass may inspect official metadata, file manifests, subject/sample identifiers, acquisition timestamps, and checksums. It must not inspect validation biological measurements or outcome labels.

## Required quantities

The reconciliation record must keep the following quantities separate:

| Quantity | Meaning |
|---|---|
| `N_reported_discovery` | Counts stated in publication or repository prose. |
| `N_identifiable_discovery` | Unique discovery subjects recoverable from authoritative manifests. |
| `N_discovery_in_acquired_artifact` | Unique discovery subjects represented in the acquired artifact set. |
| `N_reported_validation` | Counts stated for the validation cohort. |
| `N_identifiable_validation` | Unique validation subjects recoverable from metadata without opening outcomes. |
| `N_validation_in_acquired_artifact` | Unique validation subjects represented in the acquired validation artifact. |
| `intersection` | Normalized subject IDs appearing in both manifests. |

The 66-versus-67 discrepancy must not be resolved by majority vote or by selecting the more convenient number. It remains blocked until the evidence explains the difference.

## Unit-of-analysis decision rule

Before assigning a reconciled count, the audit must identify whether each number refers to subjects, samples, enrolled individuals, measured individuals, retained individuals, or another inclusion stage. The record must preserve `N_reported`, `N_identifiable`, and `N_in_acquired_artifact` separately for both discovery and validation. A count may not be promoted from reported to reconciled merely because it appears in a publication or because it matches a partial acquired artifact.

## File-role rule

Every file in the official inventory receives a record containing its source, role, role evidence, acquisition date, PRIDE checksum, local SHA-256 when acquired, and outcome-inspection state. Filename-only role assignment is insufficient for admission. The current record intentionally leaves 97 files unclassified and marks three files as validation candidates only.

## Sealing rule

Subject identifiers and manifest metadata may be reconciled separately from validation measurements. The validation outcome artifact remains sealed, and `outcome_contents_exposed_to_scoring` must remain false.

## Exit conditions

The reconciliation phase exits only when the discovery and validation subject manifests are hashed, the intersection is calculated, the 66-versus-67 discrepancy is explained, and the file-role evidence supports complete discovery and validation artifact definitions. Until then, the information boundary is not frozen, Benchmark v1 is not frozen, and scoring remains blocked.

## Candidate-exhaustion rule

If no authoritative participant-level mapping source is identified after the predefined evidence search, the candidate is excluded from Benchmark v1 and retained as a documented provenance-failure case. This is not a scientific-failure judgment, and performance must not be inspected or used to justify the exclusion. The candidate may be reopened only if new authoritative participant-level evidence appears.

For PXD007535, the formal closure status is `NEEDS_CLARIFICATION` with `benchmark_eligibility: BLOCKED`, `scientific_failure: false`, and `provenance_sufficiency: INSUFFICIENT`. The next candidate must be selected independently of OysterBox performance.
