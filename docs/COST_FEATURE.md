# Cost Gateway - Cost Feature

This document describes the cost monitoring and exposure feature added to cost-gateway.

## Overview

Cost Gateway can now monitor and expose energy and cloud costs to Prometheus using a sinusoidal simulator. This allows you to simulate cost patterns without integrating with real cost sources.

## Configuration

Add a `cost` section to your `config.yaml`:

```yaml
prometheus:
  endpoint_port: 8085
cost:
  enabled: true
  sources:
    energy:
      min_cost: 0.1
      max_cost: 0.5
      peak_time: 43200  # Unix timestamp for peak
    cloud:
      min_cost: 100.0
      max_cost: 500.0
      peak_time: 21600  # Unix timestamp for peak
```

### Configuration Parameters

- **enabled**: Set to `true` to enable cost monitoring
- **sources**: Dictionary of cost sources to monitor
  - **name**: Unique identifier for the cost source (e.g., "energy", "cloud")
    - **min_cost**: Minimum cost value
    - **max_cost**: Maximum cost value  
    - **peak_time**: Unix timestamp when cost should be at maximum
    - **period**: Cost cycle period in seconds (default: 86400 = 24 hours)

## Simulation Algorithm

Cost values are calculated using a sinusoidal function:

```
cost = min_cost + (max_cost - min_cost) * (1 + cos(angle)) / 2
```

Where `angle` is based on the time elapsed since `peak_time` within the configured period.

This creates a smooth oscillation between `min_cost` and `max_cost` with:
- Peak at: `peak_time` (and every `period` seconds after)
- Valley at: `peak_time + period/2` (and every `period` seconds after)

## Prometheus Metrics

Cost metrics are exposed as Prometheus Gauges with the following label:

- **source**: The cost source name (from config)

Each metric follows the naming convention: `cost_{name}`

Example metrics:
- `cost_energy` - Energy cost
- `cost_cloud` - Cloud cost

## Usage

1. Configure costs in `config.yaml`
2. Run cost-gateway: `uv run python -m cost_gateway.main --config ./etc/config.yaml`
3. Access metrics at: `http://localhost:8085/metrics`
4. Configure Prometheus to scrape the metrics endpoint

## Real Cost Sources

To integrate real cost sources, implement the `CostSource` interface:

```python
from cost_gateway.cost.source import CostSource

class MyCostSource(CostSource):
    async def get_cost(self, name: str) -> float:
        # Fetch actual cost from your source
        return 0.42
```

Then use it in your context by passing it to `CostService`.

## Unit Tests

Run tests with:
```bash
uv run pytest
```

Test files:
- `test_simulator.py` - Tests for CostSimulator
- `test_metrics.py` - Tests for Prometheus metrics
- `test_cost_service.py` - Tests for CostService
- `test_cost_settings.py` - Tests for configuration loading
- `test_cost_integration.py` - End-to-end integration tests
