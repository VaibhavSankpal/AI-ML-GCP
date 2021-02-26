# -------------------------- AI Platform Jobs Custom Container -------------------------- 

module "gcp_storage_file_upload" {
    source         = "acnciotfregistry.accenture.com/accenture-cio/storagefileupload/google"
    version        = "#{TF_VERSION_STORAGE_UPLOAD}#"
    project_id     = var.gcp_project_id
    storage_name   = "#{STORAGE_NAME}#"
    directory_name = "#{DIRECTORY_NAME}#"
}

module "gcp_aiplatformjob1" {
  source      = "acnciotfregistry.accenture.com/accenture-cio/aiplatformjob/google"
  version     = "#{TF_VERSION}#"
  project_id  = var.gcp_project_id
}