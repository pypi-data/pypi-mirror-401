# Progress Observability Instrumentation (Python)

Zero-intrusion telemetry for AI agents and LLM apps. Built on Traceloop SDK and OpenTelemetry with a simple one-line init and optional decorators.

## Installation

```bash
pip install progress-observability
```

Or from wheel file:

```bash
pip install progress_observability-x.y.z-py3-none-any.whl
```

## Quick Start

```python
from progress.observability import Observability, ObservabilityInstruments

# Initialize once at process start
Observability.instrument(
    app_name="my-app",
    api_key="<your-api-key>",
    # endpoint="https://collector.observability.progress.com:443"  # Optional: has default
)
```

## Configuration

Environment overrides (optional):

- `OBSERVABILITY_APP_NAME` sets the application name (e.g. "my-app")
- `OBSERVABILITY_ENDPOINT` sets a custom endpoint for collecting data (e.g. "https://collector.observability.progress.com:443")
- `OBSERVABILITY_API_KEY` sets the authentication key to use when sending data
- `OBSERVABILITY_TRACE_CONTENT` when set to "false" will stop sending LLM prompt/responses as part of the telemetry data

Auth headers are added automatically for HTTP(S) endpoints when api_key is provided.

## Package Structure

```text
src/progress/observability/
├── __init__.py        # Package entry point
├── sdk.py             # Main Observability SDK
├── decorators.py      # @task, @workflow, @agent, @tool decorators
├── constants.py       # Environment variables and constants
├── enums.py           # ObservabilityInstruments enum
└── helpers.py         # Helper functions
```
