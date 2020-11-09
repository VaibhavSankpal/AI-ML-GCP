module "gcp_aiplatformjob1" {
  source = "acnciotfregistry.accenture.com/accenture-cio/aiplatformjob/google"
  version = "1.0.0"

  project_id = "#{GCP_PROJECT_ID}#"
}