import cv2
import os
import zipfile
import time

def extract_frames(video_path, interval, frame_count):
    output_folder = './extracted_frames'
    os.makedirs(output_folder, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    frame_index = 0
    frame_count_current = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count_current < frame_count and frame_index % interval == 0:
            frame_filename = f"{output_folder}/frame_{frame_count_current:04d}.jpg"
            cv2.imwrite(frame_filename, frame)
            frame_count_current += 1
        
        frame_index += 1
    
    cap.release()
    return output_folder
