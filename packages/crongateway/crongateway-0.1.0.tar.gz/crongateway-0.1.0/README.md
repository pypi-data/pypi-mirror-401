# CronGateway Python SDK

Official Python client for the CronGateway AI Platform.

## Installation

```bash
pip install crongateway
```

## Quick Start

```python
from crongateway import CronGatewayClient

# Initialize the client
client = CronGatewayClient(api_key="your-api-key")

# Create a job
job = client.create_job(
    tool_id="flux-pro",
    input={
        "prompt": "A beautiful sunset over mountains",
        "aspect_ratio": "16:9"
    }
)

# Check job status
status = client.get_job(job["id"])
print(f"Job status: {status['status']}")

# List all available models
tools = client.list_tools()
for tool in tools:
    print(f"{tool['name']}: ${tool['costPerRun']} per run")
```

## API Reference

### Jobs

#### `create_job(tool_id: str, input: dict) -> dict`
Create a new AI job.

#### `get_job(job_id: str) -> dict`
Get job details by ID.

#### `list_jobs() -> list`
List all jobs for the authenticated user.

### Tools

#### `list_tools() -> list`
List all available AI models/tools.

#### `get_tool(tool_id: str) -> dict`
Get a specific tool by ID.

#### `search_tools(query: str) -> list`
Search tools by name or description.

#### `get_tools_by_category(category: str) -> list`
Get tools filtered by category (Text, Image, Video, Audio).

### Storage

#### `list_artifacts() -> list`
List all generated artifacts.

#### `upload_file(file_path: str) -> dict`
Upload a file to CronGateway storage.

### Billing

#### `top_up(amount: float) -> dict`
Add credits to your account.

#### `get_billing_history() -> list`
Get billing transaction history.

#### `get_usage_stats() -> dict`
Get usage analytics and statistics.

## Examples

### Image Generation

```python
client = CronGatewayClient(api_key="your-api-key")

# Generate an image with FLUX Pro
job = client.create_job(
    tool_id="flux-pro",
    input={
        "prompt": "A futuristic cityscape at night, neon lights",
        "aspect_ratio": "16:9"
    }
)

# Poll for completion
import time
while True:
    status = client.get_job(job["id"])
    if status["status"] == "COMPLETED":
        print(f"Image URL: {status['output']['image_url']}")
        break
    elif status["status"] == "FAILED":
        print(f"Job failed: {status.get('error')}")
        break
    time.sleep(2)
```

### Text Generation

```python
client = CronGatewayClient(api_key="your-api-key")

# Generate text with Gemini
job = client.create_job(
    tool_id="gemini-2.5-flash-preview",
    input={
        "prompt": "Explain quantum computing in simple terms"
    }
)

status = client.get_job(job["id"])
if status["status"] == "COMPLETED":
    print(status["output"]["text"])
```

### Virtual Try-On (Cron TRY-ON)

```python
client = CronGatewayClient(api_key="your-api-key")

# CronGateway's proprietary virtual try-on model
job = client.create_job(
    tool_id="cron-try-on",
    input={
        "type": "clothing",
        "image1": "https://example.com/person.jpg",
        "image2": "https://example.com/shirt.jpg",
        "prompt": "Make sure the shirt fits naturally"
    }
)

status = client.get_job(job["id"])
if status["status"] == "COMPLETED":
    print(f"Try-on result: {status['output']['image_url']}")
```

## Error Handling

```python
from crongateway import CronGatewayClient
import requests

client = CronGatewayClient(api_key="your-api-key")

try:
    job = client.create_job("flux-pro", {"prompt": "test"})
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Invalid API key")
    elif e.response.status_code == 402:
        print("Insufficient credits")
    else:
        print(f"Error: {e}")
```

## License

MIT

