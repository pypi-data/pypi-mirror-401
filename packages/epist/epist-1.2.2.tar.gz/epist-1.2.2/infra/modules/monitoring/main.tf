resource "google_monitoring_uptime_check_config" "api_health" {
  display_name = "epist-api-${var.environment}-health"
  timeout      = "10s"
  period       = "300s"
  project      = var.project_id

  http_check {
    path         = "/health"
    port         = "443"
    use_ssl      = true
    validate_ssl = true
  }

  monitored_resource {
    type = "uptime_url"
    labels = {
      project_id = var.project_id
      host       = var.api_host
    }
  }
}

resource "google_monitoring_uptime_check_config" "web_health" {
  display_name = "epist-web-${var.environment}-health"
  timeout      = "10s"
  period       = "300s"
  project      = var.project_id

  http_check {
    path         = "/"
    port         = "443"
    use_ssl      = true
    validate_ssl = true
  }

  monitored_resource {
    type = "uptime_url"
    labels = {
      project_id = var.project_id
      host       = var.web_host
    }
  }
}
