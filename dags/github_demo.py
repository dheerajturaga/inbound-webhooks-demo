"""
Dags that run when something happens in this repository, through airflow-provider-inbound-webhooks.

Copy this file into your Airflow Dags folder. If you fork the repository, set REPO to your fork.
"""

from __future__ import annotations

from airflow.sdk import Asset, dag, task

REPO = "dheerajturaga/inbound-webhooks-demo"

main_push = Asset(f"github/{REPO}/push/main")
issue_opened = Asset(f"github/{REPO}/issues/opened")
deploy_preview_label = Asset(f"github/{REPO}/pull_request/labeled/deploy-preview")


def get_payloads(triggering_asset_events, asset) -> list[dict]:
    # One run can carry several deliveries, which are not ordered: sort them oldest first.
    events = sorted(triggering_asset_events[asset], key=lambda event: event.timestamp)
    return [event.extra["payload"] for event in events]


@dag(schedule=main_push, tags=["github-demo"])
def deploy_staging():
    @task
    def deploy(*, triggering_asset_events=None):
        push = get_payloads(triggering_asset_events, main_push)[-1]
        message = (push.get("head_commit") or {}).get("message", "")
        print(f"Deploying {push['after'][:7]} to staging, pushed by {push['pusher']['name']}: {message}")

    deploy()


@dag(schedule=issue_opened, tags=["github-demo"])
def triage_issue():
    @task
    def triage(*, triggering_asset_events=None):
        for delivery in get_payloads(triggering_asset_events, issue_opened):
            issue = delivery["issue"]
            print(f"Triaging issue #{issue['number']} by {issue['user']['login']}: {issue['title']}")

    triage()


@dag(schedule=deploy_preview_label, tags=["github-demo"])
def deploy_preview():
    @task
    def deploy(*, triggering_asset_events=None):
        for delivery in get_payloads(triggering_asset_events, deploy_preview_label):
            pr = delivery["pull_request"]
            print(f"Deploying a preview of PR #{pr['number']} at {pr['head']['sha'][:7]}: {pr['title']}")

    deploy()


deploy_staging()
triage_issue()
deploy_preview()
