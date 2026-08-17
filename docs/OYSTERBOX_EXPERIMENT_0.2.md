# OysterBox Experiment 0.2: Prospective validation-readiness benchmark

**Status:** protocol draft to be frozen before any benchmark outcomes are inspected.

## Scientific question

Can the frozen OysterBox 0.1 Validation Readiness Score rank proteomic findings by their likelihood of meeting a prespecified independent validation outcome, using only information available at the discovery-time cutoff?

This experiment evaluates predictive usefulness. It does not test whether OysterBox identifies biological importance, establishes causality, or replaces laboratory validation.

## Primary estimand and unit of analysis

The unit of analysis is one **protein finding within one discovery study**. The primary estimand is the probability that a finding meeting the primary validation definition is ranked above a finding that does not meet it, as summarized by AUROC at the finding level with study-grouped uncertainty intervals.

Proteins from the same study are not treated as independent observations for confidence intervals. The primary analysis groups resampling by study or cohort to avoid overstating precision.

## Primary validation outcome

A finding is a primary-positive only when, after the discovery cutoff, it receives an orthogonal confirmation using a prespecified assay or an independently collected cohort, with the protein identity and direction of effect recorded before outcome review. Publication-only support is not sufficient unless the protocol explicitly classifies it as a secondary outcome.

The outcome adjudication file must include the validation source, date, assay or cohort type, identity-matching method, direction agreement, and adjudicator decision. Ambiguous or unavailable outcomes remain missing and are not silently treated as negatives.

## Information boundary and leakage policy

The discovery cutoff is a fixed date and must be recorded per dataset before scoring. OysterBox may use only discovery-stage measurements, QC metadata, provenance metadata, and evidence that was publicly available on or before that cutoff. The scoring process must not access later publications, later database annotations, validation labels, post-cutoff reanalyses, analyst conclusions, or any file containing the primary outcome.

Dataset acquisition, filtering, evidence mapping, and feature construction are logged with hashes. The prediction file is committed or archived with a checksum before the validation-outcome file is made available to the scoring process.

## Dataset inclusion criteria

A dataset must have a clear license or redistribution permission, identifiable study and sample metadata, a reproducible raw or normalized measurement source, a documented acquisition date or public-release date, and a feasible independent validation source. The benchmark cannot proceed if the discovery and validation evidence originate from the same samples or if the information boundary cannot be reconstructed.

Dataset selection criteria, exclusions, and the final list of studies must be recorded before performance results are calculated.

## Frozen score and prohibited tuning

Experiment 0.2 uses the OysterBox 0.1 rubric exactly as frozen in `provenance/OYSTERBOX_0.1_BASELINE.yaml`. The six dimensions remain equally weighted. No weight tuning, threshold tuning, feature addition, AI model, or outcome-informed redefinition is permitted during the primary analysis.

Biological coherence and independent evidence must be operationalized before scoring. If either field is assigned by human review, reviewers must be blinded to validation outcomes and the review instructions must be versioned.

## Prespecified comparators

The primary comparison is the complete frozen OysterBox score against simple baselines: measurement quality alone, reproducibility alone, provenance completeness alone, the unweighted mean of non-biological dimensions, and a prevalence-matched random ranking. These comparators determine whether the full architecture adds ranking value beyond one obvious quality signal.

## Metrics

The primary metric is study-grouped AUROC with a 95% confidence interval. Secondary metrics are AUPRC, precision among findings with score at least 0.70, validation-rate lift relative to the prevalence baseline, calibration by score bin, score distribution, and false-positive and false-negative patterns.

Ties, missing outcomes, duplicate protein-study records, and zero-positive or zero-negative study groups must be handled according to a locked analysis script. Confidence intervals use study-level bootstrap resampling with a recorded random seed; if the number of independent studies is too small, results are reported descriptively rather than assigned misleading intervals.

## Success and failure criteria

The primary result is considered supportive only if the frozen OysterBox score exceeds every prespecified simple baseline on the primary AUROC estimate, the 95% interval is reported, and the direction is consistent in a held-out study or cohort. A score that does not outperform the baselines is a valid negative result.

No commercial or biological claim may be made from Experiment 0.2 alone. A positive benchmark result would justify a separately designed resource-constrained validation experiment; it would not establish clinical utility or causal biological relevance.

## Required artifacts before outcome release

Before validation outcomes are exposed, the repository must contain the dataset registry, discovery cutoff records, acquisition and preprocessing manifests, feature-definition document, frozen prediction file and checksum, analysis-plan commit, comparator definitions, and a statement that no primary outcome labels were visible during scoring.

After outcome release, the outcome ledger, adjudication notes, analysis output, confidence intervals, and all deviations from this protocol must be added without rewriting the pre-outcome artifacts.

## Decision log

Experiment 0.2 is not considered started until this document, the dataset list, the primary outcome definition, and the analysis script are committed together. Any change afterward requires a new protocol version and must not overwrite the original plan.
