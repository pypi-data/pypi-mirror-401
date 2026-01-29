# acdc-aws-etl-pipeline
Infrastructure and code for the ACDC ETL pipeline and data operations in AWS

## Documentation

- [Dictionary deployment](docs/dictionary_deployment.md)
- [Data ingestion](docs/data_ingestion.md)
- [Data validation](docs/data_validation.md)
- [Data transformation (dbt)](docs/data_transformation_dbt.md)
- [Data releases](docs/write_data_release.md)
- [Synthetic data generation](docs/synthetic_data_generation.md)
- [REST API upload to sheepdog](docs/rest_api_sheepdog_upload.md)
- [Data deletion](docs/data_deletion.md)
- [IndexD file registration](docs/indexd_registration.md)
- [Querying Athena](docs/querying_athena.md)
- [Writing Athena queries to JSON](docs/write_athena_queries_to_json.md)
- [Troubleshooting](docs/troubleshooting.md)

## Library and source code (`src/acdc_aws_etl_pipeline`)

The Python package in [`src/acdc_aws_etl_pipeline`](src/acdc_aws_etl_pipeline) provides reusable utilities for ingestion, validation, uploads, and Athena/Glue operations used across the pipeline and services.

### Modules

- **`ingest/`**: ingestion helpers for loading source datasets into S3/Glue (see [`ingest/ingest.py`](src/acdc_aws_etl_pipeline/ingest/ingest.py)).
- **`upload/`**: Gen3/Sheepdog metadata submission and deletion utilities (e.g. [`upload/metadata_submitter.py`](src/acdc_aws_etl_pipeline/upload/metadata_submitter.py)).
- **`validate/`**: schema validation utilities and helpers for validation workflows (see [`validate/validate.py`](src/acdc_aws_etl_pipeline/validate/validate.py)).
- **`utils/`**: shared Athena/Glue/dbt/release helpers (e.g. [`utils/athena_utils.py`](src/acdc_aws_etl_pipeline/utils/athena_utils.py), [`utils/release_writer.py`](src/acdc_aws_etl_pipeline/utils/release_writer.py)).

### Local development

To install dependencies and run tests:

```bash
pip install poetry
poetry install
source $(poetry env info --path)/bin/activate
poetry run pytest
```

### Install from PyPI

Releases are published automatically, so you can also install the package directly:

```bash
pip install acdc_aws_etl_pipeline