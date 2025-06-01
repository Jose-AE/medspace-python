# MedSpace Python - Google Cloud Run Deployment

This Flask application provides a machine learning API for rental price prediction, containerized for Google Cloud Run deployment.

## Features

- Machine learning model for rental price prediction using scikit-learn
- Flask REST API with health check endpoint
- Dockerized for easy deployment
- Optimized for Google Cloud Run

## API Endpoints

- `GET /` - Returns the rental price prediction
- `GET /health` - Health check endpoint

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python src/main.py
   ```

3. Access the API at `http://localhost:8080`

## Docker Deployment

### Build and run locally

```bash
# Build the image
docker build -t medspace-python .

# Run the container
docker run -p 8080:8080 medspace-python
```

## Google Cloud Run Deployment

### Prerequisites

1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Authenticate: `gcloud auth login`
3. Set your project: `gcloud config set project YOUR_PROJECT_ID`
4. Enable required APIs:
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

### Manual Deployment

#### Option 1: Using the deployment script (PowerShell)

1. Edit `deploy.ps1` and set your `PROJECT_ID`
2. Run:
   ```powershell
   .\deploy.ps1
   ```

#### Option 2: Using the deployment script (Bash)

1. Edit `deploy.sh` and set your `PROJECT_ID`
2. Make it executable: `chmod +x deploy.sh`
3. Run: `./deploy.sh`

#### Option 3: Manual commands

```bash
# Set variables
export PROJECT_ID="your-gcp-project-id"
export SERVICE_NAME="medspace-python"
export REGION="us-central1"

# Build and push
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME .
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10
```

### Automated Deployment with Cloud Build

1. Connect your repository to Cloud Build
2. Use the provided `cloudbuild.yaml` for automated builds and deployments
3. Trigger builds automatically on code changes

## Environment Variables

- `PORT`: The port number (default: 8080)

## Configuration

The application is configured for Cloud Run with:

- **Memory**: 512Mi
- **CPU**: 1 vCPU
- **Scaling**: 0-10 instances
- **Port**: 8080
- **Platform**: Fully managed

## Data Files

The application uses two CSV files:

- `src/training_data.csv`: Training data for the ML model
- `src/predict_data.csv`: Data to predict (single row)

## Security

- Runs as non-root user in container
- Uses Python slim image for smaller attack surface
- Health check endpoint for monitoring

## Monitoring

Access Cloud Run metrics and logs through the Google Cloud Console:

- Logs: Cloud Logging
- Metrics: Cloud Monitoring
- Health checks: Built-in `/health` endpoint
