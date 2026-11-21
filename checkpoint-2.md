# Team ALERT · Checkpoint 2

## What we can show — 16 November 2026

We have a small HTML service desk page packaged with Nginx in Docker. GitHub Actions builds the image, starts the container on a temporary Ubuntu runner and checks that the page returns HTTP 200 and contains the expected heading. The container is removed at the end of the job. This is an automated build-and-test demonstration; it is not yet a deployment to a persistent shared host.

[PR #1](https://github.com/qbaman/evolving-ltd-devops/pull/1) was merged into main on 16 November after Esrom's technical approval and a passing check.

- [Esrom's review](https://github.com/qbaman/evolving-ltd-devops/pull/1#pullrequestreview-5908373440), submitted on 15 November, covers the page, Dockerfile, workflow and checkpoint notes.
- [Passing run for the reviewed version](https://github.com/qbaman/evolving-ltd-devops/actions/runs/43501908019), commit a9df69f964475fe310add1e7227da9219fef8a4f.
- [Merge commit](https://github.com/qbaman/evolving-ltd-devops/commit/4872d7a724c246fd4b6747b607576c05f7aa6070).
- [Original successful job log](https://github.com/qbaman/evolving-ltd-devops/actions/runs/43489321880/job/132105968860) and [original screenshot](checkpoint-2-run-1.jpg). These record the earlier demo run.

## My checkpoint walkthrough

1. Open the [team board](https://github.com/users/qbaman/projects/1/views/1) and explain the current owners, completed demo and remaining tasks.
2. Open PR #1 and show the commits, Esrom's review and merged status.
3. Show index.html: this is the example webpage, not a complete ticket system.
4. Show Dockerfile: Nginx serves the HTML page inside the container.
5. Show .github/workflows/checkpoint.yml: build, start, check HTTP 200 and the heading, show logs on failure, then clean up.
6. Open the passing run and explain how the check provides feedback on a proposed change.
7. Explain the remaining host, Terraform, monitoring and rollback work and the measurements below.

Rehearsal is still to be recorded in [issue #2](https://github.com/qbaman/evolving-ltd-devops/issues/2). These notes do not claim the walkthrough has already been rehearsed.

## Contributions and current ownership

My commits in PR #1 contain the demo, workflow and evidence notes. I also maintain the backlog and delivery evidence. Esrom completed the technical review linked above. Terraform implementation and provisioning evidence have not yet been pushed to the repository at the time of this update.

| Work | Current owner | Reviewer |
| --- | --- | --- |
| [Checkpoint walkthrough and acceptance evidence](https://github.com/qbaman/evolving-ltd-devops/issues/2) | Aman | Esrom |
| [Test host and Terraform](https://github.com/qbaman/evolving-ltd-devops/issues/3) | Esrom | Aman |
| [Service desk and HTTP check](https://github.com/qbaman/evolving-ltd-devops/issues/5) | Aman, taking over the planned Lucas task | Esrom |
| [Uptime check and rollback](https://github.com/qbaman/evolving-ltd-devops/issues/4) | Esrom, taking over the planned Titas task | Aman |

Further contributions from Lucas and Titas need an agreed task and linked evidence. Each member needs to review a colleague's technical work. Aman still needs to complete his review when a colleague's implementation is available; Esrom's approval of Aman's PR does not fulfil Aman's own review requirement.

Start new task branches from the updated main branch and open PRs back to main. Existing branches should incorporate the merged baseline before work that depends on the demo. Link each PR and test result to its issue and update the board as work progresses.

## Response to Viva 1 feedback and next increment

The reported verbal feedback was to make our tooling clearer. GitHub Actions runs the automated workflow; Docker packages and runs the page; Terraform is planned for provisioning the test infrastructure. Terraform is not implemented yet.

The next priority is agreeing a shared test host. The university Ubuntu VM is a candidate, but we still need to confirm how it is provided, team access and what infrastructure Terraform can manage. An existing VM alone is not evidence of Terraform provisioning. One shared host can support the team; each member does not need their own local VM.

After the host is ready, connect the tested application to a repeatable deployment process, then add monitoring and rehearse recovery. Live alerting and rollback in issue #4 depend on the host in issue #3. Hosting access and the small number of active contributors remain delivery risks; task ownership and outstanding work are recorded above.

## What I want to measure for Viva 2

These are planned acceptance tests, not achieved results:

- Deploy to the test host and time from starting the deployment to a verified response. Target: under 20 minutes.
- Roll back a failed test release to a known good image and time from starting recovery to a verified response. Target: under 10 minutes.
- Stop the service in the test environment and time from the outage to an alert arriving. Target: within 5 minutes.
- Trace every test release to its image version, commit, PR, review and check result.

Record the environment, image/commit, start and end timestamps, expected and actual outcome, and links to logs for each test. The temporary runner smoke test does not establish these persistent-host results.
