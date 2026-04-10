from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_memory_list():
    res = client.get('/api/v1/memory', params={'user_id':'demo-user'})
    assert res.status_code == 200
