# 🚀 Deployment Guide - Planify

## Prerequisites

- Google Cloud Account
- `gcloud` CLI installed
- Docker installed
- Service Account Key JSON file

## Step-by-Step Deployment to Google Cloud Run

### 1. Setup Google Cloud Project

```bash
# Set your project
gcloud config set project YOUR-PROJECT-ID

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  datastore.googleapis.com \
  logging.googleapis.com \
  cloudkms.googleapis.com
```

### 2. Create Service Account

```bash
# Create service account
gcloud iam service-accounts create planify-app \
  --display-name="Planify Application"

# Grant necessary roles
gcloud projects add-iam-policy-binding YOUR-PROJECT-ID \
  --member=serviceAccount:planify-app@YOUR-PROJECT-ID.iam.gserviceaccount.com \
  --role=roles/datastore.user

gcloud projects add-iam-policy-binding YOUR-PROJECT-ID \
  --member=serviceAccount:planify-app@YOUR-PROJECT-ID.iam.gserviceaccount.com \
  --role=roles/logging.logWriter

# Create and download key
gcloud iam service-accounts keys create key.json \
  --iam-account=planify-app@YOUR-PROJECT-ID.iam.gserviceaccount.com
```

### 3. Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy files
COPY requirements.txt .
COPY Planify/ .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run app
CMD exec uvicorn agent:app --host 0.0.0.0 --port 8080
```

### 4. Build and Push Docker Image

```bash
# Build image
docker build -t gcr.io/YOUR-PROJECT-ID/planify:latest .

# Configure Docker credentials
gcloud auth configure-docker

# Push to Google Container Registry
docker push gcr.io/YOUR-PROJECT-ID/planify:latest
```

### 5. Create Cloud Run Service

```bash
# Deploy to Cloud Run
gcloud run deploy planify \
  --image gcr.io/YOUR-PROJECT-ID/planify:latest \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --allow-unauthenticated \
  --set-env-vars "MODEL=gemini-1.5-flash,GOOGLE_CLOUD_PROJECT=YOUR-PROJECT-ID"
```

### 6. Setup Database

```bash
# Set default Datastore location (one-time setup)
gcloud datastore databases create \
  --database=default \
  --location=us-central1 \
  --type=datastore-mode
```

## Alternative: Deploy with gcloud run deploy

```bash
cd Planify

# Direct deployment
gcloud run deploy planify \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --timeout 300 \
  --allow-unauthenticated \
  --set-env-vars "MODEL=gemini-1.5-flash"
```

## Verify Deployment

```bash
# Get the service URL
SERVICE_URL=$(gcloud run services describe planify \
  --region us-central1 \
  --format 'value(status.url)')

echo $SERVICE_URL

# Test the API
curl "${SERVICE_URL}/api/v1/summary"

# Test chat endpoint
curl -X POST "${SERVICE_URL}/api/v1/workspace/chat" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}'
```

## Monitor Deployment

```bash
# View logs
gcloud run services describe planify --region us-central1

# Stream logs
gcloud logging read \
  "resource.type=cloud_run_revision AND resource.labels.service_name=planify" \
  --limit 100 \
  --format json

# View metrics
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/request_count"'
```

## Troubleshooting

### Service won't start
```bash
# Check logs for errors
gcloud run logs read planify --region us-central1 --limit 50

# Verify environment variables
gcloud run services describe planify --region us-central1
```

### Datastore connection error
```bash
# Verify service account has Datastore permissions
gcloud projects get-iam-policy YOUR-PROJECT-ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:*"
```

### Out of memory errors
```bash
# Increase memory allocation
gcloud run services update planify \
  --memory 1Gi \
  --region us-central1
```

## Environment Variables

Set these via Cloud Run Console or CLI:

```bash
gcloud run services update planify \
  --region us-central1 \
  --update-env-vars "MODEL=gemini-1.5-flash,GOOGLE_CLOUD_PROJECT=YOUR-PROJECT-ID"
```

## Cost Optimization

1. **Adjust resource allocation**
   ```bash
   gcloud run services update planify \
     --memory 256Mi \
     --cpu 0.5 \
     --region us-central1
   ```

2. **Set maximum instances**
   ```bash
   gcloud run services update planify \
     --max-instances 10 \
     --region us-central1
   ```

3. **Enable Cloud CDN** (for static content)
   ```bash
   gcloud compute backend-services create planify-backend \
     --enable-cdn
   ```

## Continuous Deployment (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - uses: google-github-actions/setup-gcloud@v0
        with:
          service_account_key: ${{ secrets.GCP_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          export_default_credentials: true

      - name: Build and push image
        run: |
          gcloud builds submit \
            --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/planify

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy planify \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/planify \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated
```

## Post-Deployment Checklist

- [ ] Service is running: Check Cloud Run console
- [ ] Logging is working: View logs in Cloud Logging
- [ ] Database connectivity: Test with `/api/v1/summary`
- [ ] API endpoints work: Test POST requests
- [ ] AI chat responds: Test `/workspace/chat`
- [ ] Monitoring is setup: Check Cloud Monitoring
- [ ] Backup enabled: Enable Cloud Datastore backups

## Rollback

```bash
# View available revisions
gcloud run revisions list --service=planify --region=us-central1

# Rollback to previous version
gcloud run deploy planify \
  --image=gcr.io/YOUR-PROJECT-ID/planify:previous-version \
  --region us-central1
```

## Scaling & Performance

```bash
# Set concurrency
gcloud run services update planify \
  --concurrency 100 \
  --region us-central1

# Set request timeout
gcloud run services update planify \
  --timeout 300 \
  --region us-central1
```

---

**For detailed help, run:** `gcloud run deploy --help`
