import multiprocessing
from ColiSpider.crawler.pool import gen_crawler_collections
from ColiSpider.worker import RunTypeEnum, Worker


class ListenerWorker(Worker):
    """监听者，负责监听符合一定条件的URL"""
    TOPIC = None

    def __init__(self):
        super().__init__()

    def _self_check(self):
        if self.TOPIC == None:
            raise Exception("must set a topic before calling ThisWorker")

    def create_crawler_pool(self):
        m = multiprocessing.Manager()
        in_queue = m.Queue()
        out_queue = m.Queue()
        gen_crawler_collections(queue=in_queue)

    def push_next(self, topic=None, input=None):
        pass

    class _Config:
        # 蜘蛛数量
        spider_nums = 30
        # pool nums
        pool_nums = 10
        # run_type
        run_type = RunTypeEnum.PROCESS
        # use_base64
        use_base64 = False
        # redis_config
        redis_config = None
        # input_style
        input_style = None
        # output_style
        output_style = None
