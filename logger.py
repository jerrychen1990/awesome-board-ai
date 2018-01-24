#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/16/18 3:41 PM
# @Author  : xiaowa


# encoding:utf8
import logging
import os

# 创建名为'spam_application'的记录器
LOGGER = logging.getLogger('othello')
LOGGER.setLevel(logging.DEBUG)

# 创建级别为DEBUG的日志处理器
file_path = './log/othello-debug.log'
base, file_name = os.path.split(file_path)
if not os.path.exists(base):
    os.makedirs(base)
#
# if not os.path.exists(file_path):
#     os.mkdir(file_path)
# os.system("mkdir -p {}".format(file_path))

fh = logging.FileHandler(file_path)
fh.setLevel(logging.DEBUG)

# 创建级别为ERROR的控制台日志处理器
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# 创建格式器，加到日志处理器中
file_formatter = logging.Formatter(u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(file_formatter)
brief_formatter = logging.Formatter(u'%(message)s')
ch.setFormatter(brief_formatter)

LOGGER.addHandler(fh)
LOGGER.addHandler(ch)
