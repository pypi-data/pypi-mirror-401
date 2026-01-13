variable "project_id" {}
variable "location" {}
variable "environment" {}

resource "google_storage_bucket" "audio_bucket" {
  name          = "epist-content-${var.environment}-${var.project_id}"
  location      = var.location
  project       = var.project_id
  force_destroy = var.environment != "prod"

  uniform_bucket_level_access = true
}

output "bucket_name" {
  value = google_storage_bucket.audio_bucket.name
}
