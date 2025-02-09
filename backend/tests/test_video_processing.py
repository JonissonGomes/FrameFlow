import json
import pytest
from app import create_app
from bson.objectid import ObjectId
from flask_jwt_extended import create_access_token

@pytest.fixture(autouse=True)
def clean_db():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        app.mongo.db.users.delete_many({})
        app.mongo.db.videos.delete_many({})
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
    token = create_access_token(identity=user_id)
    return token

def test_video_list_empty(client, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.get("/videos", headers=headers)
    data = response.get_json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 0

def test_video_list_with_video(client, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    app = create_app()
    with app.app_context():
        video_data = {
            "filename": "test_video.mp4",
            "filepath": "./uploads/test_video.mp4",
            "status": "Concluído",
            "created_at": app.config['ZIP_FOLDER'],
            "user_id": "60f6d7f6f6f6f6f6f6f6f6f6",
            "zip_url": "/download/frames_test.zip",
            "fps": 30,
            "frames_extracted": 10
        }
        result = app.mongo.db.videos.insert_one(video_data)
        video_id = str(result.inserted_id)
    
    
    response = client.get("/videos", headers=headers)
    data = response.get_json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0
    video = data[0]
    assert video["filename"] == "test_video.mp4"
    assert video["fps"] == 30
    assert video["frames_extracted"] == 10
