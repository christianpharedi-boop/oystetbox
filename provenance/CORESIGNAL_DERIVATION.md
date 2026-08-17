# CoreSignal derivation record

OysterBox was created from the CoreSignal repository at commit `c29254c483b5cb0d5bcaea86c3e47b7eb727ff15`, titled `ci: scope lint checks to production code`, dated 2026-08-17.

The original Git history is retained rather than squashed. The new repository is an experimental transfer, not a modification of CoreSignal. Earth-rotation data, station/archive workflows, geomagnetic logic, and Earth-specific forecasting code were removed from the working tree because they are outside the proteomics hypothesis.

The preserved architectural invariants are: explicit provenance, content hashing, deterministic validation, quality gating before admission, experiment manifests, reproducibility metadata, and an auditable chain from a finding to supporting evidence. Any future deviation from these invariants must be recorded as an experiment decision.

This record describes software lineage only. It does not assert that the two scientific domains are substantively equivalent, and it does not grant any rights beyond the applicable repository terms.
