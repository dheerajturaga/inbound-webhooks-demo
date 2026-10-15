# inbound-webhooks-demo

A sandbox repository for [airflow-provider-inbound-webhooks](https://github.com/dheerajturaga/airflow-provider-inbound-webhooks):
activity here triggers [Apache Airflow](https://airflow.apache.org/) Dags through a repository
webhook. Push, open issues and label pull requests freely; nothing here is deployed anywhere.

## What triggers what

| Do this in this repository | Event name the Dag schedules on | Dag |
|---|---|---|
| Push a commit to `main` | `github/dheerajturaga/inbound-webhooks-demo/push/main` | `deploy_staging` |
| Open an issue | `github/dheerajturaga/inbound-webhooks-demo/issues/opened` | `triage_issue` |
| Add the `deploy-preview` label to a pull request | `github/dheerajturaga/inbound-webhooks-demo/pull_request/labeled/deploy-preview` | `deploy_preview` |

The Dags are in [`dags/github_demo.py`](dags/github_demo.py). Each one prints a line from the
delivery's payload, such as the commit pushed or the issue's title.

## Connect it to your Airflow

1. Install the plugin on your Airflow API server, enable the webhook name `github` and create the
   `webhook_github` connection, as in [Connect GitHub](https://github.com/dheerajturaga/airflow-provider-inbound-webhooks#connect-github).
2. Copy [`dags/github_demo.py`](dags/github_demo.py) into your Dags folder and unpause its Dags.
3. In this repository's **Settings → Webhooks → Add webhook** (your fork's, if you forked it), set:

   | Field | Value |
   |---|---|
   | Payload URL | `https://<your-airflow>/webhooks/github` |
   | Content type | `application/json` |
   | Secret | The secret of `webhook_github` |
   | Which events would you like to trigger this webhook? | **Let me select individual events**: *Issues*, *Pull requests* and *Pushes* |

4. Open an issue, and `triage_issue` starts a run.

Airflow on your laptop works too: GitHub only needs a public HTTPS address that reaches
`/webhooks/github`, such as a tunnel that forwards only that path.

**Forked it?** Webhooks are not copied with a fork, and the event names include the repository, so
set `REPO` in [`dags/github_demo.py`](dags/github_demo.py) to your fork.
