# Cost Optimization Agent - User Manual

## Table of Contents
1. [Introduction](#1-introduction)
2. [What is the Cost Optimization Agent?](#2-what-is-the-cost-optimization-agent)
3. [How to Access the Agent](#3-how-to-access-the-agent)
4. [What You Can Ask](#4-what-you-can-ask)
5. [Sample Conversations](#5-sample-conversations)
6. [Understanding the Responses](#6-understanding-the-responses)
7. [Monitoring and Logs](#7-monitoring-and-logs)
8. [Troubleshooting](#8-troubleshooting)
9. [Cost Information](#9-cost-information)
10. [Cleanup Instructions](#10-cleanup-instructions)

---

## 1. Introduction

This user manual explains how to use your deployed **Cost Optimization Agent** - an AI-powered assistant that helps you understand and optimize your AWS spending. The agent uses Claude 3.5 Sonnet to intelligently analyze your AWS costs and provide actionable recommendations.

### Deployment Details

| Property | Value |
|----------|-------|
| **Agent Name** | cost_optimization_agent |
| **Runtime ID** | cost_optimization_agent-7cv8wY7ZMf |
| **Region** | us-east-2 (Ohio) |
| **Status** | READY |

---

## 2. What is the Cost Optimization Agent?

The Cost Optimization Agent is an AI assistant deployed on **Amazon Bedrock AgentCore Runtime**. It can:

- **Analyze your AWS costs** - View spending by service, time period, or category
- **Detect anomalies** - Identify unusual spending patterns
- **Forecast costs** - Predict future spending based on historical data
- **Review budgets** - Check your AWS budget status and alerts
- **Provide recommendations** - Suggest ways to reduce costs

### Architecture Overview

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   Your Query    │────▶│  AgentCore Runtime   │────▶│  Claude 3.5     │
│                 │     │  (Serverless)        │     │  Sonnet         │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
                                  │
                                  ▼
                        ┌──────────────────────┐
                        │    AWS Services      │
                        │  - Cost Explorer     │
                        │  - Budgets           │
                        │  - CloudWatch        │
                        └──────────────────────┘
```

### Available Tools

The agent has access to these tools to answer your questions:

| Tool | Purpose |
|------|---------|
| `get_cost_and_usage` | Retrieve cost data for any time period |
| `get_service_costs` | Get breakdown by AWS service |
| `get_cost_forecast` | Predict future spending |
| `detect_cost_anomalies` | Find unusual spending patterns |
| `get_all_budgets` | View budget status and alerts |

---

## 3. How to Access the Agent

### Method 1: Using the Test Script (Recommended)

Run the provided test script to interact with the agent:

```bash
cd d:\Amazon_bedrock\amazon-bedrock-agentcore-samples\02-use-cases\cost-optimization-agent
python test_agentcore_runtime.py
```

### Method 2: Using Python Code

```python
import boto3
import json

# Initialize the client
client = boto3.client("bedrock-agentcore", region_name="us-east-2")

# Send a query
response = client.invoke_agent_runtime(
    agentRuntimeArn="arn:aws:bedrock-agentcore:us-east-2:075296829739:runtime/cost_optimization_agent-7cv8wY7ZMf",
    qualifier="DEFAULT",
    payload=json.dumps({"prompt": "What are my top 3 expensive services?"})
)

# Process the streaming response
for line in response["response"].iter_lines():
    if line:
        print(line.decode("utf-8"))
```

### Method 3: Using AWS CLI

```bash
aws bedrock-agentcore invoke-agent-runtime \
    --agent-runtime-arn "arn:aws:bedrock-agentcore:us-east-2:075296829739:runtime/cost_optimization_agent-7cv8wY7ZMf" \
    --qualifier "DEFAULT" \
    --payload '{"prompt": "Show my current month costs"}' \
    --region us-east-2
```

---

## 4. What You Can Ask

### Cost Analysis Questions

| Question Type | Example Queries |
|--------------|-----------------|
| **Current Spending** | "What are my current month costs?" |
| | "How much have I spent this week?" |
| | "What's my total AWS bill?" |
| **Service Breakdown** | "What are my top 5 expensive services?" |
| | "How much am I spending on EC2?" |
| | "Show me costs by service" |
| **Time Comparisons** | "Compare my costs this month vs last month" |
| | "Show me daily spending for the past week" |
| | "What was my spending in December?" |

### Anomaly Detection Questions

| Question Type | Example Queries |
|--------------|-----------------|
| **Unusual Spending** | "Are my costs higher than usual?" |
| | "Detect any cost anomalies" |
| | "Has anything spiked recently?" |
| **Trend Analysis** | "Is my spending trending up or down?" |
| | "Are there any concerning patterns?" |

### Forecasting Questions

| Question Type | Example Queries |
|--------------|-----------------|
| **Future Costs** | "What will my costs be next month?" |
| | "Forecast my spending for the next 30 days" |
| | "Predict my end-of-month bill" |

### Budget Questions

| Question Type | Example Queries |
|--------------|-----------------|
| **Budget Status** | "Show me my budget status" |
| | "Am I over budget?" |
| | "List all my AWS budgets" |
| | "How much budget do I have left?" |

### Optimization Questions

| Question Type | Example Queries |
|--------------|-----------------|
| **Recommendations** | "How can I reduce my EC2 costs?" |
| | "What services should I optimize?" |
| | "Give me cost saving tips" |

---

## 5. Sample Conversations

### Example 1: Quick Cost Check

**You:** "What are my current costs?"

**Agent:**
```
Based on my analysis of your AWS costs for the current month:

Your month-to-date spending is $33.78, with the following breakdown:
- EC2-Other: $25.83 (76%)
- Amazon Lightsail: $3.85 (11%)
- Amazon VPC: $2.87 (8%)
- Amazon SageMaker: $1.03 (3%)
- Other services: $0.10 (2%)

Your daily average is approximately $1.25/day, which projects to
around $38-40 for the full month.

Would you like me to provide optimization recommendations for any
of these services?
```

### Example 2: Anomaly Detection

**You:** "Are my costs higher than usual?"

**Agent:**
```
I've analyzed your spending patterns over the last 7 days:

Good news! No cost anomalies detected. Your spending is stable and
predictable with the following observations:

1. Daily costs are consistent at ~$1.08-$1.25/day
2. No unexpected spikes or unusual charges
3. All services are within normal operating ranges

Your main cost drivers remain:
- EC2-Other: ~$1.08/day
- Lightsail: ~$0.12/day
- VPC: ~$0.12/day

Would you like me to:
1. Look at a longer time period?
2. Set up a budget alert?
3. Generate a cost forecast?
```

### Example 3: Service-Specific Query

**You:** "How much am I spending on Amazon Bedrock?"

**Agent:**
```
Based on the cost data for the last 30 days, you have no recorded
spending on Amazon Bedrock.

This could mean:
1. You haven't used Amazon Bedrock services yet
2. Your usage is within the free tier limits
3. The charges haven't been processed yet

Would you like me to:
1. Check a different time period?
2. Show you what services you ARE using?
3. Explain Amazon Bedrock pricing?
```

---

## 6. Understanding the Responses

### Response Format

The agent provides responses in a conversational format with:

1. **Direct Answer** - The specific information you requested
2. **Context** - Relevant background or comparisons
3. **Recommendations** - Actionable suggestions when applicable
4. **Follow-up Options** - Additional queries you might find helpful

### Cost Data Sources

The agent retrieves data from:

| Source | Data Type | Latency |
|--------|-----------|---------|
| AWS Cost Explorer | Historical costs | ~24 hours |
| AWS Budgets | Budget status | Real-time |
| Cost Anomaly Detection | Anomalies | ~24 hours |

**Note:** Cost data typically has a 24-hour delay. Today's costs may not appear until tomorrow.

### Understanding Service Names

| Service Name | What It Means |
|--------------|---------------|
| EC2-Other | EC2-related costs (EBS, snapshots, data transfer) |
| Amazon EC2 | Compute instance hours |
| Amazon S3 | Storage and data transfer |
| Amazon VPC | NAT Gateway, VPN, data transfer |
| AWS Lambda | Serverless function executions |

---

## 7. Monitoring and Logs

### CloudWatch Dashboard

View the GenAI Observability Dashboard:
```
https://console.aws.amazon.com/cloudwatch/home?region=us-east-2#gen-ai-observability/agent-core
```

### View Agent Logs

**Using AWS CLI:**
```bash
# Tail logs in real-time
aws logs tail /aws/bedrock-agentcore/runtimes/cost_optimization_agent-7cv8wY7ZMf-DEFAULT --follow --region us-east-2

# View last hour of logs
aws logs tail /aws/bedrock-agentcore/runtimes/cost_optimization_agent-7cv8wY7ZMf-DEFAULT --since 1h --region us-east-2
```

**Using AWS Console:**
1. Go to CloudWatch > Log Groups
2. Find: `/aws/bedrock-agentcore/runtimes/cost_optimization_agent-7cv8wY7ZMf-DEFAULT`
3. Click on the log stream to view entries

### X-Ray Traces

View request traces for debugging:
1. Go to CloudWatch > X-Ray traces
2. Filter by service: `cost_optimization_agent`

---

## 8. Troubleshooting

### Common Issues

#### Issue: "No endpoint or agent found"

**Symptoms:**
```
ResourceNotFoundException: No endpoint or agent found with qualifier 'DEFAULT'
```

**Solutions:**
1. Verify the agent is running:
   ```bash
   aws bedrock-agentcore-control get-agent-runtime \
       --agent-runtime-id cost_optimization_agent-7cv8wY7ZMf \
       --region us-east-2
   ```
2. Wait 30 seconds and retry - the endpoint may be initializing
3. Check if the agent was deleted

#### Issue: Slow Response Times

**Possible Causes:**
- Cold start (first request after idle period)
- Large data queries
- Network latency

**Solutions:**
- First requests may take 5-10 seconds due to cold start
- Subsequent requests are faster (1-3 seconds)

#### Issue: "Access Denied" Errors

**Solutions:**
1. Verify your AWS credentials are configured
2. Check that your IAM user/role has `bedrock-agentcore:InvokeAgentRuntime` permission
3. Ensure you're using the correct region (us-east-2)

#### Issue: Empty or No Cost Data

**Possible Causes:**
- Cost Explorer not enabled
- No AWS usage in the time period
- Data delay (24 hours)

**Solutions:**
1. Enable Cost Explorer in AWS Console > Billing
2. Wait 24 hours for initial data
3. Try querying a previous month

### Getting Help

If issues persist:
1. Check CloudWatch logs for error details
2. Verify all AWS resources are in READY state
3. Review the IAM role permissions

---

## 9. Cost Information

### Agent Operating Costs

| Resource | Cost Model | Estimated Monthly Cost |
|----------|------------|------------------------|
| AgentCore Runtime | Per invocation | ~$0.001-0.01 per request |
| Claude 3.5 Sonnet | Per token | ~$0.003/1K input, $0.015/1K output |
| CloudWatch Logs | Per GB ingested | ~$0.50/GB |
| ECR Storage | Per GB/month | ~$0.10/GB |

### Cost Estimate Example

For 100 queries per month with average response length:
- AgentCore: ~$1
- Claude tokens: ~$2-5
- Logs: ~$0.50
- **Total: ~$3-7/month**

### Minimizing Costs

1. **Delete when not needed** - Run cleanup script
2. **Use concise queries** - Shorter prompts = fewer tokens
3. **Batch questions** - Ask multiple things in one query

---

## 10. Cleanup Instructions

When you're done using the agent, remove all resources to stop incurring costs.

### Automated Cleanup

```bash
cd d:\Amazon_bedrock\amazon-bedrock-agentcore-samples\02-use-cases\cost-optimization-agent
python cleanup.py --region us-east-2
```

### Manual Cleanup

If the script doesn't work, delete resources manually:

1. **Delete AgentCore Runtime:**
   ```bash
   aws bedrock-agentcore-control delete-agent-runtime \
       --agent-runtime-id cost_optimization_agent-7cv8wY7ZMf \
       --region us-east-2
   ```

2. **Delete ECR Repository:**
   ```bash
   aws ecr delete-repository \
       --repository-name bedrock-agentcore-cost_optimization_agent \
       --force \
       --region us-east-2
   ```

3. **Delete IAM Role:**
   ```bash
   # First delete inline policies
   aws iam delete-role-policy \
       --role-name CostOptimizationAgentRole \
       --policy-name CostOptimizationAgentPolicy

   # Then delete the role
   aws iam delete-role --role-name CostOptimizationAgentRole
   ```

4. **Delete S3 Bucket (CodeBuild sources):**
   ```bash
   aws s3 rb s3://bedrock-agentcore-codebuild-sources-075296829739-us-east-2 --force
   ```

5. **Delete CloudWatch Log Group:**
   ```bash
   aws logs delete-log-group \
       --log-group-name /aws/bedrock-agentcore/runtimes/cost_optimization_agent-7cv8wY7ZMf-DEFAULT \
       --region us-east-2
   ```

---

## Quick Reference Card

### Agent Details
```
Runtime ARN: arn:aws:bedrock-agentcore:us-east-2:075296829739:runtime/cost_optimization_agent-7cv8wY7ZMf
Region: us-east-2
Status: READY
```

### Quick Commands

| Action | Command |
|--------|---------|
| Test Agent | `python test_agentcore_runtime.py` |
| View Logs | `aws logs tail /aws/bedrock-agentcore/runtimes/cost_optimization_agent-7cv8wY7ZMf-DEFAULT --follow` |
| Check Status | `aws bedrock-agentcore-control get-agent-runtime --agent-runtime-id cost_optimization_agent-7cv8wY7ZMf` |
| Cleanup | `python cleanup.py --region us-east-2` |

### Useful Links

- [CloudWatch Dashboard](https://console.aws.amazon.com/cloudwatch/home?region=us-east-2#gen-ai-observability/agent-core)
- [Cost Explorer](https://console.aws.amazon.com/cost-management/home#/cost-explorer)
- [Bedrock Console](https://console.aws.amazon.com/bedrock/home?region=us-east-2)

---

*Document Version: 1.0*
*Last Updated: January 2026*
*Agent Version: cost_optimization_agent-7cv8wY7ZMf*
