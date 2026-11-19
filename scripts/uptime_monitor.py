#!/usr/bin/env python3
"""Check the service and deliver ordered outage and recovery notifications."""

from __future__ import annotations

import json
import os
import time
from collections import deque
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MAX_DELIVERY_ATTEMPTS = 5
MAX_PENDING_ALERTS = 32


def log(message: str) -> None:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"{timestamp} {message}", flush=True)


def check_service(url: str, timeout: int) -> tuple[bool, str]:
    request = Request(url, headers={"User-Agent": "evolving-uptime-check/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status == 200, f"HTTP {response.status}"
    except HTTPError as error:
        error.close()
        return False, f"HTTP {error.code}"
    except (URLError, OSError) as error:
        return False, type(error).__name__


def send_alert(url: str, message: str, timeout: int) -> bool:
    request = Request(
        url,
        data=json.dumps({"text": message}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return 200 <= response.status < 300
    except HTTPError as error:
        error.close()
        return False
    except (URLError, OSError):
        # Exception details may contain parts of the private webhook URL.
        return False


class UptimeMonitor:
    def __init__(self, check_url: str, webhook_url: str, timeout: int):
        self.check_url = check_url
        self.webhook_url = webhook_url
        self.timeout = timeout
        self.previous_health: bool | None = None
        self.pending: deque[tuple[str, int]] = deque()

    def poll(self) -> None:
        healthy, detail = check_service(self.check_url, self.timeout)
        if healthy != self.previous_health:
            if healthy:
                event = "UP" if self.previous_health is None else "RECOVERY: UP"
            else:
                event = "ALERT: DOWN"
            message = f"{event} — {self.check_url} ({detail})"
            log(message)
            if self.previous_health is not None or not healthy:
                self.enqueue(message)
        self.previous_health = healthy
        self.deliver_pending()

    def enqueue(self, message: str) -> None:
        if not self.webhook_url:
            return
        if len(self.pending) >= MAX_PENDING_ALERTS:
            log("Webhook queue is full. Dropping new notification.")
            return
        self.pending.append((message, 0))

    def deliver_pending(self) -> None:
        if not self.pending:
            return
        message, previous_attempts = self.pending[0]
        attempt = previous_attempts + 1
        if send_alert(self.webhook_url, message, self.timeout):
            self.pending.popleft()
            log(f"Webhook accepted notification on attempt {attempt}.")
        elif attempt == MAX_DELIVERY_ATTEMPTS:
            self.pending.popleft()
            log(f"Webhook delivery failed after {attempt} attempts. Dropping notification.")
        else:
            self.pending[0] = (message, attempt)
            log(f"Webhook delivery failed on attempt {attempt}. Retrying at next poll.")


def main() -> None:
    check_url = os.environ.get("CHECK_URL", "").strip()
    webhook_url = os.environ.get("ALERT_WEBHOOK_URL", "").strip()
    interval = int(os.environ.get("CHECK_INTERVAL_SECONDS", "60"))
    timeout = int(os.environ.get("REQUEST_TIMEOUT_SECONDS", "5"))
    if not check_url:
        raise SystemExit("CHECK_URL must be set")
    if interval < 10 or timeout < 1:
        raise SystemExit("Use a check interval of at least 10 seconds and a timeout of at least 1 second.")
    if not webhook_url:
        log("ALERT_WEBHOOK_URL is empty. Notifications will only appear in the local log.")
    monitor = UptimeMonitor(check_url, webhook_url, timeout)
    while True:
        monitor.poll()
        time.sleep(interval)


if __name__ == "__main__":
    main()
