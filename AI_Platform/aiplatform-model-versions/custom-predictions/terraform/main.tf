# -------------------------- Model Version - custom prediction -------------------------- 

module "gcp_storage_file_upload" {
    source         = "acnciotfregistry.accenture.com/accenture-cio/storagefileupload/google"
    version        = "#{STORAGE_TF_VERSION}#"
    project_id     = var.gcp_project_id
    storage_name   = "#{GCP_PACKAGE_BUCKET}#"
    directory_name = "#{DIRECTORY}#"
  }

module "gcp_aiplatformodelver" {
  source      = "acnciotfregistry.accenture.com/accenture-cio/aiplatformodelver/google"
  version     = "#{TF_VERSION}#"
  project_id  = var.gcp_project_id
}