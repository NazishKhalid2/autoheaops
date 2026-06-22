from flask import Flask, jsonify
from prometheus_client import Counter, Gauge, generate_latest
import psutil
import os

app = Flask(__name__)

# Prometheus metrics
app_requests_total = Counter(
    'app_requests_total', 
    'Total number of requests', 
    ['method', 'endpoint']
)
app_errors_total = Counter(
    'app_errors_total',
    'Total number of errors',
    ['endpoint']
)
app_cpu_usage_percent = Gauge(
    'app_cpu_usage_percent',
    'CPU usage percentage'
)

@app.route('/')
def index():
    app_requests_total.labels(method='GET', endpoint='/').inc()
    return jsonify({"message": "AutoHealOps is running!", "status": "ok"}), 200

@app.route('/health')
def health():
    app_requests_total.labels(method='GET', endpoint='/health').inc()
    return jsonify({"status": "healthy"}), 200

@app.route('/error')
def error():
    app_requests_total.labels(method='GET', endpoint='/error').inc()
    app_errors_total.labels(endpoint='/error').inc()
    return jsonify({"error": "simulated error"}), 500

@app.route('/metrics')
def metrics():
    # Update CPU usage before exposing metrics
    app_cpu_usage_percent.set(psutil.cpu_percent(interval=0.1))
    return generate_latest(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)