# -------------------------- Model Version creation -------------------------- 
module "gcp_aiplatformodelver" {
  source      = "acnciotfregistry.accenture.com/accenture-cio/aiplatformodelver/google"
  version     = "#{TF_VERSION}#"
  project_id  = var.gcp_project_id
}