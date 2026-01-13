# nirn.py

A highly available, transparent & dynamic HTTP proxy that handles Discord rate limits and exports Prometheus metrics.

This is a Python implementation using asyncio and aiohttp for high-performance concurrent request handling.

## Features

- ✅ Highly available, horizontally scalable
- ✅ Transparent ratelimit handling, per-route and global
- ✅ Works with any API version
- ✅ Small resource footprint
- ✅ Works with webhooks
- ✅ Works with Bearer tokens
- ✅ Supports an unlimited number of clients (Bots and Bearer)
- ✅ Prometheus metrics exported out of the box
- ✅ No hardcoded routes, therefore no need of updates for new routes introduced by Discord

## Installation

### From PyPI
```bash
pip install nirn.py
```

### From Source
```bash
git clone https://github.com/lorenzo132/nirn.py
cd nirn.py
pip install -e .
```

### Docker
```bash
docker build -t nirn.py .
docker run -p 8080:8080 -p 9000:9000 nirn.py
```

## Usage

### Command Line
```bash
nirn
```

### Python API
```python
from nirn_proxy import QueueManager, Config

config = Config(
    port=8080,
    log_level="info",
    enable_metrics=True
)

queue_manager = QueueManager(config)
app = queue_manager.create_app()

from aiohttp import web
web.run_app(app, host=config.bind_ip, port=config.port)
```

### Configuration

The proxy sits between the client and Discord. Instead of pointing to discord.com, you point to whatever IP and port the proxy is running on, so `discord.com/api/v9/gateway` becomes `10.0.0.1:8080/api/v9/gateway`.

| Variable | Default | Description |
|----------|---------|-------------|
| LOG_LEVEL | info | Log level (debug, info, warning, error) |
| PORT | 8080 | Proxy port |
| METRICS_PORT | 9000 | Metrics server port |
| ENABLE_METRICS | true | Enable Prometheus metrics |
| BUFFER_SIZE | 50 | Request buffer size per bucket |
| BIND_IP | 0.0.0.0 | IP to bind to |
| REQUEST_TIMEOUT | 5000 | Request timeout in milliseconds |
| MAX_BEARER_COUNT | 1024 | Maximum bearer token queues |
| BOT_RATELIMIT_OVERRIDES | "" | Bot rate limit overrides (bot_id:limit,bot_id:limit) |
| DISABLE_GLOBAL_RATELIMIT_DETECTION | false | Disable global rate limit detection |
| CLUSTER_PORT | 7654 | Cluster communication port |
| CLUSTER_MEMBERS | "" | Comma-separated list of cluster members |
| CLUSTER_DNS | "" | DNS address for cluster discovery |

Information on each config var can be found in [CONFIG.md](CONFIG.md)

.env files are loaded if present

### Behaviour

The proxy listens on all routes and relays them to Discord, while keeping track of ratelimit buckets and making requests wait if there are no tokens to spare. The proxy fires requests sequentially for each bucket and ordering is preserved. The proxy does not modify the requests in any way so any library compatible with Discord's API can be pointed at the proxy and it will not break the library.

When using the proxy, it is safe to remove the ratelimiting logic from clients and fire requests instantly, however, the proxy does not handle retries. If for some reason the proxy encounters a 429, it will return that to the client. It is safe to immediately retry requests that return 429.

The proxy also guards against known scenarios that might cause a Cloudflare ban, like too many webhook 404s or too many 401s.

### Proxy Specific Responses

The proxy may return a 408 Request Timeout if Discord takes more than REQUEST_TIMEOUT milliseconds to respond.

### High Availability

The proxy can be run in a cluster by setting either `CLUSTER_MEMBERS` or `CLUSTER_DNS` env vars. When in cluster mode, all nodes are a suitable gateway for all requests and the proxy will route requests consistently using the bucket hash.

### Bearer Tokens

Bearer tokens are first class citizens. They are treated differently than bot tokens - while bot queues are long-lived and never get evicted, Bearer queues are put into an LRU and are spread out by their token hash. You can control how many bearer queues to keep at any time with the MAX_BEARER_COUNT env var.

### Metrics / Health

| Key | Labels | Description |
|-----|--------|-------------|
| nirn_proxy_error | none | Counter for errors |
| nirn_proxy_requests | method, status, route, clientId | Histogram for request metrics |
| nirn_proxy_open_connections | route, method | Gauge for open connections |

The proxy has an internal endpoint located at `/nirn/healthz` for liveliness and readiness probes.

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black nirn_proxy/

# Lint code
flake8 nirn_proxy/
```

## License

MIT License - see LICENSE file for details.

## Acknowledgements
- [Eris](https://github.com/abalabahaha/eris) - used as reference throughout this project
- [Twilight](https://github.com/twilight-rs) - used as inspiration and reference