# Uptime monitoring and rollback

Use this runbook after setting up the [shared test deployment](../terraform/README.md). Agree on the test window, a second machine for endpoint checks and a private webhook receiver that accepts a JSON `text` field.

## Install the monitor

Run on the approved Linux test host. The example unit expects the script at `/opt/evolving-ltd/scripts/uptime_monitor.py` and uses an unprivileged system account.

```bash
id evolving-monitor >/dev/null 2>&1 ||
  sudo useradd --system --no-create-home --shell /usr/sbin/nologin evolving-monitor
sudo install -D -m 0644 scripts/uptime_monitor.py /opt/evolving-ltd/scripts/uptime_monitor.py
sudo install -m 0644 ops/evolving-uptime.service /etc/systemd/system/evolving-uptime.service
sudo test -f /etc/evolving-uptime.env ||
  sudo install -m 0600 ops/evolving-uptime.env.example /etc/evolving-uptime.env
sudoedit /etc/evolving-uptime.env
sudo systemctl daemon-reload
sudo systemctl enable evolving-uptime.service
sudo systemctl restart evolving-uptime.service
sudo journalctl -u evolving-uptime.service --utc -f
```

Set `CHECK_URL` to the Terraform service URL and enter the webhook URL in the private environment file. Keep webhook credentials out of Git and screenshots. The default poll interval is 60 seconds and the HTTP timeout is five seconds. Failed webhook deliveries are retried once per poll, up to five total attempts per notification. The monitor sends pending notifications in order, even if the service recovers during a retry. The queue is in memory and pending notifications are lost on a service restart.

## Rehearse outage and rollback

1. Deploy and verify a known-good release from a second machine. Record its source commit, image ID and service URL. Deploy a different reviewed image to rehearse an actual version rollback.
2. Confirm both releases can be inspected locally by image ID. Check the running release and monitor logs, then record the outage start in UTC and stop the test service with `docker --host unix:///var/run/docker.sock stop evolving-ltd-test`.
3. Verify the same URL fails from the second machine and note when the outage alert arrives at the receiver. Confirm delivery within five minutes against the recorded outage start. The journal shows attempts. Receiver evidence confirms delivery.
4. Recover by applying the previously verified image ID from the **same** Terraform checkout, state and `host.tfvars`. Record the rollback start in UTC. Check the plan before applying it.

```bash
set -euo pipefail
: "${known_good_id:?Set known_good_id to the recorded sha256 image ID}"
docker --host unix:///var/run/docker.sock image inspect "$known_good_id" >/dev/null
terraform -chdir=terraform plan -var-file=host.tfvars -var="image_id=$known_good_id" -out=rollback.tfplan
terraform -chdir=terraform apply rollback.tfplan
terraform -chdir=terraform output -raw service_url
```

5. Verify the original URL returns HTTP 200 and the expected page heading from the second machine. Check the running image ID using `docker --host unix:///var/run/docker.sock inspect --format '{{.Image}}' evolving-ltd-test`. Record the recovery time and confirm the recovery notification arrives. The rollback target is under ten minutes from the start of rollback to successful second-machine verification.

If the rollback is blocked before replacing the stopped container, restore the pre-drill release with `docker --host unix:///var/run/docker.sock start evolving-ltd-test` if it is still present. If replacement already occurred, inspect the Terraform state and container, then use the same Terraform workflow to restore a retained release and recheck the endpoint.

## Viva 2 evidence

Record the host decision and access model, both release commits and image IDs, and the reviewed PR and workflow run. Save the plan/apply result, second-machine HTTP and heading checks, outage start, receiver arrival time, rollback start, verified recovery and recovery notification. Report elapsed deployment, alert and rollback times against the targets. Store private host and receiver information in the approved team workspace and redact it from public evidence. Collect these results during the shared-host drill.
