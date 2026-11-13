# Evolving Ltd DevOps

**Service desk demo · CMP6237 DevOps and Enterprise Automation**

[Checkpoint 2 notes and team plan](https://github.com/qbaman/evolving-ltd-devops/blob/checkpoint-2-demo/checkpoint-2.md) &nbsp;·&nbsp; [Demo pull request](https://github.com/qbaman/evolving-ltd-devops/pull/1) &nbsp;·&nbsp; [GitHub Actions](https://github.com/qbaman/evolving-ltd-devops/actions)

---

## The project

Evolving Ltd is our case study for a staged DevOps rollout. We started with a small service desk page that we can build, run and check automatically. The next step is to deploy it to a persistent test environment so we can measure deployment, alerting and recovery for Viva 2.

| Tool | Role in the project |
| --- | --- |
| GitHub Actions | Builds the image and checks the running page on each pull request. |
| Docker | Packages the page and Nginx into an image we can run the same way each time. |
| Terraform | Planned for provisioning the persistent test environment. |

## Checkpoint 2 demo

GitHub Actions builds and starts the Docker container on an Ubuntu runner. The smoke test checks that the page returns HTTP 200 and contains the expected heading. The runner removes the container when the job ends. [Successful workflow log](https://github.com/qbaman/evolving-ltd-devops/actions/runs/43489321880/job/132105968860)

To run the page locally with Docker, check out `checkpoint-2-demo` while PR #1 is open. Build and start the image from the repository root.

```bash
docker build -t evolving-ltd-demo .
docker run --rm -p 127.0.0.1:8080:80 evolving-ltd-demo
```

Open [localhost:8080](http://localhost:8080/) to see the service desk page.

## Contributing

Use a separate branch for each task and ask a teammate to review your PR. Start from `main` for independent work. If your task needs the unmerged demo, branch from `checkpoint-2-demo` and open your PR against that branch. Once PR #1 merges, start new work from `main` and open PRs back to `main`.

Use a name that describes the task, such as `infra/terraform-test-host` or `ops/uptime-check`. Link your PR and test result in the checkpoint notes so we can show who did what and how it was checked.
