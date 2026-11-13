# Checkpoint 2 demo and evidence

The demo uses a static Evolving Ltd service desk page. GitHub Actions checks out the proposed change, builds a Docker image tagged with the commit SHA, starts the container on an Ubuntu runner, and checks that it returns HTTP 200 and serves the expected heading. The runner removes the container after the check. The deployment is available during the job.

## Lab walkthrough

1. Open the pull request and show the change, reviewer feedback when available, and the workflow result.
2. Open **Build, start and verify the container**. Show the image build, container startup, and HTTP check. Point out the tested commit SHA in the log.
3. Show the contribution record and explain the plan for Terraform provisioning, persistent deployment, monitoring, and rollback.

## Checkpoint evidence

| Evidence | Record |
| --- | --- |
| Shared repository | [evolving-ltd-devops](https://github.com/qbaman/evolving-ltd-devops) |
| Automation and initial test | [Successful GitHub Actions job](https://github.com/qbaman/evolving-ltd-devops/actions/runs/43489321880/job/132105968860). The job log confirms HTTP 200 and the expected page heading. [Evidence screenshot](checkpoint-2-run-1.jpg). |
| Contribution record | Add each team member’s name, completed work, evidence link and next task as work is agreed or completed. |
| Peer review | Link the teammate’s review once it has happened. |

## Risks and decisions

| Item | Decision or next step |
| --- | --- |
| Viva 1 verbal feedback | Make the agreed tooling explicit. GitHub Actions runs CI/CD, Docker packages and runs the service, and Terraform will provision infrastructure. The workflow shows the first two tools in use. |
| Persistent environment | A Linux VM is currently unavailable. Run the first test deployment on GitHub’s Ubuntu runner and agree a persistent target before wiring in Terraform. |
| Review availability | The team needs a teammate review to demonstrate the agreed delivery process. Keep the PR open for review. |

## Viva 2 evaluation plan

| Target | How to test it |
| --- | --- |
| Deployment under 20 minutes | On the persistent test target, record the time from deployment start to a verified HTTP response. Keep the workflow log and timestamps. |
| Recovery under 10 minutes | In the test environment, roll back a failed release to a known good image and record the time to a verified response. |
| Critical failure detected and reported within 5 minutes | Stop the test service and compare the outage timestamp with the alert timestamp. |
| Traceability for every release | Match each test release to its image version, commit, pull request, review and check result. |

Use the Checkpoint 2 workflow run as initial test evidence. Add the measured results for persistent deployment, recovery and alerting once the team runs those tests.
