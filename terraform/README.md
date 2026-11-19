# Shared Linux test deployment

Confirm one team-accessible host with Aman, including who maintains it, the permitted interface and port, and whether a second team machine can reach that address. The university Ubuntu VM is a candidate. Terraform manages Docker on the agreed Linux host. Host allocation, access and network policy are separate decisions for the team and lab administrator.

## Set up the host once

- Use Terraform 1.5 or later and Docker Engine on the host. Check `terraform version` and `docker --host unix:///var/run/docker.sock info`.
- Restrict access to the team's approved network using the lab's network controls. Docker-published ports may bypass host firewall rules that only filter normal host traffic. Confirm access before putting the service on the selected interface.
- Use a single private checkout and state directory on the host. Keep state, variable files and saved plans out of Git. Use one operator at a time and keep a private state backup.
- Set the approved address and port once in `terraform/host.tfvars`. Use this same file for deployments and rollbacks.

```hcl
bind_address = "192.0.2.10" # Replace this documentation address.
host_port    = 8080
```

Run `terraform -chdir=terraform init` from the root of the checkout.

## Build and deploy a release

From the root of the checkout, build only from a clean, reviewed revision. Keep a separate source checkout for builds if the release source differs from the stable Terraform checkout.

```bash
set -euo pipefail
source_dir=$(pwd) # Or set to the separate clean source checkout.
test -z "$(git -C "$source_dir" status --porcelain)"
commit=$(git -C "$source_dir" rev-parse HEAD)
image="evolving-ltd-demo:$commit"
docker --host unix:///var/run/docker.sock build --tag "$image" "$source_dir"
image_id=$(docker --host unix:///var/run/docker.sock image inspect --format '{{.Id}}' "$image")
terraform -chdir=terraform plan -var-file=host.tfvars -var="image_id=$image_id" -out=release.tfplan
terraform -chdir=terraform apply release.tfplan
terraform -chdir=terraform output -raw service_url
```

Use a fresh commit tag for each release. Record both the Git commit and immutable image ID. Before deploying a second version, keep the known-good image and tag on disk and verify that it is still inspectable by ID. Avoid image pruning until the drill is complete.

## Verify the deployment

On a second machine, set `service_url` to the exact URL printed by Terraform. Check the status and expected page heading with the same criteria as the Docker CI job.

```bash
status=$(curl --fail --silent --show-error --max-time 5 \
  --output served-page.html --write-out '%{http_code}' "$service_url")
test "$status" = 200
grep -F '<h1>Evolving Ltd Service Desk</h1>' served-page.html
```

Measure deployment from the start of the release build until this second-machine verification succeeds. The indicative target is under 20 minutes. See the [monitoring and rollback runbook](../ops/README.md) for the outage drill, recovery and evidence.
