module "gcp_aiplatformodelver" {
  source  = "acnciotfregistry.accenture.com/accenture-cio/aiplatformodelver/google"
  version = "0.1.0-beta5"

  project_id = "#{GCP_PROJECT_ID}#"
}