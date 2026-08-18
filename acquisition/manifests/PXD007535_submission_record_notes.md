# PXD007535 ProteomeXchange submission record notes

## Source

- Submission record route: https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD007535.0-2&outputMode=XML&test=no

## Findings

The ProteomeXchange XML is revision 2 for accession PXD007535 and repeats the project-level description: 66 systemically healthy subjects in Phase 1 and 82 subjects in the Phase 2 independent saliva cohort. It contains dataset summary, accession, species, instrument, and repository metadata, but the exposed record does not provide subject-level identifiers, sample manifests, or an explicit mapping of files to discovery versus validation cohorts.

The submission record therefore confirms the project-level count discrepancy but does not resolve its unit of analysis or cohort intersection. No validation measurements or outcome contents were opened.

## Consequence

This route is authoritative for project-level submission metadata but insufficient for population reconciliation. The unit-of-analysis status remains blocked, and the next route remains PRIDE sample metadata/SDRF or an equivalent authoritative sample-level manifest.
