# -------------------------- Terraform Providers -------------------------- 
provider "google-beta" {
  credentials = var.gcp_credential_path
  project     = var.gcp_project_id
  region      = var.gcp_project_region
  zone        = var.gcp_project_zone
}

provider "google" {
  credentials = var.gcp_credential_path
  project     = var.gcp_project_id
  region      = var.gcp_project_region
  zone        = var.gcp_project_zone
}

data "google_project" "project" {
  project_id = var.gcp_project_id
}

# -------------------------- Bucket creation -------------------------- 
module "gcp_storage1" {
  source        = "acnciotfregistry.accenture.com/accenture-cio/storage/google"
  version       = "1.0.0"
  project_id    = var.gcp_project_id
  storage_class = "REGIONAL"
  location      = var.gcp_project_region
  storage_name  = "ml"
}

module "gcp_storage2" {
  source        = "acnciotfregistry.accenture.com/accenture-cio/storage/google"
  version       = "1.0.0"
  project_id    = var.gcp_project_id
  storage_class = "REGIONAL"
  location      = var.gcp_project_region
  storage_name  = "pkgs"
}

module "gcp_storage3" {
  source        = "acnciotfregistry.accenture.com/accenture-cio/storage/google"
  version       = "1.0.0"
  project_id    = var.gcp_project_id
  storage_class = "REGIONAL"
  location      = var.gcp_project_region
  storage_name  = "staging"
}

# -------------------------- BACKEND --------------------------
terraform {
  backend "gcs" {
    bucket      = "#{TF_STATE_FILES_BUCKET}#"
    prefix      = "terraform/#{GCP_PROJECT_ID}#/#{Release.DefinitionName}#"
    credentials = "#{GCP_PROJECT_CREDENTIAL_FILE_PATH}#"
  }
}
