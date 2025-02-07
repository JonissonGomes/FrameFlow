from flask import Flask, Blueprint, request, send_from_directory, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from .video_processing import extract_frames, create_zip

app = Flask(__name__)

CORS(app, origins=["http://localhost:8080", "http://localhost:5000"])

bp = Blueprint('routes', __name__)

@bp.route('/upload', methods=['POST'])
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
def download_zip(zip_filename):
    return send_from_directory('./zips', zip_filename)
