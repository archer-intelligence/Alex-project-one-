import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_serves_index(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'<input' in resp.data
    assert b'id="generate-btn"' in resp.data
