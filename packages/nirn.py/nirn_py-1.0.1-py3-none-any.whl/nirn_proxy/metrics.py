"""Prometheus metrics for monitoring proxy performance."""
import logging
from prometheus_client import Counter, Histogram, Gauge, start_http_server, REGISTRY


logger = logging.getLogger(__name__)


# Error counter
error_counter = Counter(
    'nirn_proxy_error',
    'The total number of errors when processing requests'
)

# Request histogram with timing buckets
request_histogram = Histogram(
    'nirn_proxy_requests',
    'Request histogram',
    ['method', 'status', 'route', 'clientId'],
    buckets=[0.1, 0.25, 1, 2.5, 5, 20]
)

# Connections gauge
open_connections = Gauge(
    'nirn_proxy_open_connections',
    'Gauge for client connections currently open with the proxy',
    ['method', 'route']
)

# Routed request counters
requests_routed_sent = Counter(
    'nirn_proxy_requests_routed_sent',
    'Counter for requests routed from this node into other nodes'
)

requests_routed_received = Counter(
    'nirn_proxy_requests_routed_received',
    'Counter for requests received from other nodes'
)

requests_routed_error = Counter(
    'nirn_proxy_requests_routed_error',
    'Counter for failed requests routed from this node'
)


def start_metrics_server(bind_ip: str, port: int):
    """Start Prometheus metrics server."""
    logger.info(f"Starting metrics server on {bind_ip}:{port}")
    try:
        start_http_server(port, addr=bind_ip)
    except Exception as e:
        logger.error(f"Failed to start metrics server: {e}")
        raise