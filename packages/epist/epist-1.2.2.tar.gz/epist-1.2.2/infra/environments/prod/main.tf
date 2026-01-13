terraform {
  required_version = ">= 1.5.0"
  backend "gcs" {
    bucket  = "epist-terraform-state"
    prefix  = "prod"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "database" {
  source = "../../modules/database"
  
  environment = "prod"
  project_id  = var.project_id
  region      = var.region
  tier        = "db-g1-small" # Optimized for cost
}

module "storage" {
  source = "../../modules/storage"
  
  environment = "prod"
  project_id  = var.project_id
  location    = var.region
}

module "cloud_tasks" {
  source = "../../modules/cloud_tasks"

  project_id = var.project_id
  location   = var.region
  queue_name = "transcription-queue-v3"
}

# Secrets for App
resource "random_password" "api_key" {
  length  = 32
  special = false
}

resource "google_secret_manager_secret" "api_key" {
  secret_id = "epist-api-key-prod"
  project   = var.project_id
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "api_key" {
  secret      = google_secret_manager_secret.api_key.id
  secret_data = random_password.api_key.result
}

resource "random_password" "secret_key" {
  length  = 64
  special = true
}

resource "google_secret_manager_secret" "secret_key" {
  secret_id = "epist-secret-key-prod"
  project   = var.project_id
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "secret_key" {
  secret      = google_secret_manager_secret.secret_key.id
  secret_data = random_password.secret_key.result
}

module "api_service" {
  source = "../../modules/cloud_run"

  service_name = "epist-api-prod"
  project_id   = var.project_id
  region       = var.region
  image        = var.api_image
  cloud_sql_instance_connection_name = module.database.instance_connection_name
  min_instances = 0 # Scale to zero when idle
  memory        = "2Gi"
  
  env_vars = {
    DB_HOST               = "/cloudsql/${module.database.instance_connection_name}"
    DB_NAME               = "epist"
    DB_USER               = "epist_user"
    ENVIRONMENT           = "prod"
    FIREBASE_PROJECT_ID   = var.project_id
    SERVICE_ACCOUNT_EMAIL = "920152096400-compute@developer.gserviceaccount.com"
    CLOUD_TASKS_QUEUE_PATH = "projects/audiointelligence-3cb34/locations/us-central1/queues/transcription-queue-v3"
    STRIPE_PRICE_ID_PRO    = "price_1SkAav3yCRFf2ZvZhicGygjC" # Update with Prod Price ID if different
    STRIPE_PRICE_ID_STARTER = "price_1SkAau3yCRFf2ZvZUKCoBNk3"
    API_BASE_URL           = "https://api.epist.ai"
    FRONTEND_URL           = "https://epist.ai"
  }

  secrets = {
    DB_PASSWORD           = module.database.db_password_secret_id
    API_KEY               = google_secret_manager_secret.api_key.secret_id
    SECRET_KEY            = google_secret_manager_secret.secret_key.secret_id
    FIREWORKS_API_KEY     = "epist-fireworks-key"
    OPENAI_API_KEY        = "epist-openai-key"
    STRIPE_SECRET_KEY     = "epist-stripe-secret-key-prod"
    STRIPE_WEBHOOK_SECRET = "epist-stripe-webhook-secret-prod"
    FIREWORKS_PROXY_URL   = "FIREWORKS_PROXY_URL"
  }
}

resource "google_project_iam_member" "secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:920152096400-compute@developer.gserviceaccount.com"
}

module "monitoring" {
  source = "../../modules/monitoring"

  project_id  = var.project_id
  environment = "prod"
  api_host    = "epist-api-prod-920152096400.us-central1.run.app"
  web_host    = "epist.web.app"
}
