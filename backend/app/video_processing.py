from pymongo import MongoClient
from bson.objectid import ObjectId
import cv2
import os
import zipfile
import time

def extract_frames(video_path, interval, video_id):
    output_folder = f"./zips/frames_{video_id}"
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise Exception(f"Erro ao abrir o vídeo: {video_path}")

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_index = 0
    extracted_count = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        if frame_index % (fps * interval) == 0:
            frame_filename = f"{output_folder}/frame_{extracted_count:04d}.jpg"
            cv2.imwrite(frame_filename, frame)
            extracted_count += 1

        frame_index += 1

    cap.release()

    update_video_info(video_id, fps, extracted_count)

    return output_folder, fps, extracted_count

def update_video_info(video_id, fps, extracted_count):
    mongo_uri = os.environ.get('MONGO_URI')
    if not mongo_uri:
        raise ValueError("MONGO_URI não está definida no ambiente.")

    try:
        client = MongoClient(mongo_uri)
        db = client.get_default_database()
        db.videos.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {
                "fps": fps,
                "frames_extracted": extracted_count
            }}
        )
        client.close()
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {str(e)}")
        raise

def create_zip(folder):
    zip_filename = f"frames_{int(time.time())}.zip"
    zip_filepath = os.path.join('./zips', zip_filename)

    with zipfile.ZipFile(zip_filepath, 'w') as zipf:
        for root, dirs, files in os.walk(folder):
            if not files:
                raise Exception(f"Nenhum arquivo encontrado para compactar em {folder}")
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)

    return zip_filename

