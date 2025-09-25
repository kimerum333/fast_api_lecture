## TestClient
from fastapi.testclient import TestClient

from ..src.main import app

client = TestClient(app)


def test_get_all_posts():
    response = client.get("/blog/all")  # 리퀘스트로 시작해서
    assert response.status_code == 200  # 어설트 문법으로 검증
