#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

PROJECT_ID="arenagrid"
REGION="us-central1"
BUCKET_NAME="gs://sukoon-media-bucket-arenagrid"
SERVICE_NAME="sukoon-backend"

echo "Deploying Sukoon Backend to Google Cloud..."

echo "1. Enabling required APIs..."
gcloud services enable run.googleapis.com storage-component.googleapis.com cloudbuild.googleapis.com --project $PROJECT_ID

echo "2. Provisioning Cloud Storage bucket for media..."
# Check if bucket exists, if not create it
if gcloud storage ls --project $PROJECT_ID | grep -q "$BUCKET_NAME"; then
    echo "Bucket $BUCKET_NAME already exists."
else
    echo "Creating bucket $BUCKET_NAME..."
    gcloud storage buckets create $BUCKET_NAME --location=$REGION --project $PROJECT_ID
    # Make the bucket publicly readable if needed (optional, assuming media is public)
    # gcloud storage buckets add-iam-policy-binding $BUCKET_NAME --member=allUsers --role=roles/storage.objectViewer --project $PROJECT_ID
fi

echo "3. Deploying backend to Cloud Run..."
# Source environment variables from backend/.env if it exists
if [ -f "./backend/.env" ]; then
    export $(grep -v '^#' ./backend/.env | xargs)
fi

# Deploy the backend folder to Cloud Run
# Injecting Qdrant configuration from environment variables
gcloud run deploy $SERVICE_NAME \
    --source ./backend \
    --region $REGION \
    --project $PROJECT_ID \
    --allow-unauthenticated \
    --set-env-vars="QDRANT_URL=${QDRANT_URL:-},QDRANT_API_KEY=${QDRANT_API_KEY:-}" \
    --quiet

echo "Deployment completed successfully!"
