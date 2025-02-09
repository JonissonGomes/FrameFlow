import json
import uuid
import pytest
from app import create_app
from flask_jwt_extended import create_access_token

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

@pytest.fixture
def access_token(client):
    user_id = "60f6d7f6f6f6f6f6f6f6f6f6"
    return create_access_token(identity=user_id)

def test_upload_video_no_file(client, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/upload", headers=headers)
    data = response.get_json()

    assert response.status_code == 400, f"Erro: {data}"
    assert "error" in data
