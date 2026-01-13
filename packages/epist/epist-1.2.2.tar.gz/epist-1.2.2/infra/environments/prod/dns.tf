resource "google_dns_managed_zone" "prod_zone" {
  name        = "epist-ai-zone"
  dns_name    = "epist.ai."
  description = "Production DNS zone for epist.ai"
  project     = var.project_id

  visibility = "public"
}

resource "google_dns_record_set" "verification" {
  name         = "epist.ai."
  managed_zone = google_dns_managed_zone.prod_zone.name
  type         = "TXT"
  ttl          = 300
  project      = var.project_id

  rrdatas = [
    "google-site-verification=nwVMHNfsmqNkHiP0OYisummC8p_oylyU0MiNshtiMtY",
    "hosting-site=audiointelligence-3cb34"
  ]
}

resource "google_dns_record_set" "root_a" {
  name         = "epist.ai."
  managed_zone = google_dns_managed_zone.prod_zone.name
  type         = "A"
  ttl          = 300
  project      = var.project_id

  rrdatas = ["199.36.158.100"]
}

resource "google_dns_record_set" "api_cname" {
  name         = "api.epist.ai."
  managed_zone = google_dns_managed_zone.prod_zone.name
  type         = "CNAME"
  ttl          = 300
  project      = var.project_id

  rrdatas = ["ghs.googlehosted.com."]
}

resource "google_dns_record_set" "www_cname" {
  name         = "www.epist.ai."
  managed_zone = google_dns_managed_zone.prod_zone.name
  type         = "CNAME"
  ttl          = 300
  project      = var.project_id

  rrdatas = ["audiointelligence-3cb34.web.app."]
}

resource "google_cloud_run_domain_mapping" "api_mapping" {
  name      = "api.epist.ai"
  location  = var.region
  project   = var.project_id
  
  metadata {
    namespace = var.project_id
  }

  spec {
    route_name = module.api_service.service_name
  }
}

output "nameservers" {
  value       = google_dns_managed_zone.prod_zone.name_servers
  description = "The nameservers for the production DNS zone. Update your registrar with these."
}

output "api_domain_verification" {
  value       = google_cloud_run_domain_mapping.api_mapping.status[0].resource_records
  description = "DNS records required for Cloud Run domain mapping verification."
}
