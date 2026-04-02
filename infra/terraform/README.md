# Terraform Scaffold

This is a bootstrap scaffold for MusePicker infrastructure.

## Intended Modules

- `network`: VPC, subnets, routing
- `api_service`: ECS service for Spring API
- `web_service`: ECS service or static hosting for Next.js
- `ingest_jobs`: scheduled ECS tasks for source adapters
- `database`: managed MySQL
- `edge`: Cloudflare DNS/WAF/proxy config

## State & Secrets

- Use remote state backend (S3 + DynamoDB lock) in real deployments.
- Do not commit tfvars with credentials.
- CI/CD should assume AWS role via GitHub OIDC.
