from ColiSpider.worker import Worker


class Client(object):

    def __init__(self):
        self._redis_client = None
        self._redis_config = None
        self._worker_pool = []

    @property
    def redis_client(self):
        return self._redis_client

    def use_redis_client(self, config):
        self._redis_config = config

    def regist_worker(self, worker: Worker):
        self._worker_pool.append(worker)

    def start(self):
        pass
