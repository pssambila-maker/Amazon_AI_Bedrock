# Amazon Bedrock AgentCore - Cost Optimization Agent Implementation Guide

A step-by-step guide to implementing the Cost Optimization Agent using Amazon Bedrock AgentCore. This guide covers local development, troubleshooting, and deployment to AWS.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Repository Setup](#2-repository-setup)
3. [Understanding the Project Structure](#3-understanding-the-project-structure)
4. [AWS Bedrock Model Access Setup](#4-aws-bedrock-model-access-setup)
5. [Local Development Setup](#5-local-development-setup)
6. [Troubleshooting Common Issues](#6-troubleshooting-common-issues)
7. [Running Local Tests](#7-running-local-tests)
8. [Understanding the Agent Architecture](#8-understanding-the-agent-architecture)
9. [Deploying to AgentCore Runtime](#9-deploying-to-agentcore-runtime)
10. [Testing the Deployed Agent](#10-testing-the-deployed-agent)
11. [Cleanup](#11-cleanup)
12. [Key Learnings](#12-key-learnings)

---

## 1. Prerequisites

### Software Requirements

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Python | 3.10 or higher | `python --version` |
| AWS CLI | 2.x | `aws --version` |
| Git | Any recent version | `git --version` |

### AWS Requirements

- AWS Account with administrator access (or specific permissions listed below)
- AWS CLI configured with valid credentials
- AWS Cost Explorer enabled in your account (may take 24 hours after first enabling)

### Required AWS Permissions

```
bedrock:InvokeModel
bedrock:GetFoundationModelAvailability
ce:* (Cost Explorer)
budgets:* (Budget management)
iam:* (for creating execution roles)
bedrock-agentcore:* (for AgentCore operations)
ecr:* (for container registry)
codebuild:* (for building containers)
```

### Verify AWS Configuration

```bash
# Check AWS CLI is configured
aws configure list

# Check current region
aws configure get region

# Verify credentials work
aws sts get-caller-identity
```

---

## 2. Repository Setup

### Step 2.1: Clone the Repository

```bash
# Navigate to your working directory
cd D:\Amazon_bedrock

# Clone the Amazon Bedrock AgentCore samples repository
git clone https://github.com/awslabs/amazon-bedrock-agentcore-samples.git

# Navigate to the cloned repository
cd amazon-bedrock-agentcore-samples
```

### Step 2.2: Verify Repository Structure

```bash
# List main folders
ls -la

# You should see:
# 01-tutorials/    - Learning tutorials for AgentCore
# 02-use-cases/    - Production-ready use case implementations
# 03-integrations/ - Framework and protocol integrations
```

---

## 3. Understanding the Project Structure

### Repository Overview

```
amazon-bedrock-agentcore-samples/
├── 01-tutorials/           # Step-by-step tutorials
│   ├── 01-AgentCore-runtime/
│   └── ...
├── 02-use-cases/           # Production use cases (22 total)
│   ├── cost-optimization-agent/    # <-- Our focus
│   ├── customer-support-assistant/
│   ├── SRE-agent/
│   └── ...
└── 03-integrations/        # Framework integrations
```

### Cost Optimization Agent Structure

```
02-use-cases/cost-optimization-agent/
├── cost_optimization_agent.py   # Main agent code
├── deploy.py                    # Deployment script
├── cleanup.py                   # Resource cleanup script
├── test_local.py               # Local test suite
├── test_agentcore_runtime.py   # Deployed agent test
├── requirements.txt            # Python dependencies
├── tools/                      # Agent tools
│   ├── cost_explorer_tools.py  # AWS Cost Explorer integration
│   └── budget_tools.py         # AWS Budgets integration
├── README.md                   # Project documentation
├── ARCHITECTURE.md             # Architecture details
└── DEPLOYMENT.md               # Deployment guide
```

---

## 4. AWS Bedrock Model Access Setup

This is a critical step. The Cost Optimization Agent uses Claude 3.5 Sonnet, which requires explicit access in AWS Bedrock.

### Step 4.1: Navigate to Bedrock Console

1. Open AWS Console: https://console.aws.amazon.com/bedrock/
2. Ensure you're in the correct region (e.g., us-east-2)
3. Click on **Model access** in the left sidebar

### Step 4.2: Enable Claude 3.5 Sonnet

1. Click **Manage model access**
2. Find **Anthropic** section
3. Select **Claude 3.5 Sonnet v2**
4. Click **Request model access**

### Step 4.3: Complete the Use Case Agreement Form

This is required for Anthropic models:

1. **Company Name**: Your company or "Personal/Learning"
2. **Use Case Description**: "Learning AWS Bedrock and building cost optimization tools for AWS spending analysis"
3. **Website**: Optional
4. Click **Submit**

### Step 4.4: Verify Model Access

Wait a few minutes, then verify access:

```bash
# Check model availability
aws bedrock get-foundation-model-availability \
    --model-id anthropic.claude-3-5-sonnet-20241022-v2:0

# Expected output should show:
# "agreementAvailability": { "status": "AVAILABLE" }
```

### Step 4.5: Test Model Access in Console (Optional)

1. Go to Bedrock Console > **Playgrounds** > **Chat**
2. Select **Claude 3.5 Sonnet v2**
3. Type a test message: "Hello, what can you help me with?"
4. If you get a response, model access is working

---

## 5. Local Development Setup

### Step 5.1: Navigate to the Project

```bash
cd amazon-bedrock-agentcore-samples/02-use-cases/cost-optimization-agent
```

### Step 5.2: Install Dependencies

```bash
# Using pip (standard)
pip install -r requirements.txt

# OR using uv (faster, recommended)
pip install uv
uv sync
```

### Step 5.3: Fix the Model ID (Important!)

The default code uses a cross-region inference profile that may not work. Update the model ID:

**File**: `cost_optimization_agent.py` (Line 20)

**Change FROM:**
```python
MODEL_ID = os.getenv("MODEL_ID", "us.anthropic.claude-3-5-sonnet-20241022-v2:0")
```

**Change TO:**
```python
MODEL_ID = os.getenv("MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")
```

This removes the `us.` prefix which is for cross-region inference profiles.

---

## 6. Troubleshooting Common Issues

### Issue 1: "Model use case details have not been submitted"

**Error:**
```
ResourceNotFoundException: Model use case details have not been submitted for this account.
```

**Solution:**
1. Go to Bedrock Console > Model Access
2. Complete the Anthropic use case agreement form
3. Wait 15 minutes for approval

### Issue 2: "agreementAvailability: NOT_AVAILABLE"

**Cause:** Use case form not completed

**Verify with:**
```bash
aws bedrock get-foundation-model-availability \
    --model-id anthropic.claude-3-5-sonnet-20241022-v2:0
```

**Solution:** Complete the use case form in Step 4.3

### Issue 3: Cross-Region Inference Profile Error

**Error:**
```
Model id: us.anthropic.claude-3-5-sonnet-20241022-v2:0 not found
```

**Solution:** Change the model ID as shown in Step 5.3

### Issue 4: Unicode Encoding Error on Windows

**Error:**
```
UnicodeEncodeError: 'charmap' codec can't encode characters
```

**Solution:** Create a wrapper script or set encoding:

```python
# Add at the top of your test script
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
```

### Issue 5: Cost Explorer Access Denied

**Error:**
```
AccessDeniedException: Cost Explorer not enabled
```

**Solution:**
1. Go to AWS Console > Billing > Cost Explorer
2. Enable Cost Explorer
3. Wait 24 hours for data to populate

### Issue 6: ZIP Timestamp Error on Windows

**Error:**
```
ValueError: ZIP does not support timestamps before 1980
```

**Cause:** Windows may have files (like `nul` device references) with epoch timestamps (1970).

**Solution:** Add this patch at the top of `deploy.py`:

```python
# Fix for Windows: Patch zipfile to handle timestamps before 1980
import zipfile
import os as _os

_original_from_file = zipfile.ZipInfo.from_file

@classmethod
def _patched_from_file(cls, filename, arcname=None, *, strict_timestamps=True):
    """Patched version that handles timestamps before 1980."""
    try:
        return _original_from_file.__func__(cls, filename, arcname, strict_timestamps=strict_timestamps)
    except ValueError as e:
        if "timestamps before 1980" in str(e):
            arcname = arcname or filename
            while arcname and arcname[0] in ("/", "\\"):
                arcname = arcname[1:]
            info = cls(arcname, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            try:
                st = _os.stat(filename)
                if _os.path.isdir(filename):
                    info.external_attr = 0o40755 << 16
                    info.file_size = 0
                else:
                    info.external_attr = 0o644 << 16
                    info.file_size = st.st_size
            except OSError:
                info.external_attr = 0o644 << 16
                info.file_size = 0
            return info
        raise

zipfile.ZipInfo.from_file = _patched_from_file
```

### Issue 7: Model ID Difference Between Local and Deployed

**Important:** The model ID requirements differ between local testing and AgentCore Runtime deployment:

| Environment | Model ID |
|-------------|----------|
| **Local Testing** | `anthropic.claude-3-5-sonnet-20241022-v2:0` (direct model ID) |
| **AgentCore Runtime** | `us.anthropic.claude-3-5-sonnet-20241022-v2:0` (inference profile) |

**Error when using direct model ID in AgentCore:**
```
ValidationException: Invocation of model ID anthropic.claude-3-5-sonnet-20241022-v2:0
with on-demand throughput isn't supported. Retry your request with the ID or ARN of
an inference profile that contains this model.
```

**Solution:** For deployment, use the inference profile with the `us.` prefix.

### Issue 8: Wrong Region in Test Script

**Error:**
```
ResourceNotFoundException: No endpoint or agent found with qualifier 'DEFAULT'
```

**Cause:** The test script (`test_agentcore_runtime.py`) may be using the wrong region.

**Solution:** Update the region in `test_agentcore_runtime.py` line 30:
```python
client = boto3.client("bedrock-agentcore", region_name="us-east-2")  # Match your deployment region
```

---

## 7. Running Local Tests

### Step 7.1: Create a Simple Test Script (Windows-Compatible)

Create `run_test.py` in the cost-optimization-agent folder:

```python
"""
Simple test wrapper for Windows compatibility
"""
import sys
import io

# Set UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import asyncio
from cost_optimization_agent import process_request


async def test_query(query: str, description: str):
    """Test a single query and display results"""
    print(f"\n{'=' * 80}")
    print(f"TEST: {description}")
    print(f"{'=' * 80}")
    print(f"Query: {query}\n")
    print("Response:")
    print("-" * 80)

    payload = {"prompt": query}

    full_response = []
    async for chunk in process_request(payload):
        if chunk.get("type") == "chunk":
            data = chunk.get("data", "")
            print(data, end="", flush=True)
            full_response.append(data)
        elif chunk.get("error"):
            print(f"\nError: {chunk['error']}")
            return

    print("\n" + "=" * 80 + "\n")
    return "".join(full_response)


async def main():
    """Run a simple test"""
    print("\n" + "=" * 80)
    print("COST OPTIMIZATION AGENT - LOCAL TEST")
    print("=" * 80 + "\n")

    # Test 1: Simple cost query
    await test_query(
        "Are my costs higher than usual?",
        "Natural Language Understanding - Anomaly Detection"
    )

    print("\nTest completed!")


if __name__ == "__main__":
    asyncio.run(main())
```

### Step 7.2: Run the Test

```bash
python run_test.py
```

### Step 7.3: Expected Output

```
================================================================================
COST OPTIMIZATION AGENT - LOCAL TEST
================================================================================

================================================================================
TEST: Natural Language Understanding - Anomaly Detection
================================================================================
Query: Are my costs higher than usual?

Response:
--------------------------------------------------------------------------------
I'll help you check for any unusual spending patterns in your AWS costs...

Based on the analysis of your AWS costs:

1. There are no unusual cost spikes or anomalies detected in the last 7 days.

2. Your daily costs have been very consistent throughout the month, with the main contributors being:
   - EC2-Other: ~$1.08/day
   - Amazon Lightsail: ~$0.12/day
   - Amazon Virtual Private Cloud: ~$0.12/day
   - Amazon SageMaker: ~$0.06/day

3. The total cost for the month so far is $33.78.

Your spending appears to be stable and predictable...
================================================================================

Test completed!
```

### Step 7.4: Additional Test Queries

Try these queries to explore the agent's capabilities:

```python
# Budget status
"What's my current budget status?"

# Service breakdown
"Show me my top 3 most expensive services"

# Specific service
"How much am I spending on Amazon Bedrock?"

# Cost reduction
"I need to cut my AWS bill by 20%. What should I do?"

# Forecasting
"Forecast my spending for next month"
```

---

## 8. Understanding the Agent Architecture

### Agent Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cost Optimization Agent                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │   Strands   │    │   Claude    │    │    AWS Cost APIs    │ │
│  │  Framework  │───▶│ 3.5 Sonnet  │───▶│  (Cost Explorer,    │ │
│  │             │    │             │    │   Budgets, etc.)    │ │
│  └─────────────┘    └─────────────┘    └─────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### The 5 Agent Tools

| Tool | Function | AWS API |
|------|----------|---------|
| `analyze_cost_anomalies` | Detect unusual spending patterns | Cost Explorer Anomaly Detection |
| `get_budget_information` | Retrieve budget status | AWS Budgets |
| `forecast_future_costs` | Predict future spending | Cost Explorer Forecast |
| `get_service_cost_breakdown` | Cost by service | Cost Explorer |
| `get_current_month_costs` | Daily cost breakdown | Cost Explorer |

### How Tool Selection Works

1. User asks a question in natural language
2. Claude 3.5 Sonnet analyzes the intent
3. Claude selects appropriate tool(s) to call
4. Tools execute and return data
5. Claude synthesizes results into a response

---

## 9. Deploying to AgentCore Runtime

### Step 9.1: Review Deployment Script

The `deploy.py` script handles:
- Creating IAM roles with necessary permissions
- Building Docker container
- Pushing to Amazon ECR
- Deploying to AgentCore Runtime

### Step 9.2: Run Deployment

```bash
# From the cost-optimization-agent directory
python deploy.py

# Or specify a region
python deploy.py --region us-east-2
```

### Step 9.3: Deployment Process

The script will:
1. Create IAM execution role (`cost-optimization-agent-role`)
2. Build Docker container with agent code
3. Push container to Amazon ECR
4. Deploy to AgentCore Runtime
5. Output the Agent Runtime ID

**Expected output:**
```
Creating IAM role...
Building container...
Pushing to ECR...
Deploying to AgentCore Runtime...

Deployment complete!
Agent Runtime ID: arn:aws:bedrock-agentcore:us-east-2:123456789:agent-runtime/abc123
```

### Step 9.4: Note the Agent Runtime ID

Save the Agent Runtime ID - you'll need it for testing:
```
Agent Runtime ID: <your-agent-runtime-id>
```

---

## 10. Testing the Deployed Agent

### Step 10.1: Run the AgentCore Runtime Test

```bash
python test_agentcore_runtime.py
```

### Step 10.2: Monitor in CloudWatch

View agent logs and metrics:
- **URL**: https://console.aws.amazon.com/cloudwatch/home?region=us-east-2#gen-ai-observability/agent-core

---

## 11. Cleanup

When you're done, clean up AWS resources to avoid ongoing costs:

```bash
# Run cleanup script
python cleanup.py --region us-east-2

# Or manually delete:
# 1. AgentCore Runtime agent
# 2. ECR repository
# 3. IAM roles
# 4. CloudWatch log groups
```

---

## 12. Key Learnings

### What We Learned

1. **Strands Framework**: A Python framework for building LLM-powered agents with tool use
2. **Bedrock Model Access**: Requires both enabling the model AND completing a use case form
3. **Cross-Region Inference**: Use direct model IDs (`anthropic.claude-*`) instead of cross-region profiles (`us.anthropic.claude-*`) for simplicity
4. **AgentCore Runtime**: AWS's managed hosting platform for AI agents

### Architecture Patterns

- **Single Agent Pattern**: One agent with multiple tools (this use case)
- **Tool-Based Design**: LLM selects and orchestrates tool calls
- **Streaming Responses**: Real-time response generation

### Best Practices

1. Always test locally before deploying
2. Use environment variables for configuration
3. Implement proper error handling
4. Clean up resources when done testing

---

## Quick Reference Commands

```bash
# Clone repository
git clone https://github.com/awslabs/amazon-bedrock-agentcore-samples.git

# Navigate to project
cd amazon-bedrock-agentcore-samples/02-use-cases/cost-optimization-agent

# Install dependencies
pip install -r requirements.txt

# Run local test
python run_test.py

# Deploy to AgentCore
python deploy.py --region us-east-2

# Test deployed agent
python test_agentcore_runtime.py

# Cleanup resources
python cleanup.py --region us-east-2
```

---

## Resources

- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [Strands Agents SDK](https://strandsagents.com/)
- [AWS Cost Explorer API](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-api.html)
- [Amazon Bedrock Model Access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)

---

*Guide created during Amazon Bedrock AgentCore learning session*
