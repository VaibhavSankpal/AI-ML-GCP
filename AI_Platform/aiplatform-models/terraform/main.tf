# -------------------------- Model creation -------------------------- 
module "gcp_tfaimodel" {
  source        = "acnciotfregistry.accenture.com/accenture-cio/aiplatformodel/google"
  version       = "#{TF_VERSION}#"
  project_id    = var.gcp_project_id
}