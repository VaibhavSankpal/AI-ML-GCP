module "gcp_storage_file_upload" {
    source         = "acnciotfregistry.accenture.com/accenture-cio/storagefileupload/google"
    version        = "1.0.0"
    project_id     = "#{GCP_PROJECT_ID}#"
    storage_name   = "#{GCP_PACKAGE_BUCKET}#"
    directory_name = "#{DIRECTORY}#"
  }

module "gcp_aiplatformodelver" {
  source  = "acnciotfregistry.accenture.com/accenture-cio/aiplatformodelver/google"
  version = "0.1.0-beta5"
  project_id = "#{GCP_PROJECT_ID}#"
}