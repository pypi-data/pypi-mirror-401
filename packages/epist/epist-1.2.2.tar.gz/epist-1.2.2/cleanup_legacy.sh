#!/bin/bash
set -e

echo "⚠️  WARNING: This script will DELETE the following legacy resources:"
echo "   - Cloud Run: ambiverse-api"
echo "   - Cloud SQL: audio-rag-db-prod"
echo "   - GCS Bucket: gs://ambiverse-audio-raw"
echo "   - GCS Bucket: gs://audio-rag-content-prod-audiointelligence-3cb34"
echo ""
read -p "Are you sure you want to proceed? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Aborted."
    exit 1
fi

echo "Deleting Cloud Run service..."
gcloud run services delete ambiverse-api --region us-central1 --quiet || echo "Service not found or already deleted."

echo "Deleting Cloud SQL instance..."
gcloud sql instances delete audio-rag-db-prod --quiet || echo "Instance not found or already deleted."

echo "Deleting GCS buckets..."
gcloud storage rm -r gs://ambiverse-audio-raw --quiet || echo "Bucket not found or already deleted."
gcloud storage rm -r gs://audio-rag-content-prod-audiointelligence-3cb34 --quiet || echo "Bucket not found or already deleted."

echo "✅ Cleanup complete!"
