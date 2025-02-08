import datetime
import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from .tasks import process_video

bp = Blueprint('routes', __name__)

@bp.route('/upload', methods=['POST'])
@jwt_required()
@cross_origin()
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        frame_count = int(request.form['frame_count'])
        interval = int(request.form['interval'])
    except (KeyError, ValueError):
        return jsonify({"error": "Parâmetros inválidos"}), 400

    user_id = get_jwt_identity()

    video_data = {
        "filename": filename,
        "filepath": filepath,
        "status": "Processando",
        "created_at": datetime.datetime.utcnow(),
        "user_id": user_id,
        "zip_url": ""
    }
    video_doc = current_app.mongo.db.videos.insert_one(video_data)
    video_id = str(video_doc.inserted_id)

    task = process_video.delay(filepath, interval, frame_count, video_id)
    
    return jsonify({
        "message": "Video processing started.",
        "task_id": task.id,
        "video_id": video_id
    })
    
@bp.route('/video_status/<video_id>', methods=['GET'])
@jwt_required()
@cross_origin()
def video_status(video_id):
    from bson.objectid import ObjectId
    mongo = current_app.mongo
    video = mongo.db.videos.find_one({"_id": ObjectId(video_id)})
    if video:
        return jsonify({
            "id": str(video["_id"]),
            "filename": video["filename"],
            "status": video["status"],
            "zip_url": video.get("zip_url", ""),
            "created_at": video["created_at"].strftime("%Y-%m-%d %H:%M:%S") if "created_at" in video else ""
        })
    else:
        return jsonify({"error": "Vídeo não encontrado"}), 404

@bp.route('/videos', methods=['GET'])
@jwt_required()
@cross_origin()
def list_videos():
    user_id = get_jwt_identity()
    mongo = current_app.mongo
    videos_cursor = mongo.db.videos.find({"user_id": user_id})
    videos = []
    for video in videos_cursor:
        videos.append({
            "id": str(video["_id"]),
            "filename": video["filename"],
            "status": video["status"],
            "zip_url": video.get("zip_url", ""),
            "created_at": video["created_at"].strftime("%Y-%m-%d %H:%M:%S") if "created_at" in video else ""
        })
    return jsonify(videos)


@bp.route('/download/<zip_filename>', methods=['GET'])
@cross_origin()
def download_zip(zip_filename):
    zip_folder = os.path.join(os.getcwd(), 'zips')
    file_path = os.path.join(zip_folder, zip_filename)

    if os.path.exists(file_path):
        return send_from_directory(zip_folder, zip_filename)
    else:
        current_app.logger.error(f"Arquivo {zip_filename} não encontrado.")
        return jsonify({"error": "Arquivo não encontrado"}), 404
    
@bp.route('/test-db-connection', methods=['GET'])
@cross_origin()
def test_db():
    try:
        uri = current_app.config.get('MONGO_URI')
        current_app.logger.info(f"MONGO_URI: {uri}")
        result = current_app.mongo.db.command("ping")
        return jsonify({"message": "Conexão com o MongoDB bem-sucedida", "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
