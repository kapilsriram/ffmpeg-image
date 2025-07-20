from rq import Worker, Queue
from redis import Redis
import os

listen = ['default']
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = Redis.from_url(redis_url)

if __name__ == '__main__':
    worker = Worker(queues=[Queue(name, connection=conn) for name in listen])
    worker.work()
