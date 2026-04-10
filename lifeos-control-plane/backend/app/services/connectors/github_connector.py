import httpx
from app.config import settings
from app.services.connectors.base import BaseConnector


class GitHubConnector(BaseConnector):
    name = "github"

    def health_check(self) -> dict:
        return {"name": self.name, "mode": "live-readonly" if settings.github_token else "mock", "status": "ok"}

    def simulate(self, action_type: str, payload: dict) -> dict:
        return {"action": action_type, "preview": "Would fetch latest open issues from repo."}

    def execute(self, action_type: str, payload: dict) -> dict:
        if not settings.github_token:
            return {"issues": [{"title": "Mock: flaky test"}, {"title": "Mock: optimize API"}]}
        if action_type == "github.fetch_issues":
            repo = payload.get("repo_name", "octocat/hello-world")
            headers = {"Authorization": f"Bearer {settings.github_token}"}
            with httpx.Client(timeout=10) as client:
                res = client.get(f"https://api.github.com/repos/{repo}/issues", headers=headers)
                res.raise_for_status()
            return {"issues": res.json()[:5]}
        return {"summary": "Unsupported action"}
