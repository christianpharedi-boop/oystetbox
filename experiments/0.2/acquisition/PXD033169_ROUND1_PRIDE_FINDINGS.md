# PXD033169 Round 1 — ProteomeXchange / PRIDE findings

**Inspection mode:** metadata-only. No measurement files, validation outcomes, or outcome labels were opened.

## Sources reviewed

- ProteomeXchange record: https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD033169
- PRIDE project page: https://www.ebi.ac.uk/pride/archive/projects/PXD033169
- PRIDE archive API project record: https://www.ebi.ac.uk/pride/ws/archive/v2/projects/PXD033169

## Findings

The PRIDE project page rendered an empty project summary, zero project files, and no experimental-design samples in the reviewed route. It displayed unknown values for organism, instrument, software, experiment type, and number of files. This route did not establish any Run-to-Sample, Sample-to-Subject, or Subject-to-Cohort edge.

The PRIDE API route exposed accession-level metadata: PXD033169, partial submission type, CC0 dataset license, publication date 2022-08-11, Orbitrap Exploris 480 instrument, MS-GF+ and DIA-NN software, shotgun proteomics experiment type, human blood serum, and malignant neoplasm of ovary disease annotation. It also exposed the publication DOI 10.1021/acs.jproteome.2c00218 and an accession-level description reporting DIA discovery and targeted-MS validation in an independent cohort.

The API record did not expose a usable participant-level SDRF, sample accession mapping, validation cohort membership, discovery/validation subject IDs, or intersection. The identity graph therefore remains unresolved. The API metadata supports assay and processing metadata at study level but not biological identity-chain proof.

## Round 1 status

| Gate | Status | Basis |
|---|---|---|
| Dataset identity | PASS | Accession and project API record |
| Discovery assay modality | PASS_METADATA_ONLY | DIA and Orbitrap Exploris 480 reported |
| Processing metadata | PARTIAL | DIA-NN and MS-GF+ reported; complete file/parameter chain absent |
| Dataset license | REPORTED_CC0_PENDING_RECONCILIATION | API reports CC0; terms still require record freeze |
| Run → Sample | UNRESOLVED | No usable mapping exposed |
| Sample → Subject | UNRESOLVED | No participant-level field exposed |
| Subject → Cohort | UNRESOLVED | No cohort membership map exposed |
| Cohort intersection | UNRESOLVED | No subject ID sets available |
| Validation subtype | UNRESOLVED | Targeted-MS reported; PRM/SRM subtype not established |

Round 1 did not establish admission. The search proceeds to Round 2, without opening biological measurements or validation outcomes.
