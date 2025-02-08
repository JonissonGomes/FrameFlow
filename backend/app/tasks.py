import os
import datetime
from celery import Celery
from pymongo import MongoClient
from bson.objectid import ObjectId
from .video_processing import extract_frames, create_zip

celery = Celery('tasks', broker=os.environ.get('CELERY_BROKER_URL'))

@celery.task
def process_video(filepath, interval, frame_count, video_id):
    extracted_frames_folder = extract_frames(filepath, interval, frame_count)
    zip_file = create_zip(extracted_frames_folder)
    
    mongo_uri = os.environ.get('MONGO_URI')
    if not mongo_uri:
        raise ValueError("MONGO_URI não está definida no ambiente.")
    
    client = MongoClient(mongo_uri)
    db = client.get_default_database()
    
    db.videos.update_one(
        {"_id": ObjectId(video_id)},
        {"$set": {
            "status": "Concluído",
            "zip_url": f"/download/{zip_file}",
            "processed_at": datetime.datetime.utcnow()
        }}
    )
    
    client.close()
    return zip_file
