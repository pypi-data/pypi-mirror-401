#!/bin/bash
set -e

PROJECT_ID="audiointelligence-3cb34"
PROJECT_NUMBER="920152096400"
POOL_NAME="github-pool"
PROVIDER_NAME="github-provider"
SA_NAME="github-actions"
REPO="Seifollahi/epist"  # Update if your repo name is different

echo "🚀 Setting up Workload Identity Federation for $REPO..."

# 1. Create Service Account
if ! gcloud iam service-accounts describe "$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" --project "$PROJECT_ID" &>/dev/null; then
    echo "Creating Service Account: $SA_NAME"
    gcloud iam service-accounts create "$SA_NAME" \
        --display-name="GitHub Actions Service Account" \
        --project "$PROJECT_ID"
else
    echo "Service Account $SA_NAME already exists."
fi

# 2. Grant Permissions
echo "Granting permissions..."
ROLES=(
    "roles/run.admin"
    "roles/artifactregistry.writer"
    "roles/iam.serviceAccountUser"
    "roles/storage.admin"
    "roles/secretmanager.secretAccessor"
    "roles/cloudsql.client"
)

for role in "${ROLES[@]}"; do
    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="serviceAccount:$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
        --role="$role" \
        --condition=None
done

# 3. Create Workload Identity Pool
if ! gcloud iam workload-identity-pools describe "$POOL_NAME" --location="global" --project "$PROJECT_ID" &>/dev/null; then
    echo "Creating Workload Identity Pool: $POOL_NAME"
    gcloud iam workload-identity-pools create "$POOL_NAME" \
        --location="global" \
        --display-name="GitHub Actions Pool" \
        --project "$PROJECT_ID"
else
    echo "Pool $POOL_NAME already exists."
fi

# 4. Create Workload Identity Provider
if ! gcloud iam workload-identity-pools providers describe "$PROVIDER_NAME" --workload-identity-pool="$POOL_NAME" --location="global" --project "$PROJECT_ID" &>/dev/null; then
    echo "Creating Workload Identity Provider: $PROVIDER_NAME"
    gcloud iam workload-identity-pools providers create-oidc "$PROVIDER_NAME" \
        --workload-identity-pool="$POOL_NAME" \
        --location="global" \
        --display-name="GitHub Actions Provider" \
        --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
        --attribute-condition="assertion.repository=='$REPO'" \
        --issuer-uri="https://token.actions.githubusercontent.com" \
        --project "$PROJECT_ID"
else
    echo "Provider $PROVIDER_NAME already exists."
fi

# 5. Allow GitHub Actions to impersonate the Service Account
echo "Binding Service Account to WIF..."
gcloud iam service-accounts add-iam-policy-binding "$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --project "$PROJECT_ID" \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/$POOL_NAME/attribute.repository/$REPO"

echo "✅ WIF Setup Complete!"
echo "---------------------------------------------------"
echo "Workload Identity Provider: projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/$POOL_NAME/providers/$PROVIDER_NAME"
echo "Service Account: $SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"
echo "---------------------------------------------------"
