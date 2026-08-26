# Cloud Operations — Troubleshooting & Success Criteria

Read this when a cloud deployment is misbehaving (latency, state locks, failover, IAM, cost spikes, peering, replication) or when defining the success bar for an architecture.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Cross-region latency exceeds 200ms | No regional caching or CDN configured | Deploy CloudFront/Cloud CDN with edge locations closest to user base; enable regional API Gateway caches |
| Terraform state lock conflicts across teams | Shared state backend without proper locking | Use DynamoDB (AWS) or GCS (GCP) state locking with per-team state file partitioning via workspaces |
| Multi-cloud DNS failover not triggering | Health check thresholds too lenient or misconfigured endpoints | Set health check interval to 10s, failure threshold to 3, and verify endpoint returns 200 on the exact path monitored |
| IAM permission errors after cross-account migration | Trust policies not updated for new account IDs | Update AssumeRole trust policies with correct account principals and external IDs; validate with `aws sts assume-role` |
| Cloud costs spike unexpectedly after scaling event | Auto-scaling max limits set too high or no budget alerts | Set hard max instance counts per ASG, configure billing alerts at 80%/100%/120% thresholds, and review Spot fallback behavior |
| VPC peering routes not propagating between clouds | Route tables missing entries for peered CIDR ranges | Add explicit route entries in both VPCs pointing peered CIDRs to the peering connection; verify no overlapping CIDRs |
| DR failover test fails with data inconsistency | Replication lag between primary and secondary regions | Switch to synchronous replication for critical databases or implement application-level consistency checks pre-failover |

## Success Criteria

- **99.99% availability SLA met** across all production workloads with documented uptime reports
- **Cost optimization savings above 25%** compared to on-demand baseline through Reserved Instances, Savings Plans, and right-sizing
- **RTO < 15 minutes and RPO < 1 minute** validated through quarterly DR failover tests
- **Zero critical CIS benchmark findings** in production accounts after security audit remediation
- **Infrastructure drift < 2%** measured by Terraform plan diffs on scheduled compliance scans
- **Cross-region failover completes within 60 seconds** with automated Route 53 health check validation
- **100% resource tagging compliance** enforced via automated policy checks with no untagged resources older than 24 hours
