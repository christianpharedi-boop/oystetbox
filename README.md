# OysterBox

OysterBox is a clean experimental repository testing whether the scientific-trust architecture developed in [CoreSignal](https://github.com/christianpharedi-boop/coresignal) transfers from Earth-rotation research to proteomics.

> Can a provenance, integrity, quality, admission, analysis, and evidence-chain architecture survive transplantation into molecular science without being redesigned around the new results?

This repository is intentionally a **sandbox**, not a claim that a proteomics result has been biologically validated. It begins with a frozen specification, transparent scoring, deterministic tests, and an explicit record of which CoreSignal invariants are reused and which Earth-specific modules are removed.

## Status

OysterBox Experiment 0.1 is a validation-readiness framework. The default dataset is a small synthetic fixture used only to exercise the pipeline; no biological conclusion should be drawn from it. A real proteomics dataset must be registered with its license, acquisition metadata, raw-file checksum, and analysis plan before admission.

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

The implementation deliberately keeps the architecture small. It does not import Earth-rotation semantics, station logic, geomagnetic models, or domain-specific forecasting into the proteomics experiment.

## Run

```bash
python3 -m unittest discover -s tests -v
python3 scoring/validation_readiness.py
```

The score is transparent and bounded between 0 and 1. It is a readiness indicator, not a probability of biological truth.

## Provenance

OysterBox derives its initial architecture from CoreSignal commit `c29254c483b5cb0d5bcaea86c3e47b7eb727ff15` (2026-08-17). The source history is retained in this repository; the transfer is documented in `provenance/CORESIGNAL_DERIVATION.md`.
