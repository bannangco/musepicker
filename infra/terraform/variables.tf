variable "aws_region" {
  type        = string
  description = "AWS region for MusePicker services"
  default     = "ap-northeast-2"
}

variable "project_name" {
  type        = string
  description = "Project slug"
  default     = "musepicker"
}

variable "environment" {
  type        = string
  description = "Deployment environment (dev/staging/prod)"
}

variable "cloudflare_zone_id" {
  type        = string
  description = "Cloudflare Zone ID"
  sensitive   = true
}
