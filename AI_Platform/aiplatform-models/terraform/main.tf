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

# -------------------------- Model creation -------------------------- 
module "gcp_tfaimodel" {
  source        = "acnciotfregistry.accenture.com/accenture-cio/aiplatformodel/google"
  version       = "1.0.0"
  project_id    = var.gcp_project_id
  model_name    = "#{MODEL_NAME}#"
  region        = ["#{MODEL_REGION}#"]
  info_model    = "model created for testing by modelmgmt team"
}

# -------------------------- BACKEND --------------------------
terraform {
  backend "gcs" {
    bucket      = "#{TF_STATE_FILES_BUCKET}#"
    prefix      = "terraform/#{GCP_PROJECT_ID}#/#{Release.DefinitionName}#"
    credentials = "#{GCP_PROJECT_CREDENTIAL_FILE_PATH}#"
  }
}
