import httpx
from app.config import settings
from app.services.connectors.base import BaseConnector


class GitHubConnector(BaseConnector):
    name = "github"

    def health_check(self) -> dict:
        return {
            "name": self.name,
            "mode": "live-readonly" if settings.github_token else "mock",
            "status": "ok",
        }

    def simulate(self, action_type: str, payload: dict) -> dict:
        repo = payload.get("repo_name", "octocat/hello-world")
        return {
            "action": action_type,
            "repo_name": repo,
            "preview": f"Would fetch latest open issues from repo '{repo}'.",
        }

    def execute(self, action_type: str, payload: dict) -> dict:
        repo = payload.get("repo_name", "octocat/hello-world")

        if action_type != "github.fetch_issues":
            return {
                "status": "ok",
                "mode": "mock",
                "repo_name": repo,
                "summary": "Unsupported GitHub action",
            }

        if not settings.github_token:
            return {
                "status": "ok",
                "mode": "mock",
                "repo_name": repo,
                "issues": [
                    {"title": f"Mock: flaky test in {repo}"},
                    {"title": f"Mock: optimize API for {repo}"},
                ],
            }

        headers = {"Authorization": f"Bearer {settings.github_token}"}
        with httpx.Client(timeout=10) as client:
            res = client.get(f"https://api.github.com/repos/{repo}/issues", headers=headers)
            res.raise_for_status()

        issues = res.json()[:5]
        return {
            "status": "ok",
            "mode": "live-readonly",
            "repo_name": repo,
            "issues": issues,
        }