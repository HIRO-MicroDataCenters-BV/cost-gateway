from prometheus_client import Gauge

_cost_gauges: dict[str, Gauge] = {}


def get_or_create_gauge(name: str, description: str = "") -> Gauge:
    if name in _cost_gauges:
        return _cost_gauges[name]

    gauge = Gauge(
        name=f"cost_{name}",
        documentation=description or f"Cost for {name}",
        labelnames=["source"],
    )
    _cost_gauges[name] = gauge
    return gauge
