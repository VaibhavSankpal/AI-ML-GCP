variable "gcp_credential_path" {
  type        = string
  description = "the gcp credential path"
  default     = ""
}

variable "gcp_project_id" {
  type        = string
  description = "the internal project id of your project "
  default     = ""
}

variable "gcp_project_region" {
  type        = string
  description = "the internal project id of your project"
  default     = "us-east1"
}

variable "gcp_project_zone" {
  type        = string
  description = "the internal project id of your project"
  default     = ""
}