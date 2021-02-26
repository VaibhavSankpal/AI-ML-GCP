# -------------------------- AI Platform Jobs Training -------------------------- 

module "gcp_aiplatformjob1" {
  source = "acnciotfregistry.accenture.com/accenture-cio/aiplatformjob/google"
  version = "#{TF_VERSION}#"
  project_id = var.gcp_project_id
}