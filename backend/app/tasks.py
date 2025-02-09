import os
import datetime
from celery import Celery
from pymongo import MongoClient
from bson.objectid import ObjectId
from .video_processing import extract_frames, create_zip

celery = Celery('tasks', broker=os.environ.get('CELERY_BROKER_URL'))

@celery.task
def process_video(filepath, interval, video_id):
    mongo_uri = os.environ.get('MONGO_URI')
    if not mongo_uri:
        raise ValueError("MONGO_URI não está definida no ambiente.")

    client = MongoClient(mongo_uri)
    db = client.get_default_database()

    try:
        extracted_frames_folder, fps, frames_extracted = extract_frames(filepath, interval, video_id)

        zip_file = create_zip(extracted_frames_folder)

        db.videos.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {
                "status": "Concluído",
                "zip_url": f"/download/{zip_file}",
                "fps": fps,
                "frames_extracted": frames_extracted,
                "processed_at": datetime.datetime.utcnow()
            }}
        )

        client.close()
        return zip_file

    except Exception as e:
        error_message = str(e)

        db.videos.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {
                "status": "Falha no processamento",
                "error": error_message
            }}
        )

        client.close()
        raise e