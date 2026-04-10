from app.services.connectors.github_connector import GitHubConnector


def test_github_fallback_mock():
    out = GitHubConnector().execute('github.fetch_issues', {})
    assert 'issues' in out
