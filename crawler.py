#!/usr/bin/env python

# encoding: utf-8

'''
 * Create File crawler
 * Created by leixu on 2018/5/10
 * IDE PyCharm
'''
import asyncio
from enum import Enum
from concurrent.futures import ProcessPoolExecutor
import aiohttp
import os
from logger import logger
import multiprocessing

total_count = 0


class CrawlerStatus(Enum):
    FREE = 0
    BUSY = 1
    NOT_AVAILABLE = 2
    WAITING = 3


class CurrentArgInfo(object):
    pass


class Crawler(object):
    RUNNING = 0
    FREE = 0
    TOTAL = 0
    TOTAL_REQUEST = 0

    def __init__(self, loop: asyncio.AbstractEventLoop, queue):
        self.loop = loop
        self.status = CrawlerStatus.FREE
        self._s_command = None
        self.TOTAL += 1
        self.async_queue = queue
        self.task = None

    def send_command(self, command):
        self._s_command = command

    def start(self):

        async def watch_new_url():
            while True:
                if self.status == CrawlerStatus.FREE:
                    url, kwargs = await self.async_queue.get()
                    await self.fetch(url, kwargs)

        self.task = self.loop.create_task(watch_new_url())

    def end_fetch(self):
        self.RUNNING -= 1
        self.FREE += 1
        self.TOTAL_REQUEST += 1
        self.status = CrawlerStatus.FREE
        logger.warn("Process" + str(os.getpid()) + "         CurrentRequestIndex:" + str(self.TOTAL_REQUEST))

    async def fetch(self, url, kwargs):
        self.RUNNING += 1
        self.status = CrawlerStatus.BUSY

        async def _data_fetch_task(_url, _kwargs):
            async with aiohttp.ClientSession() as session:
                async with session.get(_url) as resp:
                    await resp.text()

        try:
            await _data_fetch_task(url, kwargs)
            self.end_fetch()
        except Exception as e:
            print(e)


class CrawlerCollectionManager(object):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: multiprocessing.Queue, count):
        self.loop = loop
        self.count = count
        self.queue = queue
        self.async_queue = asyncio.Queue(loop=self.loop)

    def start(self):
        for _ in range(self.count):
            crawler = Crawler(self.loop, self.async_queue)
            crawler.start()
        self.loop.create_task(self.watch_new_url())
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


def gen_process(queue, count):
    """

    :param queue: 爬取的参数传递器
    :param count: 爬虫个数
    :return:
    """
    loop = asyncio.new_event_loop()
    cm = CrawlerCollectionManager(loop, queue, count)
    cm.start()


# 生成蜘蛛群
def gen_crawler_collections(num=50, count=100, queue=None):
    """

    :param num:种群个数
    :param count: 每个群开启开启多少蜘蛛
    :return:
    """
    loop = asyncio.get_event_loop()
    p = ProcessPoolExecutor(num)
    loop.run_in_executor(p, gen_process, queue, count)
    loop.run_forever()


if __name__ == "__main__":
    m = multiprocessing.Manager()
    queue = m.Queue()
    for i in range(10000):
        queue.put(("https://www.baidu.com/", {"method": "get"}))
    gen_crawler_collections(queue=queue)
