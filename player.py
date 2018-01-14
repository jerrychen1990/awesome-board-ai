#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/11/18 7:33 PM
# @Author  : xiaowa
import random

class BasePlayer:
    def __init__(self, n):
        self.name = n

    def play(self, valid_points, board, piece):
        return random.choice(valid_points)

    def __repr__(self):
        return self.name


class MCSTPlayer(BasePlayer):
    def __init__(self, mcst):
        super.__init__()
        self.mcst = mcst

    def play(self, valid_points, board, piece):
        status = (board, piece)
        if self.mcst.current_node.staus != (board, piece):
            print(u"node track failed")
            node = self.mcst.search_dict(status)
            self.mcst.current_node = node

        self.mcst.expand(valid_points)
        next_node




