provider "aws" {
  region = var.aws_region
}

provider "cloudflare" {}

locals {
  name_prefix = "${var.project_name}-${var.environment}"
  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# Bootstrap placeholders:
# Replace with concrete modules/resources as implementation progresses.
resource "aws_ssm_parameter" "api_placeholder" {
  name  = "/${local.name_prefix}/api/placeholder"
  type  = "String"
  value = "replace-me"
  tags  = local.tags
}
