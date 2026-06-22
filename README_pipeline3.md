# Pipeline 3 — Monitoring + Auto-Healing (Nazish)

## What this pipeline does
Flask app runs → Prometheus scrapes metrics every 5s → Grafana displays live dashboard → Healer polls /health every 10s → crash detected → container auto-restarted → Slack alert sent

## Architecture
- **Prometheus**: scrapes /metrics endpoint every 5 seconds, stores time-series data
- **Grafana**: reads from Prometheus, displays 4 live panels
- **healer.py**: polls /health every 10s, restarts container after 2 failures, sends Slack alerts

## Files
- `monitoring/prometheus.yml` — Prometheus scrape config
- `healing/healer.py` — auto-healing script
- `healing/requirements.txt` — Python dependencies
- `monitoring/grafana/dashboard.json` — exported Grafana dashboard

## Grafana Dashboard Panels
| Panel | Query |
|-------|-------|
| Total Requests | `app_requests_total` |
| Request Rate Per Minute | `rate(app_requests_total[1m]) * 60` |
| CPU Usage Percent | `app_cpu_usage_percent` |
| Total Errors | `app_errors_total` |

## How to run the healer
```bash
cd healing
pip install -r requirements.txt
export SLACK_WEBHOOK_URL="your-webhook-url"
python -u healer.py
```

## Environment variables
| Variable | Default | Description |
|----------|---------|-------------|
| HEALTH_URL | http://localhost:5000/health | App health endpoint |
| SLACK_WEBHOOK_URL | (none) | Slack incoming webhook |
| CHECK_INTERVAL | 10 | Seconds between checks |
| CPU_THRESHOLD | 80.0 | CPU % alert threshold |

## Security
- No hardcoded secrets anywhere
- All sensitive values passed via environment variables

## Live demo steps
1. `docker compose up --build` — starts all containers
2. `python -u healing/healer.py` — starts healer
3. Open Grafana at localhost:3000 (admin/admin123)
4. `docker stop autoheaops-app` — simulate crash
5. Watch healer detect failure and restart container
6. Check Slack for alerts

## Screenshots
- Grafana dashboard with 4 live panels
- Healer terminal showing crash detection and auto-restart
- Slack alerts for down and recovery
- Prometheus targets page showing app UP
