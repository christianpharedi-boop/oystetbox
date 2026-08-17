# OysterBox

OysterBox is a clean experimental repository implementing and testing a minimal proteomics-oriented adaptation of the provenance-first scientific-trust architecture developed in [CoreSignal](https://github.com/christianpharedi-boop/coresignal).

> Can a provenance, integrity, quality, admission, analysis, and evidence-chain architecture survive transplantation into molecular science without being redesigned around the new results?

This repository is intentionally an **engineering sandbox**, not a claim that the architecture has been scientifically validated or that any protein finding is biologically important. It begins with a frozen specification, transparent scoring, deterministic tests, and an explicit record of which CoreSignal invariants are reused and which Earth-specific modules are removed.

## Status

OysterBox Experiment 0.1 is a **frozen engineering baseline**. It demonstrates deterministic ingestion, integrity checking, QC, admission, finding construction, evidence-chain recording, and transparent scoring on a small synthetic fixture. It does not establish real-world predictive validity. Experiment 0.2 defines the preregistered, leakage-safe benchmark required before predictive claims can be assessed.

## Architecture transfer

| CoreSignal concept | OysterBox adaptation |
|---|---|
| Dataset provenance | Sample and data provenance |
| Acquisition | Dataset acquisition |
| Hashing | Raw proteomics file hashing |
| Parsing | Proteomics metadata and measurement parsing |
| Quality gate | Proteomics QC gate |
| Admission | Admission into the experiment |
| Scientific computation | Proteomic analysis |
| Result | Protein finding |
| Evidence chain | Finding-to-evidence chain |

The implementation deliberately keeps the architecture small. It does not import Earth-rotation semantics, station logic, geomagnetic models, or domain-specific forecasting into the proteomics experiment. The result should be described as an architectural adaptation that passed engineering tests, not as proof that the original scientific architecture has already transferred successfully.

## Run

```bash
python3 -m unittest discover -s tests -v
python3 scoring/validation_readiness.py
```

The score is transparent and bounded between 0 and 1. It is a readiness indicator, not a probability of biological truth. The v0.1 rubric is frozen; it must not be tuned using future validation outcomes. Dataset selection is governed separately by `docs/DATASET_SCREENING_0.2.md`, and no candidate may be scored until its screening decision and provenance artifacts are frozen.

## Provenance

OysterBox derives its initial architecture from CoreSignal commit `c29254c483b5cb0d5bcaea86c3e47b7eb727ff15` (2026-08-17). The v0.1 baseline is frozen at commit `df9c14ada1013a7c6b2e2a73df7ba57893a640cc`; its fixture checksum and rubric are recorded in `provenance/OYSTERBOX_0.1_BASELINE.yaml`. The source history is retained in this repository, and the transfer is documented in `provenance/CORESIGNAL_DERIVATION.md`. Experiment 0.2 is specified in `docs/OYSTERBOX_EXPERIMENT_0.2.md`.
