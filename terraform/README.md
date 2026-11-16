# Docker test deployment

This configuration builds the repository's service desk image and runs it as a persistent Docker container. It manages the container on an **existing Linux test host**; it does not create a VM or select a cloud provider. The team still needs to agree and record which shared host to use before deployment evidence can be collected.

## Requirements

- Terraform 1.5 or later
- Docker Engine on the agreed Linux host
- A Docker CLI connection to that host
- Network access to the host's selected TCP port (8080 by default)

For a local host, run Terraform on that host. For a remote host, configure Docker's supported SSH connection before running Terraform, for example:

```sh
export DOCKER_HOST=ssh://<user>@<test-host>
```

Use the team's approved SSH key and host address; do not commit credentials or private keys.

## Deploy

Run from the repository root:

```sh
terraform -chdir=terraform init
terraform -chdir=terraform plan -var="image_tag=<git-commit-sha>"
terraform -chdir=terraform apply -var="image_tag=<git-commit-sha>"
```

Terraform builds the Docker image from the checked-out repository, starts or updates `evolving-ltd-test`, and exposes port 80 on host port 8080. Verify it from a machine that can reach the test host:

```sh
curl --fail --show-error http://<test-host>:8080/
```

Record the host name, commit SHA, HTTP status, deployment time, and PR link in the project evidence. Do not record private addresses or credentials in a public repository.

## Roll back

Keep the previous deployment's commit SHA. To restore that image, check out the corresponding source revision and apply the same Terraform configuration with its SHA:

```sh
git checkout <known-good-commit-sha>
terraform -chdir=terraform apply -var="image_tag=<known-good-commit-sha>"
```

The image is retained locally so the prior version remains available. Confirm recovery with the same HTTP check and record the recovery time. Store Terraform state securely on the agreed host; never commit `terraform.tfstate` or its backup.
