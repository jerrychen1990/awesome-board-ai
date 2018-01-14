#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/12/18 10:53 AM
# @Author  : xiaowa
from othello import get_valid_targets

board = [[1, 1, -1, 1, -1, -1, 0, 0],
         [0, 1, 1, -1, -1, 0, 0, 0],
         [-1, 1, -1, -1, -1, 1, 0, -1],
         [-1, 1, -1, -1, 1, 1, -1, 0],
         [-1, -1, -1, 1, 1, -1, 0, 0],
         [-1, 1, -1, 1, -1, 1, 0, 0],
         [-1, 1, 1, -1, 1, -1, 0, 0],
         [1, 1, 0, 1, -1, 1, -1, 0]]

targets = get_valid_targets(board, 4, 6, 1)
print(targets)
