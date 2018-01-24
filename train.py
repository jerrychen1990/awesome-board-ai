#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/12/18 4:03 PM
# @Author  : xiaowa

from common import random_move
from game import OxGame
from logger import LOGGER
from mcst import MCST, MCST_NODE
from othello import BLACK

def train_mcst(game, train_round=200):
    mcst = MCST(BLACK)
    status = game.get_status()
    mcst.root_node = MCST_NODE(status=status)

    for idx in range(train_round):
        LOGGER.info("train round[{}]".format(idx))
        mcst.train(game, fast_move_func=random_move)
    return mcst


if __name__ == u'__main__':
    ox = OxGame()
    rs_mcst = train_mcst(game=ox, train_round=500)
    LOGGER.info("train finished")
