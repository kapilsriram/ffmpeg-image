import subprocess

def merge_video_image(video_path, image_path, output_path='output.mp4'):
    cmd = [
        'ffmpeg', '-y', '-i', video_path, '-i', image_path,
        '-filter_complex', '[0:v][1:v] overlay=10:10',
        '-codec:a', 'copy', output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path
