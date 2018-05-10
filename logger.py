#!/usr/bin/env python

# encoding: utf-8

'''
 * Create File logger
 * Created by leixu on 2018/5/10
 * IDE PyCharm
'''
import sys

import logging

logger = logging.getLogger("MySpider")

formatter = logging.Formatter('%(asctime)s %(module)s %(lineno)d %(levelname)-8s: %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值
console_handler.setLevel(logging.DEBUG)

logger.addHandler(console_handler)
