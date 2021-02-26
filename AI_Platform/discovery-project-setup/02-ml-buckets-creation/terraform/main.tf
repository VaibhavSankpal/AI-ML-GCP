# -------------------------- Bucket creation -------------------------- 
module "gcp_storage1" {
  source        = "acnciotfregistry.accenture.com/accenture-cio/storage/google"
  version       = "#{TF_VERSION}#"
  project_id    = var.gcp_project_id
  storage_class = "#{STORAGE_CLASS}#"
  location      = var.gcp_project_region
  storage_name  = "ml"
}

module "gcp_storage2" {
  source        = "acnciotfregistry.accenture.com/accenture-cio/storage/google"
  version       = "#{TF_VERSION}#"
  project_id    = var.gcp_project_id
  storage_class = "#{STORAGE_CLASS}#"
  location      = var.gcp_project_region
  storage_name  = "pkgs"
}

module "gcp_storage3" {
  source        = "acnciotfregistry.accenture.com/accenture-cio/storage/google"
  version       = "#{TF_VERSION}#"
  project_id    = var.gcp_project_id
  storage_class = "#{STORAGE_CLASS}#"
  location      = var.gcp_project_region
  storage_name  = "staging"
}

# -------------------------- BACKEND --------------------------
terraform {
  backend "gcs" {
    bucket      = "#{TF_STATE_FILES_BUCKET}#"
    prefix      = "terraform/#{GCP_PROJECT_ID}#/#{Release.DefinitionName}#"
    credentials = "#{GCP_CRED}#"
  }
}