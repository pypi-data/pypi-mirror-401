variable "project_id" {}
variable "region" {}
variable "environment" {}
variable "tier" {
  default = "db-f1-micro"
}

resource "random_password" "db_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "google_secret_manager_secret" "db_password" {
  secret_id = "epist-db-password-${var.environment}"
  project   = var.project_id
  
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = random_password.db_password.result
}

resource "google_sql_database_instance" "instance" {
  name             = "epist-db-${var.environment}"
  database_version = "POSTGRES_15"
  region           = var.region
  project          = var.project_id

  settings {
    tier = var.tier
    
    ip_configuration {
      ipv4_enabled = true # Keeping Public IP for now, but using strong password
      ssl_mode     = "ENCRYPTED_ONLY" # Enforce SSL
    }

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "02:00" # 2 AM UTC
      transaction_log_retention_days = 7
    }
  }

  deletion_protection = var.environment == "prod"
}

resource "google_sql_database" "database" {
  name     = "epist"
  instance = google_sql_database_instance.instance.name
  project  = var.project_id
}

resource "google_sql_user" "users" {
  name     = "epist_user"
  instance = google_sql_database_instance.instance.name
  password = random_password.db_password.result
  project  = var.project_id
}

output "connection_string" {
  # Note: This output now contains a sensitive value (the password)
  # In a real pipeline, we might want to suppress this or construct it differently
  value     = "postgresql://epist_user:${random_password.db_password.result}@${google_sql_database_instance.instance.public_ip_address}/epist"
  sensitive = true
}

output "public_ip_address" {
  value = google_sql_database_instance.instance.public_ip_address
}

output "instance_connection_name" {
  value = google_sql_database_instance.instance.connection_name
}

output "db_password_secret_id" {
  value = google_secret_manager_secret.db_password.secret_id
}
