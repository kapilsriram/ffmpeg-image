import os
import requests

def merge_video_image(video_path, image_path):
    output_path = 'output.mp4'

    cmd = [
        'ffmpeg', '-y', '-i', video_path, '-i', image_path,
        '-filter_complex', '[0:v][1:v] overlay=10:10',
        '-codec:a', 'copy', output_path
    ]
    subprocess.run(cmd, check=True)

    # Send to Make.com webhook
    webhook_url = os.getenv("MAKE_WEBHOOK_URL")
    if webhook_url:
        with open(output_path, 'rb') as f:
            requests.post(webhook_url, files={'file': f})
    
    return output_path
