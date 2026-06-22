import requests
import subprocess
import time
import os
from datetime import datetime

HEALTH_URL = os.getenv("HEALTH_URL", "http://localhost:5000/health")
METRICS_URL = HEALTH_URL.replace("/health", "/metrics")
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL", "")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "10"))
CPU_THRESHOLD = float(os.getenv("CPU_THRESHOLD", "80.0"))

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")

def send_slack(message):
    if not SLACK_WEBHOOK:
        log("(No Slack webhook set — skipping alert)")
        return
    try:
        requests.post(SLACK_WEBHOOK, json={
            "text": f":rotating_light: *AutoHealOps Alert*\n{message}"
        }, timeout=5)
        log("Slack alert sent")
    except Exception as e:
        log(f"Slack failed: {e}")

def restart_app():
    log("Attempting to restart app container...")
    try:
        subprocess.run(
            ["docker", "compose", "restart", "app"],
            check=True, capture_output=True, text=True
        )
        log("Container restarted successfully")
        send_slack(":white_check_mark: App container restarted successfully after failure.")
    except subprocess.CalledProcessError as e:
        log(f"Restart failed: {e.stderr}")
        send_slack(":x: Auto-restart FAILED. Manual intervention needed immediately.")

def check_health():
    try:
        r = requests.get(HEALTH_URL, timeout=3)
        if r.status_code == 200:
            log("Health check PASSED")
            return True
        log(f"Health check FAILED — status code {r.status_code}")
        return False
    except requests.exceptions.ConnectionError:
        log("Health check FAILED — app unreachable")
        return False
    except requests.exceptions.Timeout:
        log("Health check FAILED — request timed out")
        return False

def check_cpu():
    try:
        r = requests.get(METRICS_URL, timeout=3)
        for line in r.text.split('\n'):
            if line.startswith('app_cpu_usage_percent') and not line.startswith('#'):
                cpu = float(line.split()[-1])
                log(f"CPU usage: {cpu:.1f}%")
                if cpu > CPU_THRESHOLD:
                    send_slack(
                        f":warning: High CPU usage detected: *{cpu:.1f}%*\n"
                        f"Threshold is {CPU_THRESHOLD}%. App may be under stress."
                    )
    except Exception as e:
        log(f"Could not read CPU metrics: {e}")

if __name__ == '__main__':
    log("AutoHealOps healer started")
    send_slack(":eyes: AutoHealOps monitoring is now active and watching your app.")
    failures = 0

    while True:
        healthy = check_health()
        if healthy:
            failures = 0
            check_cpu()
        else:
            failures += 1
            log(f"Consecutive failures: {failures}")
            if failures >= 2:
                send_slack(
                    f":skull: App has been DOWN for {failures} consecutive checks.\n"
                    f"Triggering auto-restart now..."
                )
                restart_app()
                failures = 0
        time.sleep(CHECK_INTERVAL)
