from flask import Flask, request, send_file
import subprocess

app = Flask(__name__)

@app.route('/merge', methods=['POST'])
def merge_video_image():
    video = request.files['video']
    image = request.files['image']

    video.save('input.mp4')
    image.save('input.png')

    output = 'output.mp4'

    cmd = [
        'ffmpeg', '-y', '-i', 'input.mp4', '-i', 'input.png',
        '-filter_complex', '[0:v][1:v] overlay=10:10',
        '-codec:a', 'copy', output
    ]

    subprocess.run(cmd, check=True)
    return send_file(output, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
