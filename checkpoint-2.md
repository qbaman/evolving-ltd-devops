# Checkpoint 2

## What we can show

We have a small Evolving Ltd service desk page running in Docker. In [PR #1](https://github.com/qbaman/evolving-ltd-devops/pull/1), GitHub Actions builds the image, starts the container on an Ubuntu runner and checks the page. The log shows HTTP 200 and the heading we expected. The container stops at the end of the job.

[Successful job log](https://github.com/qbaman/evolving-ltd-devops/actions/runs/43489321880/job/132105968860) · [Screenshot](checkpoint-2-run-1.jpg)

In the lab, I'll open the PR and walk through the build, container startup and HTTP check. I'll ask a teammate to review the PR and link that review here once it's done.

## What we're doing next

The feedback from Viva 1 was to make our tooling clearer. GitHub Actions runs the workflow, Docker packages and runs the page, and we plan to use Terraform to set up the infrastructure. We still need to agree where the service will run after the workflow ends.

Here's the split I'd propose for the team. Esrom led architecture and IaC in Viva 1. Lucas and Titas still need to confirm their tasks.

| Person | Proposed work | Evidence to add |
| --- | --- | --- |
| Aman | I'll coordinate delivery, walk through the Actions workflow, and track the acceptance tests. | PR #1 review and the combined test results. |
| Esrom | Confirm a Linux test host, then write and test the Terraform setup. | Terraform PR and a record of a successful provision. |
| Lucas | Own the service desk page and extend the checks to cover any new features the team agrees on. | App PR and passing checks tied to it. |
| Titas | Set up an uptime check and rehearse rolling back to an earlier Docker image. | Monitoring and rollback PR with timestamps from a test. |

Once the team agrees the split, we'll each open a PR from a branch named for the task. Work that needs the Docker demo can start from `checkpoint-2-demo` and target that branch until PR #1 merges. After that, new branches start from `main` and PRs go back to `main`. We'll each review someone else's work and add our PRs, reviews and test logs here as we go.

## What I want to measure for Viva 2

- Deploy to the test host and time how long it takes to get a verified response. Target: under 20 minutes.
- Roll back a failed test release to a known good image and time the recovery. Target: under 10 minutes.
- Stop the service in the test environment and time how long it takes for an alert to arrive. Target: within 5 minutes.
- Trace every test release back to its image version, commit, PR, review and check result.
