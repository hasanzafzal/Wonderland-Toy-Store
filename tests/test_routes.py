"""Unit tests for routes"""
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test index route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Wonderland Toy Store' in response.data

def test_products(client):
    """Test products route"""
    response = client.get('/products')
    assert response.status_code == 200

def test_about(client):
    """Test about route"""
    response = client.get('/about')
    assert response.status_code == 200
