# Tool Reference

Read this when invoking the Python tools programmatically — full constructor parameters,
methods, requirement dictionaries, and worked examples for each script.

These tools are Python classes imported from `scripts/` (not CLIs). Import the class, pass
the requirement/resource dictionaries described below, and call the documented methods.

## architecture_designer.py

**Purpose:** Generates architecture pattern recommendations based on application requirements. Analyzes app type, expected scale, budget, team experience, and compliance needs to recommend the optimal AWS architecture pattern with full service configurations and cost estimates.

**Usage:**

```python
from scripts.architecture_designer import ArchitectureDesigner

designer = ArchitectureDesigner(requirements)
pattern = designer.recommend_architecture_pattern()
checklist = designer.generate_service_checklist()
```

**Constructor Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `requirements` | `dict` | Yes | -- | Dictionary containing all application requirements (see fields below) |

**Requirements Dictionary Fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `application_type` | `str` | `"web_application"` | One of: `web_application`, `mobile_backend`, `data_pipeline`, `microservices`, `saas_platform`, `iot_platform` |
| `expected_users` | `int` | `1000` | Expected number of users (or devices for IoT) |
| `requests_per_second` | `int` | `10` | Expected peak requests per second |
| `budget_monthly_usd` | `float` | `500` | Maximum monthly AWS budget in USD |
| `team_size` | `int` | `3` | Number of engineers on the team |
| `aws_experience` | `str` | `"beginner"` | Team AWS experience level |
| `compliance` | `list` | `[]` | List of compliance frameworks (e.g., `["SOC2", "HIPAA"]`) |
| `data_size_gb` | `int` | `10` | Expected data volume in GB |

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `recommend_architecture_pattern()` | `dict` | Returns recommended pattern with services, cost estimate, pros/cons, and scaling characteristics |
| `generate_service_checklist()` | `list[dict]` | Returns phased implementation checklist (Planning, Foundation, Core Services, Security, Monitoring, CI/CD) |

**Example:**

```python
from scripts.architecture_designer import ArchitectureDesigner

requirements = {
    "application_type": "saas_platform",
    "expected_users": 10000,
    "requests_per_second": 100,
    "budget_monthly_usd": 500,
    "team_size": 3,
    "aws_experience": "intermediate",
    "compliance": ["SOC2"],
    "data_size_gb": 50
}

designer = ArchitectureDesigner(requirements)
result = designer.recommend_architecture_pattern()
print(result['pattern_name'])       # "Serverless Web Application"
print(result['estimated_cost'])     # {"monthly_usd": ..., "breakdown": {...}}
print(result['services'])           # Full service stack with configurations
```

**Output Format:** Returns a dictionary with keys: `pattern_name`, `description`, `use_case`, `services` (nested service configurations), `estimated_cost` (with `monthly_usd` and `breakdown`), `pros`, `cons`, and `scaling_characteristics`.

**Supported Patterns:**
- Serverless Web Application (< 10k users)
- Modern Three-Tier Application (10k-100k users)
- Multi-Region High Availability (100k+ users)
- Serverless Mobile Backend (mobile app type)
- Event-Driven Microservices (microservices type)
- Real-Time Data Pipeline (data pipeline type)
- IoT Platform (IoT type)

## serverless_stack.py

**Purpose:** Generates production-ready infrastructure-as-code templates for serverless applications. Produces CloudFormation (SAM), CDK (TypeScript), and Terraform (HCL) configurations with API Gateway, Lambda, DynamoDB, Cognito, IAM roles, and CloudWatch logging preconfigured.

**Usage:**

```python
from scripts.serverless_stack import ServerlessStackGenerator

generator = ServerlessStackGenerator(app_name, requirements)
cfn_template = generator.generate_cloudformation_template()
cdk_stack = generator.generate_cdk_stack()
terraform_config = generator.generate_terraform_configuration()
```

**Constructor Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `app_name` | `str` | Yes | -- | Application name (used for resource naming; auto-lowercased, spaces replaced with hyphens) |
| `requirements` | `dict` | Yes | -- | Dictionary with deployment requirements (see fields below) |

**Requirements Dictionary Fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `region` | `str` | `"us-east-1"` | AWS region for deployment |

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `generate_cloudformation_template()` | `str` | YAML CloudFormation/SAM template with DynamoDB, Lambda, API Gateway, Cognito, IAM, and CloudWatch |
| `generate_cdk_stack()` | `str` | TypeScript CDK stack with equivalent resources |
| `generate_terraform_configuration()` | `str` | Terraform HCL configuration with equivalent resources |

**Example:**

```python
from scripts.serverless_stack import ServerlessStackGenerator

generator = ServerlessStackGenerator("my-saas-app", {"region": "us-west-2"})

# Generate CloudFormation template
cfn = generator.generate_cloudformation_template()
with open("template.yaml", "w") as f:
    f.write(cfn)

# Generate CDK stack
cdk = generator.generate_cdk_stack()
with open("lib/stack.ts", "w") as f:
    f.write(cdk)

# Generate Terraform config
tf = generator.generate_terraform_configuration()
with open("main.tf", "w") as f:
    f.write(tf)
```

**Output Format:** Each method returns a string containing the full IaC template. Templates include: DynamoDB table (single-table design with PK/SK), Lambda function (Node.js 18.x, 512 MB, 10s timeout), API Gateway (REST, Cognito auth, CORS, throttling), Cognito User Pool (email sign-in, optional MFA), IAM roles (least privilege), and CloudWatch log group (7-day retention). All templates output: API URL, User Pool ID, User Pool Client ID, and Table Name.

## cost_optimizer.py

**Purpose:** Analyzes current AWS resource inventory and spending to generate prioritized cost optimization recommendations. Evaluates compute (EC2, Lambda), storage (S3), databases (RDS, DynamoDB), networking (NAT Gateway, VPC endpoints), and general optimizations (CloudWatch Logs, Elastic IPs, budget alerts).

**Usage:**

```python
from scripts.cost_optimizer import CostOptimizer

optimizer = CostOptimizer(current_resources, monthly_spend)
analysis = optimizer.analyze_and_optimize()
checklist = optimizer.generate_optimization_checklist()
```

**Constructor Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `current_resources` | `dict` | Yes | -- | Dictionary describing current AWS resources (see fields below) |
| `monthly_spend` | `float` | Yes | -- | Current monthly AWS spend in USD |

**Resources Dictionary Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `ec2_instances` | `list[dict]` | EC2 instances with `cpu_utilization` (%), `pricing` (`"on-demand"` or `"reserved"`) |
| `lambda_functions` | `list[dict]` | Lambda functions with `memory_mb`, `avg_memory_used_mb` |
| `s3_buckets` | `list[dict]` | S3 buckets with `name`, `size_gb`, `storage_class`, `has_lifecycle_policy` (bool) |
| `rds_instances` | `list[dict]` | RDS instances with `name`, `connections_per_day`, `monthly_cost`, `engine`, `utilization` (%) |
| `dynamodb_tables` | `list[dict]` | DynamoDB tables with `name`, `billing_mode`, `read_capacity_units`, `write_capacity_units`, `utilization_percentage` |
| `nat_gateways` | `list[dict]` | NAT Gateway resources |
| `multi_az_required` | `bool` | Whether multi-AZ NAT is required |
| `vpc_endpoints` | `list` | Existing VPC endpoints |
| `s3_data_transfer_gb` | `float` | Monthly S3 data transfer volume in GB |
| `cloudwatch_log_groups` | `list[dict]` | Log groups with `name`, `retention_days` (`-1` for never expire), `size_gb` |
| `elastic_ips` | `list[dict]` | Elastic IPs with `attached` (bool) |
| `has_budget_alerts` | `bool` | Whether AWS Budgets are configured |
| `has_cost_explorer` | `bool` | Whether Cost Explorer is enabled |

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `analyze_and_optimize()` | `dict` | Full cost analysis with current spend, potential savings, optimized spend, savings percentage, recommendations list, and top 5 priority actions |
| `generate_optimization_checklist()` | `list[dict]` | Phased action checklist: Immediate (today), This Week, This Month, Ongoing |

**Example:**

```python
from scripts.cost_optimizer import CostOptimizer

resources = {
    "ec2_instances": [
        {"cpu_utilization": 5, "pricing": "on-demand"},
        {"cpu_utilization": 65, "pricing": "on-demand"}
    ],
    "s3_buckets": [
        {"name": "app-assets", "size_gb": 200, "storage_class": "STANDARD", "has_lifecycle_policy": False}
    ],
    "nat_gateways": [{"id": "nat-1"}, {"id": "nat-2"}],
    "multi_az_required": False,
    "has_budget_alerts": False,
    "has_cost_explorer": False
}

optimizer = CostOptimizer(resources, monthly_spend=3000)
result = optimizer.analyze_and_optimize()

print(f"Current spend: ${result['current_monthly_spend']}")
print(f"Potential savings: ${result['potential_monthly_savings']}")
print(f"Savings: {result['savings_percentage']}%")
for rec in result['priority_actions']:
    print(f"  [{rec['priority']}] {rec['service']}: {rec['recommendation']}")
```

**Output Format:** `analyze_and_optimize()` returns a dictionary with keys: `current_monthly_spend` (float), `potential_monthly_savings` (float), `optimized_monthly_spend` (float), `savings_percentage` (float), `recommendations` (list of dicts with `service`, `type`, `issue`, `recommendation`, `potential_savings`, `priority`), and `priority_actions` (top 5 high-priority recommendations sorted by savings).
