import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app import app
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_status_code(client):
    """Test that / returns 200"""
    response = client.get('/')
    assert response.status_code == 200

def test_index_returns_ok(client):
    """Test that / returns status ok"""
    response = client.get('/')
    data = response.get_json()
    assert data['status'] == 'ok'

def test_health_status_code(client):
    """Test that /health returns 200"""
    response = client.get('/health')
    assert response.status_code == 200

def test_health_returns_healthy(client):
    """Test that /health returns status healthy"""
    response = client.get('/health')
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_error_returns_500(client):
    """Test that /error returns 500"""
    response = client.get('/error')
    assert response.status_code == 500