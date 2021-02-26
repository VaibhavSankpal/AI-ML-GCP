# -------------------------- VPC MODULE --------------------------
module "gcp_create_vpc"{
   source       = "acnciotfregistry.accenture.com/accenture-cio/vpc/google" 
   version      = "#{TF_VERSION}#" 
   project_id   = var.gcp_project_id
   region_name  = [var.gcp_project_region]
}

# -------------------------- BACKEND --------------------------
terraform {
  backend "gcs" {
    bucket      = "#{TF_STATE_FILES_BUCKET}#"
    prefix      = "terraform/#{GCP_PROJECT_ID}#/#{Release.DefinitionName}#"
    credentials = "#{GCP_CRED}#"
  }
}