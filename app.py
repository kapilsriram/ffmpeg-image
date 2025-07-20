from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
from tasks import merge_video_image

app = Flask(__name__)
q = Queue(connection=Redis())

@app.route('/merge', methods=['POST'])
def enqueue_merge():
    video = request.files['video']
    image = request.files['image']

    video.save('input.mp4')
    image.save('input.png')

    job = q.enqueue(merge_video_image, 'input.mp4', 'input.png', 'output.mp4')
    return jsonify({'job_id': job.get_id()})
