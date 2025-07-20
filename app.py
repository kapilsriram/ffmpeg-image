from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/merge', methods=['POST'])
def merge_video_image():
    video = request.files['video']
    image = request.files['image']

    video_path = 'input.mp4'
    image_path = 'input.png'
    output_path = 'output.mp4'

    video.save(video_path)
    image.save(image_path)

    cmd = [
        'ffmpeg', '-y', '-i', video_path, '-i', image_path,
        '-filter_complex', '[0:v][1:v] overlay=10:10',
        '-codec:a', 'copy', output_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return f"FFmpeg error: {result.stderr}", 500
    except subprocess.TimeoutExpired:
        return "FFmpeg process timed out", 500

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
