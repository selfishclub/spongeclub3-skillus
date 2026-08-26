# AWS Architecture Workflow & Usage

Read this when running the end-to-end design process, generating IaC, reviewing costs, or
formatting inputs/outputs for the architecture and cost tools.

## Workflow

### Step 1: Gather Requirements

Collect application specifications:

```
- Application type (web app, mobile backend, data pipeline, SaaS)
- Expected users and requests per second
- Budget constraints (monthly spend limit)
- Team size and AWS experience level
- Compliance requirements (GDPR, HIPAA, SOC 2)
- Availability requirements (SLA, RPO/RTO)
```

### Step 2: Design Architecture

Run the architecture designer to get pattern recommendations:

```bash
python scripts/architecture_designer.py --input requirements.json
```

Select from recommended patterns:
- **Serverless Web**: S3 + CloudFront + API Gateway + Lambda + DynamoDB
- **Event-Driven Microservices**: EventBridge + Lambda + SQS + Step Functions
- **Three-Tier**: ALB + ECS Fargate + Aurora + ElastiCache
- **GraphQL Backend**: AppSync + Lambda + DynamoDB + Cognito

See `references/architecture_patterns.md` for detailed pattern specifications.

### Step 3: Generate IaC Templates

Create infrastructure-as-code for the selected pattern:

```bash
# Serverless stack (CloudFormation)
python scripts/serverless_stack.py --app-name my-app --region us-east-1

# Output: CloudFormation YAML template ready to deploy
```

### Step 4: Review Costs

Analyze estimated costs and optimization opportunities:

```bash
python scripts/cost_optimizer.py --resources current_setup.json --monthly-spend 2000
```

Output includes:
- Monthly cost breakdown by service
- Right-sizing recommendations
- Savings Plans opportunities
- Potential monthly savings

### Step 5: Deploy

Deploy the generated infrastructure:

```bash
# CloudFormation
aws cloudformation create-stack \
  --stack-name my-app-stack \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_IAM

# CDK
cdk deploy

# Terraform
terraform init && terraform apply
```

### Step 6: Validate

Verify deployment and set up monitoring:

```bash
# Check stack status
aws cloudformation describe-stacks --stack-name my-app-stack

# Set up CloudWatch alarms
aws cloudwatch put-metric-alarm --alarm-name high-errors ...
```

## Quick Start

### MVP Architecture (< $100/month)

```
Ask: "Design a serverless MVP backend for a mobile app with 1000 users"

Result:
- Lambda + API Gateway for API
- DynamoDB pay-per-request for data
- Cognito for authentication
- S3 + CloudFront for static assets
- Estimated: $20-50/month
```

### Scaling Architecture ($500-2000/month)

```
Ask: "Design a scalable architecture for a SaaS platform with 50k users"

Result:
- ECS Fargate for containerized API
- Aurora Serverless for relational data
- ElastiCache for session caching
- CloudFront for CDN
- CodePipeline for CI/CD
- Multi-AZ deployment
```

### Cost Optimization

```
Ask: "Optimize my AWS setup to reduce costs by 30%. Current spend: $3000/month"

Provide: Current resource inventory (EC2, RDS, S3, etc.)

Result:
- Idle resource identification
- Right-sizing recommendations
- Savings Plans analysis
- Storage lifecycle policies
- Target savings: $900/month
```

### IaC Generation

```
Ask: "Generate CloudFormation for a three-tier web app with auto-scaling"

Result:
- VPC with public/private subnets
- ALB with HTTPS
- ECS Fargate with auto-scaling
- Aurora with read replicas
- Security groups and IAM roles
```

## Input Requirements

Provide these details for architecture design:

| Requirement | Description | Example |
|-------------|-------------|---------|
| Application type | What you're building | SaaS platform, mobile backend |
| Expected scale | Users, requests/sec | 10k users, 100 RPS |
| Budget | Monthly AWS limit | $500/month max |
| Team context | Size, AWS experience | 3 devs, intermediate |
| Compliance | Regulatory needs | HIPAA, GDPR, SOC 2 |
| Availability | Uptime requirements | 99.9% SLA, 1hr RPO |

**JSON Format:**

```json
{
  "application_type": "saas_platform",
  "expected_users": 10000,
  "requests_per_second": 100,
  "budget_monthly_usd": 500,
  "team_size": 3,
  "aws_experience": "intermediate",
  "compliance": ["SOC2"],
  "availability_sla": "99.9%"
}
```

## Output Formats

### Architecture Design

- Pattern recommendation with rationale
- Service stack diagram (ASCII)
- Configuration specifications
- Monthly cost estimate
- Scaling characteristics
- Trade-offs and limitations

### IaC Templates

- **CloudFormation YAML**: Production-ready SAM/CFN templates
- **CDK TypeScript**: Type-safe infrastructure code
- **Terraform HCL**: Multi-cloud compatible configs

### Cost Analysis

- Current spend breakdown
- Optimization recommendations with savings
- Priority action list (high/medium/low)
- Implementation checklist
