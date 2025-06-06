import pytest
from app import app
from openai_client import generate_curriculum as real_gen

@pytest.fixture(autouse=True)
def patch_generate(monkeypatch):
    def fake_generate(topic):
        return {
            "topic": topic,
            "curriculum": [
                {
                    "module_number": 1,
                    "title": "Test Module",
                    "description": "Desc",
                    "resources": [{"url": "http://example.com", "description": "Example"}],
                    "exercise": "Do this",
                    "quiz": [{"question": "Q?", "answers": ["A1","A2"], "correct_answer_index": 0}]
                }
            ]
        }
    monkeypatch.setattr('openai_client.generate_curriculum', fake_generate)
    yield

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_generate_success(client):
    resp = client.post('/generate', json={'topic': 'Demo'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['topic'] == 'Demo'
    assert isinstance(data['curriculum'], list)

def test_generate_missing_topic(client):
    resp = client.post('/generate', json={'topic': ''})
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data

def test_generate_invalid_json(client):
    resp = client.post('/generate', data='not-json')
    assert resp.status_code == 400
