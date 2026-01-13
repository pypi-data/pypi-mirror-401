variable "project_id" {
  description = "The GCP Project ID for Production"
  type        = string
}

variable "region" {
  description = "The GCP Region"
  type        = string
  default     = "us-central1"
}

variable "api_image" {
  description = "The Docker image for the API service"
  type        = string
}
