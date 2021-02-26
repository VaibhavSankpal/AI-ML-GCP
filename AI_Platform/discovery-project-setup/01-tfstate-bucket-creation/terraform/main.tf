# -------------------------- Bucket creation -------------------------- 
module "gcp_storage" {
  source        = "acnciotfregistry.accenture.com/accenture-cio/storage/google"
  version       = "#{TF_VERSION}#"
  project_id    = var.gcp_project_id
  storage_class = "REGIONAL"
  location      = var.gcp_project_region
  storage_name  = "tf-state"
  versioning    = true
}