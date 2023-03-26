import multiprocessing
from ColiSpider.crawler.pool import gen_crawler_collections
from ColiSpider.worker import RunTypeEnum, Worker


class ParserWorker(Worker):
    """解析者,负责解析文本内容"""
    TOPIC = None

    def __init__(self):
        super().__init__()

    def _self_check(self):
        if self.TOPIC == None:
            raise Exception("must set a topic before calling ThisWorker")

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