variable "project_id" {
  description = "The project ID to deploy to"
  type        = string
}

variable "environment" {
  description = "The environment (staging or prod)"
  type        = string
}

variable "api_host" {
  description = "The hostname of the API (without protocol)"
  type        = string
}

variable "web_host" {
  description = "The hostname of the Web App (without protocol)"
  type        = string
}
