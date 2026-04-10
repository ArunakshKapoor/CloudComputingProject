from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_workflow_create_plan_simulate():
    wf = client.post('/api/v1/workflows', json={'user_id':'demo-user','request_text':'draft email and checklist'}).json()
    wid = wf['id']
    assert client.post(f'/api/v1/workflows/{wid}/plan').status_code == 200
    sim = client.post(f'/api/v1/workflows/{wid}/simulate').json()
    assert sim['estimated_latency_ms'] > 0
