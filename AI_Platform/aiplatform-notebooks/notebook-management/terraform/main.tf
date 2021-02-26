# -------------------------- AI Notebooks management -------------------------- 

module "gcp_notebooks" {
  source = "acnciotfregistry.accenture.com/accenture-cio/aiplatformnotebook/google"
  version = "#{TF_VERSION}#"
  project_id = var.gcp_project_id
}