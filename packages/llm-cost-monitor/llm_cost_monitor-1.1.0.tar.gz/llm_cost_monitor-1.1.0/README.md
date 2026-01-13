# LLM Cost Monitor - Python SDK

Official Python SDK for [LLM Cost Monitor](https://github.com/check-ai/llm-cost-monitor).

## Installation

```bash
pip install llm-cost-monitor
# or
uv add llm-cost-monitor
```

## Quick Start

```python
from llm_cost_monitor import ApiClient, Configuration, EventsApi
from llm_cost_monitor.models import CreateEventRequest

config = Configuration(host="http://localhost:8080")
config.api_key["ApiKeyAuth"] = "Bearer YOUR_API_KEY"

with ApiClient(config) as client:
    events = EventsApi(client)
    
    response = events.create_event(
        CreateEventRequest(
            trace_id="unique-request-id",
            provider="openai",
            model="gpt-4o",
            input_tokens=1200,
            output_tokens=350,
            feature="chat",
            user_id="user_123",
        )
    )
    
    print(f"Cost: ${response.cost_usd}")
```

## Authentication

```python
from llm_cost_monitor import Configuration

config = Configuration(host=os.getenv("LLM_COST_MONITOR_URL"))
config.api_key["ApiKeyAuth"] = f"Bearer {os.getenv('LLM_COST_MONITOR_API_KEY')}"
```

## API Reference

### Events API

```python
from llm_cost_monitor import EventsApi
from llm_cost_monitor.models import CreateEventRequest

events = EventsApi(client)

# Create event
result = events.create_event(
    CreateEventRequest(
        trace_id="req_abc123",
        provider="openai",
        model="gpt-4o",
        input_tokens=1200,
        output_tokens=350,
    )
)

# List events
event_list = events.list_events(limit=50)
```

### Metrics API

```python
from llm_cost_monitor import MetricsApi

metrics = MetricsApi(client)

# Get aggregated metrics
data = metrics.get_metrics(period="hour")

# Get usage summary
usage = metrics.get_usage(period="month")
```

### Alerts API

```python
from llm_cost_monitor import AlertsApi
from llm_cost_monitor.models import CreateAlertRequest

alerts = AlertsApi(client)

# Create alert
alerts.create_alert(
    CreateAlertRequest(threshold=100.0, window_interval="24h")
)

# List alerts
alert_list = alerts.list_alerts()

# Delete alert
alerts.delete_alert(id="alert-uuid")
```

### Pricing API

```python
from llm_cost_monitor import PricingApi

pricing = PricingApi(client)

# List all pricing
prices = pricing.list_pricing()

# Filter by provider
openai_prices = pricing.list_pricing(provider="openai")
```

## FastAPI Middleware Example

```python
from fastapi import FastAPI, Request
from llm_cost_monitor import ApiClient, Configuration, EventsApi
from llm_cost_monitor.models import CreateEventRequest
import uuid

app = FastAPI()

config = Configuration(host="http://localhost:8080")
config.api_key["ApiKeyAuth"] = "Bearer YOUR_API_KEY"

@app.middleware("http")
async def track_llm_costs(request: Request, call_next):
    response = await call_next(request)
    
    # If this request used LLM, track it
    if hasattr(request.state, "llm_usage"):
        usage = request.state.llm_usage
        
        with ApiClient(config) as client:
            events = EventsApi(client)
            events.create_event(
                CreateEventRequest(
                    trace_id=str(uuid.uuid4()),
                    provider=usage["provider"],
                    model=usage["model"],
                    input_tokens=usage["input_tokens"],
                    output_tokens=usage["output_tokens"],
                    feature=request.url.path,
                )
            )
    
    return response
```

## Background Worker Example

```python
import asyncio
from llm_cost_monitor import ApiClient, Configuration, EventsApi
from llm_cost_monitor.models import CreateEventRequest

async def track_costs_batch(events_batch: list):
    config = Configuration(host="http://localhost:8080")
    config.api_key["ApiKeyAuth"] = "Bearer YOUR_API_KEY"
    
    with ApiClient(config) as client:
        events = EventsApi(client)
        
        for event in events_batch:
            try:
                events.create_event(
                    CreateEventRequest(**event)
                )
            except Exception as e:
                print(f"Failed to track event: {e}")

# Usage
asyncio.run(track_costs_batch([
    {"trace_id": "1", "provider": "openai", "model": "gpt-4o", "input_tokens": 100, "output_tokens": 50},
    {"trace_id": "2", "provider": "anthropic", "model": "claude-3-5-sonnet", "input_tokens": 200, "output_tokens": 100},
]))
```

## Error Handling

```python
from llm_cost_monitor.exceptions import ApiException

try:
    events.create_event(...)
except ApiException as e:
    print(f"Error {e.status}: {e.body}")
    
    # Handle budget exceeded
    if e.status == 402:
        print("Budget limit exceeded!")
```

## Environment Variables

```bash
LLM_COST_MONITOR_URL=http://localhost:8080
LLM_COST_MONITOR_API_KEY=your-api-key
```

## License

MIT
