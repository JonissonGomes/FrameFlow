from flask import Flask, Blueprint, request, send_from_directory, jsonify, current_app
from flask_cors import cross_origin
import os
from werkzeug.utils import secure_filename
from .video_processing import extract_frames, create_zip

bp = Blueprint('routes', __name__)

@bp.route('/upload', methods=['POST'])
@cross_origin()
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join('./uploads', filename)
        file.save(filepath)

        frame_count = int(request.form['frame_count'])
        interval = int(request.form['interval'])

        extracted_frames_folder = extract_frames(filepath, interval, frame_count)
        zip_file = create_zip(extracted_frames_folder)

        return jsonify({
            "message": "File processed successfully",
            "zip_url": f"/download/{zip_file}"
        })

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