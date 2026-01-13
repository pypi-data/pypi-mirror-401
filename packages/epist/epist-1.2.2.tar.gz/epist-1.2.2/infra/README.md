# Infrastructure as Code (Terraform)

This directory contains the Terraform configuration for Epist.ai, following a modular, Cloud Native approach.

## Structure

- **`environments/`**: Contains stateful configurations for each environment.
    - **`staging/`**: The staging environment, automatically deployed from the `main` branch.
    - **`prod/`**: The production environment, deployed manually after approval.
- **`modules/`**: Reusable Terraform modules.
    - **`cloud_run/`**: Configuration for Cloud Run services (API, Workers).
    - **`database/`**: Cloud SQL (PostgreSQL + pgvector) setup.
    - **`storage/`**: Cloud Storage buckets for audio and artifacts.

## Prerequisites

- Terraform >= 1.5.0
- Google Cloud SDK (gcloud)
- A GCP Project for Staging and another for Production (recommended for isolation).

## Usage

### Staging

```bash
cd environments/staging
terraform init
terraform apply
```

### Production

```bash
cd environments/prod
terraform init
terraform apply
```
