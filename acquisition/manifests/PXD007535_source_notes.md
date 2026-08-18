# PXD007535 acquisition source notes

## Official sources

The ProteomeXchange record is:

- https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD007535

The current PRIDE Archive page is:

- https://www.ebi.ac.uk/pride/archive/projects/PXD007535

The official PRIDE project API endpoints used for metadata-only acquisition are:

- https://www.ebi.ac.uk/pride/ws/archive/v2/projects/PXD007535
- https://www.ebi.ac.uk/pride/ws/archive/v2/projects/PXD007535/files

The file transport source is:

- https://ftp.pride.ebi.ac.uk/pride/data/archive/2018/04/PXD007535/

The publication DOI is:

- https://doi.org/10.1074/mcp.RA118.000718

## Metadata-only findings

The official project metadata identifies PXD007535 as an original PRIDE dataset titled “LFQ and SRM proteome analysis of Saliva reveals transition signatures from health to periodontal disease.” The project record describes a discovery phase and an SRM validation phase and lists PRIDE as the hosting repository. The official API reported a file inventory containing raw mass-spectrometry files and smaller SRM-related files.

The full project metadata and file listing were acquired without opening validation results. They are stored as `PXD007535_project.json` and `PXD007535_files.json`. A metadata-only inventory was generated as `PXD007535_file_inventory_metadata.json`.

## Acquisition boundary

One small discovery-side scan and three small SRM-side files were acquired over HTTPS. The SRM-side files are stored under `acquisition/PXD007535/validation_sealed/` and have not been opened or passed to OysterBox. The complete discovery LFQ artifact and complete validation/outcome artifact have not been acquired, so the admission audit remains blocked.

Dataset-level licensing remains unverified. Publication licensing and dataset licensing are tracked separately.
