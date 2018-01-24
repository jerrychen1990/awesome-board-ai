#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/17/18 4:11 PM
# @Author  : xiaowa
import train
import collections
from player import BasePlayer, MCSTPlayer
from logger import LOGGER
from game import OxGame


def compete(game, p1, p2, compete_round=100):
    compete_game = game()
    compete_game.add_player(p1)
    compete_game.add_player(p2)
    player_board = collections.defaultdict(int)
    for rd in range(compete_round):
        LOGGER.info("compete round[{}]".format(rd))
        compete_game.init_board()
        winner = compete_game.start()
        player_board[winner] += 1
    LOGGER.info("compete result, player_board:{}".format(player_board))


if __name__ == u'__main__':
    the_game = OxGame()
    train_round = 100
    mcst = train.train_mcst(the_game, 1000)
    LOGGER.info("after {} round training, mcts's explored node num:{}".format(train_round, len(mcst.node_dict.keys())))

    player1 = MCSTPlayer(n="mcts-player", mcst=mcst, fast_move_func=the_game.fast_move)
    player2 = BasePlayer(n="rand-player")
    compete(OxGame, player1, player2, compete_round=100)
