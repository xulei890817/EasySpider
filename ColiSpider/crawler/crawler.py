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
from Coli.logger import logger
import multiprocessing

total_count = 0


class CrawlerStatus(Enum):
    FREE = 0
    BUSY = 1
    NOT_AVAILABLE = 2
    WAITING = 3


class CurrentArgInfo(object):
    pass


class FetchResult(object):
    def __init__(self):
        self.is_error = False
        self.error = None
        self.content = None
        self.ok = False

    def set_expection(self, error):
        self.is_error = True
        self.error = error

    def set_text_content(self, content):
        self.ok = True
        self.content = content


class Crawler(object):
    RUNNING = 0
    FREE = 0
    TOTAL = 0
    TOTAL_REQUEST = 0

    def __init__(self, loop: asyncio.AbstractEventLoop, queue, out_queue: asyncio.Queue):
        self.loop = loop
        self.status = CrawlerStatus.FREE
        self._s_command = None
        self.TOTAL += 1
        self.async_queue = queue
        self.out_async_queue = out_queue
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
        logger.warn("Process" + str(os.getpid()) +
                    "         CurrentRequestIndex:" + str(self.TOTAL_REQUEST))

    async def fetch(self, url, kwargs):
        self.RUNNING += 1
        self.status = CrawlerStatus.BUSY

        async def _data_fetch_task(_url, _kwargs):
            async with aiohttp.ClientSession() as session:
                async with session.get(_url) as resp:
                    fr = FetchResult()
                    content = await resp.text()
                    fr.set_text_content(content)
                    self.out_async_queue.put_nowait(fr)

        try:
            await _data_fetch_task(url, kwargs)
            self.end_fetch()
        except Exception as e:
            print(e)
            fr = FetchResult()
            fr.set_expection(e)
            self.out_async_queue.put_nowait(fr)
