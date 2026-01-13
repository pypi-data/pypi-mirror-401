#!/bin/bash
set -e

PROJECT_ID="audiointelligence-3cb34"
REGION="us-central1"
BUCKET_NAME="epist-terraform-state"

echo "🚀 Bootstrapping GCP Project: $PROJECT_ID"

# 1. Enable required APIs
echo "Enable APIs..."
gcloud services enable \
    compute.googleapis.com \
    sqladmin.googleapis.com \
    run.googleapis.com \
    storage.googleapis.com \
    servicenetworking.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    secretmanager.googleapis.com \
    --project "$PROJECT_ID"

# 2. Create Terraform State Bucket
echo "Checking Terraform State Bucket..."
if ! gcloud storage buckets describe "gs://$BUCKET_NAME" --project "$PROJECT_ID" &>/dev/null; then
    echo "Creating bucket: gs://$BUCKET_NAME"
    gcloud storage buckets create "gs://$BUCKET_NAME" \
        --project "$PROJECT_ID" \
        --location "$REGION" \
        --uniform-bucket-level-access
    
    # Enable versioning for state safety
    gcloud storage buckets update "gs://$BUCKET_NAME" --versioning
else
    echo "Bucket gs://$BUCKET_NAME already exists."
fi

# 3. Create Artifact Registry Repository
echo "Checking Artifact Registry..."
REPO_NAME="epist-repo"
if ! gcloud artifacts repositories describe "$REPO_NAME" --project "$PROJECT_ID" --location "$REGION" &>/dev/null; then
    echo "Creating repository: $REPO_NAME"
    gcloud artifacts repositories create "$REPO_NAME" \
        --project "$PROJECT_ID" \
        --location "$REGION" \
        --repository-format=docker \
        --description="Epist Docker Repository"
else
    echo "Repository $REPO_NAME already exists."
fi

# 4. Create Audio Upload Bucket
echo "Checking Audio Bucket..."
AUDIO_BUCKET="epist-audio-raw"
if ! gcloud storage buckets describe "gs://$AUDIO_BUCKET" --project "$PROJECT_ID" &>/dev/null; then
    echo "Creating bucket: gs://$AUDIO_BUCKET"
    gcloud storage buckets create "gs://$AUDIO_BUCKET" \
        --project "$PROJECT_ID" \
        --location "$REGION" \
        --uniform-bucket-level-access
else
    echo "Bucket gs://$AUDIO_BUCKET already exists."
fi

echo "✅ Bootstrap complete!"
