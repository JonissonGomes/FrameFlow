import json
import uuid
import pytest
from app import create_app

@pytest.fixture(autouse=True)
def clean_db():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        app.mongo.db.users.delete_many({})
    yield

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_register_and_login(client):
    unique_suffix = str(uuid.uuid4())[:8]
    register_data = {
        "username": f"testuser_{unique_suffix}",
        "email": f"test_{unique_suffix}@example.com",
        "password": "testpassword"
    }
    
    response = client.post(
        "/auth/register",
        data=json.dumps(register_data),
        content_type="application/json"
    )
    assert response.status_code == 201, f"Erro no registro: {response.get_json()}"

    login_data = {
        "email": register_data["email"],
        "password": register_data["password"]
    }
    response = client.post(
        "/auth/login",
        data=json.dumps(login_data),
        content_type="application/json"
    )
    data = response.get_json()
    assert response.status_code == 200
    assert "access_token" in data