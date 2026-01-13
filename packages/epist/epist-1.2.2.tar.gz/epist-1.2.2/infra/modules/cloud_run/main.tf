variable "project_id" {}
variable "region" {}
variable "service_name" {}
variable "image" {}
variable "env_vars" {
  type = map(string)
  default = {}
}
variable "secrets" {
  type = map(string)
  default = {}
  description = "Map of environment variable name to secret ID"
}
variable "min_instances" {
  default = 0
}

variable "max_instances" {
  default = 10
}

variable "cloud_sql_instance_connection_name" {
  default = ""
}

variable "vpc_connector_id" {
  default = ""
}

variable "memory" {
  default = "1024Mi"
}

resource "google_cloud_run_v2_service" "default" {
  name     = var.service_name
  location = var.region
  project  = var.project_id
  ingress = "INGRESS_TRAFFIC_ALL"
  deletion_protection = false

  template {
    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }
    timeout = "3600s" 
    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [var.cloud_sql_instance_connection_name]
      }
    }

    dynamic "vpc_access" {
      for_each = var.vpc_connector_id != "" ? [1] : []
      content {
        connector = var.vpc_connector_id
        egress    = "PRIVATE_RANGES_ONLY"
      }
    }



    containers {
      image = var.image
      
      dynamic "env" {
        for_each = var.env_vars
        content {
          name  = env.key
          value = env.value
        }
      }

      # Mount secrets as environment variables
      dynamic "env" {
        for_each = var.secrets
        content {
          name = env.key
          value_source {
            secret_key_ref {
              secret  = env.value
              version = "latest"
            }
          }
        }
      }
      
      resources {
        limits = {
          cpu    = "2000m"
          memory = var.memory
        }
      }

      startup_probe {
        initial_delay_seconds = 10
        timeout_seconds       = 10
        period_seconds        = 30
        failure_threshold     = 20
        tcp_socket {
          port = 8080
        }
      }

      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }
    }
  }
}

resource "google_cloud_run_service_iam_member" "public" {
  service  = google_cloud_run_v2_service.default.name
  location = google_cloud_run_v2_service.default.location
  project  = google_cloud_run_v2_service.default.project
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "service_name" {
  value = google_cloud_run_v2_service.default.name
}

output "service_uri" {
  value = google_cloud_run_v2_service.default.uri
}
