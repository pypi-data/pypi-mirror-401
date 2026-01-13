resource "google_cloud_tasks_queue" "default" {
  name     = var.queue_name
  location = var.location
  project  = var.project_id

  rate_limits {
    max_concurrent_dispatches = var.max_concurrent_dispatches
    max_dispatches_per_second = var.max_dispatches_per_second
  }

  retry_config {
    max_attempts       = var.max_attempts
    max_retry_duration = var.max_retry_duration
    min_backoff        = "0.5s"
    max_backoff        = "3600s"
    max_doublings      = 16
  }
}

variable "project_id" {
  type = string
}

variable "location" {
  type = string
}

variable "queue_name" {
  type = string
}

variable "max_concurrent_dispatches" {
  type    = number
  default = 10
}

variable "max_dispatches_per_second" {
  type    = number
  default = 5
}

variable "max_attempts" {
  type    = number
  default = 5
}

variable "max_retry_duration" {
  type    = string
  default = "3600s"
}

output "queue_id" {
  value = google_cloud_tasks_queue.default.id
}

output "queue_path" {
  value = google_cloud_tasks_queue.default.name
}
