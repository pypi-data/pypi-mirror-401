terraform {
  required_version = ">= 1.5.0"
  backend "gcs" {
    bucket  = "epist-tf-state-staging"
    prefix  = "staging"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "database" {
  source = "../../modules/database"
  
  environment = "staging"
  project_id  = var.project_id
  region      = var.region
}

module "storage" {
  source = "../../modules/storage"
  
  environment = "staging"
  project_id  = var.project_id
  location    = var.region
}



# Secrets for App

resource "random_password" "api_key" {
  length  = 32
  special = false
}

resource "google_secret_manager_secret" "api_key" {
  secret_id = "epist-api-key-staging"
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
  secret_id = "epist-secret-key-staging"
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

  service_name = "epist-api-staging"
  project_id   = var.project_id
  region       = var.region
  image        = var.api_image
  cloud_sql_instance_connection_name = module.database.instance_connection_name
  env_vars = {

    DB_HOST      = "/cloudsql/${module.database.instance_connection_name}"
    DB_NAME      = "epist"
    DB_USER      = "epist_user"
    ENVIRONMENT  = "staging"
    SERVICE_ACCOUNT_EMAIL = "920152096400-compute@developer.gserviceaccount.com"
    CLOUD_TASKS_QUEUE_PATH = "projects/audiointelligence-3cb34/locations/us-central1/queues/transcription-queue-v3"
    STRIPE_PRICE_ID_PRO    = "price_1SdmnX3GSBwsq2SjKXLMiwDL" # Pro Plan Monthly
  }

  secrets = {
    DB_PASSWORD           = module.database.db_password_secret_id
    API_KEY               = google_secret_manager_secret.api_key.secret_id
    SECRET_KEY            = google_secret_manager_secret.secret_key.secret_id
    FIREWORKS_API_KEY     = "epist-fireworks-key"
    OPENAI_API_KEY        = "epist-openai-key"
    STRIPE_SECRET_KEY     = "epist-stripe-secret-key-staging"
    STRIPE_WEBHOOK_SECRET = "epist-stripe-webhook-secret-staging"
  }
}

module "cloud_tasks" {
  source = "../../modules/cloud_tasks"

  project_id = var.project_id
  location   = var.region
  queue_name = "transcription-queue-v3"
}

resource "google_project_iam_member" "secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:920152096400-compute@developer.gserviceaccount.com"
}

module "monitoring" {
  source = "../../modules/monitoring"

  project_id  = var.project_id
  environment = "staging"
  api_host    = "epist-api-staging-920152096400.us-central1.run.app"
  web_host    = "epist-staging.web.app"
}
