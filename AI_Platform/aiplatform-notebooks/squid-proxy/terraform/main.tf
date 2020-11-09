module "gcp_notebooks" {
  source = "acnciotfregistry.accenture.com/accenture-cio/aiplatformnotebook/google"
  version = "1.0.1"
  project_id = "#{GCP_PROJECT_ID}#"
}