#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/12/18 4:03 PM
# @Author  : xiaowa

from mcst import MCST
from othello import Othello, BLACK, get_valid_points

if __name__ == u'__main__':
    mcst = MCST()
    train_round = 100
    for idx in range(train_round):
        print(u"train_round:{}".format(idx))
        othello = Othello()
        idx = 0
        piece_pool = othello.piece_pool
        while True:
            status = (othello.board, piece_pool[idx % len(piece_pool)])
            mcst.current_node.status = status
            valid_points = get_valid_points(*status)
            mcst.expand(valid_points)
            action = mcst.move()







            valid_points = get_valid_points(mcst.current_node.status)
            mcst.expand(valid_points)
