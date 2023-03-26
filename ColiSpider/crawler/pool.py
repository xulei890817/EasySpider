
import asyncio
from concurrent.futures import ProcessPoolExecutor
from Coli.logger import logger
import multiprocessing
from ColiSpider.crawler.crawler import Crawler


class CrawlerCollectionManager(object):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: multiprocessing.Queue, out_queue: multiprocessing.Queue, count):
        self.loop = loop
        self.count = count
        self.queue = queue
        self.out_queue = out_queue
        self.async_queue = asyncio.Queue(loop=self.loop)
        self.async_out_queue = asyncio.Queue(loop=self.loop)

    def start(self):
        for _ in range(self.count):
            crawler = Crawler(self.loop, self.async_queue)
            crawler.start()
        self.loop.create_task(self.watch_new_url())
        self.loop.create_task(self.watch_result())
        self.loop.run_forever()

    async def watch_new_url(self):
        while True:
            try:
                url, args = self.queue.get_nowait()
                self.async_queue.put_nowait((url, args))
            except Exception:
                await asyncio.sleep(0.1)
            finally:
                await asyncio.sleep(0.001)

    async def watch_result(self):
        while True:
            try:
                _result = self.async_out_queue.get_nowait()
                self.out_queue.put_nowait(_result)
            except Exception:
                await asyncio.sleep(0.1)
            finally:
                await asyncio.sleep(0.001)


def gen_process(queue, out_queue, count):
    """

    :param queue: 爬取的参数传递器
    :param count: 爬虫个数
    :return:
    """
    loop = asyncio.new_event_loop()
    cm = CrawlerCollectionManager(loop, queue, out_queue, count)
    cm.start()


# 生成蜘蛛群
def gen_crawler_collections(num=50, count=100, queue=None, out_queue=None):

    loop = asyncio.get_event_loop()
    p = ProcessPoolExecutor(num)
    loop.run_in_executor(p, gen_process, queue, out_queue, count)


if __name__ == "__main__":
    m = multiprocessing.Manager()
    queue = m.Queue()
    for i in range(10000):
        queue.put(("https://www.baidu.com/", {"method": "get"}))
    gen_crawler_collections(queue=queue)
