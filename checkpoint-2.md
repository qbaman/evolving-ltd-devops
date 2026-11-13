# Team ALERT · Checkpoint 2

## What we can show

We have a small Evolving Ltd service desk page running in Docker. In [PR #1](https://github.com/qbaman/evolving-ltd-devops/pull/1), GitHub Actions builds the image, starts the container on an Ubuntu runner and checks the page. The log shows HTTP 200 and the heading we expected. The container stops at the end of the job.

[Successful job log](https://github.com/qbaman/evolving-ltd-devops/actions/runs/43489321880/job/132105968860) · [Screenshot](checkpoint-2-run-1.jpg)

In the lab, I'll open the PR and walk through the build, container startup and HTTP check. I'll ask a teammate to review the PR and link that review here once it's done.

## What we're doing next

The feedback from Viva 1 was to make our tooling clearer. GitHub Actions runs the workflow, Docker packages and runs the page, and we plan to use Terraform to set up the infrastructure. We still need to agree where the service will run after the workflow ends.

I’ll handle delivery and acceptance evidence. Esrom will lead Terraform and the test host. I’ll review Esrom’s PRs, and he’ll review mine, including any work we pick up for the other two.

| Work | Primary | Fallback | Reviewer |
| --- | --- | --- | --- |
| [Checkpoint walkthrough and acceptance evidence](https://github.com/qbaman/evolving-ltd-devops/issues/2) | Aman | | Esrom |
| [Test host and Terraform](https://github.com/qbaman/evolving-ltd-devops/issues/3) | Esrom | | Aman |
| [Service desk and HTTP check](https://github.com/qbaman/evolving-ltd-devops/issues/5) | Lucas | Aman | Titas reviews Lucas if available. Esrom reviews Aman. |
| [Uptime check and rollback](https://github.com/qbaman/evolving-ltd-devops/issues/4) | Titas | Esrom | Lucas reviews Titas if available. Aman reviews Esrom. |

If Lucas or Titas can't meet the agreed handoff, Aman takes Lucas’s work and Esrom takes Titas’s. We’ll update the issue assignee when the work changes hands and link the PR and test results so it’s clear who did what. If Lucas or Titas contributes before the other is available to review, ask Aman or Esrom to review the change. Each of us should leave at least one technical review on someone else’s work.

We’ll work from one branch per task. If a change needs the unmerged demo, branch from `checkpoint-2-demo` and open a PR against it for review. Once PR #1 lands, start new work from `main` and open PRs back to `main`. I’ll use the [Team ALERT TO DO board](https://github.com/users/qbaman/projects/1/views/1) to track what’s started, waiting for review and done.

## What I want to measure for Viva 2

- Deploy to the test host and time how long it takes to get a verified response. Target: under 20 minutes.
- Roll back a failed test release to a known good image and time the recovery. Target: under 10 minutes.
- Stop the service in the test environment and time how long it takes for an alert to arrive. Target: within 5 minutes.
- Trace every test release back to its image version, commit, PR, review and check result.
