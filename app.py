from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
from tasks import merge_video_image
import os

app = Flask(__name__)

# Get Redis URL from Railway environment variable
redis_url = os.getenv("REDIS_URL")
redis_conn = Redis.from_url(redis_url)
queue = Queue(connection=redis_conn)

@app.route('/merge', methods=['POST'])
def merge():
    video = request.files['video']
    image = request.files['image']

    # Save uploaded files temporarily
    video_path = '/tmp/input.mp4'
    image_path = '/tmp/input.png'
    output_path = '/tmp/output.mp4'

    video.save(video_path)
    image.save(image_path)

    # Enqueue the background job
    job = queue.enqueue(merge_video_image, video_path, image_path, output_path)

    return jsonify({"job_id": job.get_id(), "status": "queued"})

if __name__ == '__main__':
    app.run(debug=True)
