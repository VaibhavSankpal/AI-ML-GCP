module "gcp_storage_file_upload" {
    source         = "acnciotfregistry.accenture.com/accenture-cio/storagefileupload/google"
    version        = "1.0.0"
    project_id = "#{GCP_PROJECT_ID}#"
    storage_name   = "#{STORAGE_NAME}#"
    directory_name = "#{DIRECTORY_NAME}#"
}

module "gcp_aiplatformjob1" {
  source = "acnciotfregistry.accenture.com/accenture-cio/aiplatformjob/google"
  version = "1.0.0"
  project_id = "#{GCP_PROJECT_ID}#"
}