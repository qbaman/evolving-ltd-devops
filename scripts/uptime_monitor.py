#!/usr/bin/env python3
"""Small dependency-free HTTP uptime monitor with transition alerts."""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

check_url = os.environ.get("CHECK_URL", "").strip()
webhook_url = os.environ.get("ALERT_WEBHOOK_URL", "").strip()
interval = int(os.environ.get("CHECK_INTERVAL_SECONDS", "60"))
timeout = int(os.environ.get("REQUEST_TIMEOUT_SECONDS", "5"))

if not check_url:
    sys.exit("CHECK_URL must be set")
if interval < 10 or timeout < 1:
    sys.exit("CHECK_INTERVAL_SECONDS must be at least 10 and REQUEST_TIMEOUT_SECONDS at least 1")


def log(message: str) -> None:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"{now} {message}", flush=True)


def alert(message: str) -> None:
    log(message)
    if not webhook_url:
        return
    body = json.dumps({"text": message}).encode("utf-8")
    request = Request(
        webhook_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            if response.status < 200 or response.status >= 300:
                log(f"Alert webhook returned HTTP {response.status}")
    except (HTTPError, URLError, TimeoutError, OSError) as error:
        log(f"Could not deliver alert webhook: {error}")


previous_state: bool | None = None
while True:
    healthy = False
    detail = ""
    try:
        request = Request(check_url, headers={"User-Agent": "evolving-uptime-check/1.0"})
        with urlopen(request, timeout=timeout) as response:
            healthy = 200 <= response.status < 400
            detail = f"HTTP {response.status}"
    except (HTTPError, URLError, TimeoutError, OSError) as error:
        detail = str(error)

    if previous_state is None:
        if not healthy:
            alert(f"ALERT: {check_url} is DOWN ({detail})")
        else:
            log(f"UP: {check_url} ({detail})")
    elif healthy and not previous_state:
        alert(f"RECOVERY: {check_url} is UP ({detail})")
    elif not healthy and previous_state:
        alert(f"ALERT: {check_url} is DOWN ({detail})")

    previous_state = healthy
    time.sleep(interval)
