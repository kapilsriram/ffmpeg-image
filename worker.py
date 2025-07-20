import os
from redis import Redis
from rq import Worker, Queue
from tasks import merge_video_image

redis_url = os.getenv("REDIS_URL")
conn = Redis.from_url(redis_url)
queue = Queue(connection=conn)

if __name__ == '__main__':
    worker = Worker([queue], connection=conn)
    worker.work()
