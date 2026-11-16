# Uptime checks and rollback

This runbook covers the existing Docker test host. It does not create a host, configure a third-party alert destination, or prove a live recovery. Agree the host, firewall policy, and alert webhook with the team before using it.

## Install the uptime monitor

The monitor uses Python 3 from the standard library. Copy the repository to `/opt/evolving-ltd`, create the service account, and install the unit and private environment file:

```sh
sudo useradd --system --no-create-home --shell /usr/sbin/nologin evolving-monitor
sudo install -m 0644 ops/evolving-uptime.service /etc/systemd/system/evolving-uptime.service
sudo install -m 0600 ops/evolving-uptime.env.example /etc/evolving-uptime.env
sudoedit /etc/evolving-uptime.env
sudo systemctl daemon-reload
sudo systemctl enable --now evolving-uptime.service
sudo systemctl status evolving-uptime.service
```

Set `CHECK_URL` to the service URL reachable from the host. Set `ALERT_WEBHOOK_URL` only after the team selects a receiver that accepts a JSON body with a `text` field. Keep the endpoint in the host's root-readable environment file, never in Git. Monitor output is available with:

```sh
sudo journalctl -u evolving-uptime.service -f
```

The default check runs every 60 seconds with a 5-second timeout. It sends an alert on a down transition and a recovery message when service returns. A webhook delivery failure is logged locally.

## Rehearse alerting

1. Confirm the service and monitor are healthy.
2. Record the UTC time, then stop the service: `docker stop evolving-ltd-test`.
3. Record when the alert arrives in the chosen receiver and in `journalctl`.
4. Restart the service: `docker start evolving-ltd-test`.
5. Record the recovery time and verify the service returns HTTP 200.
6. Restore the service if any step fails.

The target is an alert within five minutes. Record the actual check interval, alert time, recovery time, and any delay from the receiver.

## Roll back

Build each release with a unique, known commit tag and keep the last known-good image on the host:

```sh
docker build --tag "evolving-ltd-demo:<commit-sha>" .
```

When a release fails, record the start time and run:

```sh
scripts/rollback.sh <known-good-commit-sha> 8080
```

The script replaces `evolving-ltd-test` with the retained image, waits for the local HTTP check, and returns non-zero if recovery fails. Verify the externally reachable service as well, then record the image tag and elapsed recovery time. Do not prune the known-good image until the rollback drill is complete.

## Evidence still to collect

The team must provide the shared host and alert receiver before the live test can be completed. Add actual UTC timestamps, HTTP results, and recovery duration to the checkpoint evidence after the drill; do not report planned steps as completed evidence.
