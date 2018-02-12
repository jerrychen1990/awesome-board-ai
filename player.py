#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/11/18 7:33 PM
# @Author  : xiaowa
import random
from abc import abstractmethod
import common
from logger import LOGGER


class IPlayer:
    def __init__(self, n):
        self.name = n
        self.piece = None

    @abstractmethod
    def play(self, valid_points, board):
        pass

    @abstractmethod
    def notify_win(self, win_piece):
        pass

    @abstractmethod
    def notify_status(self, board, piece):
        pass

    def set_piece(self, piece):
        self.piece = piece

    def __repr__(self):
        return self.name


class RandPlayer(IPlayer):
    def __init__(self, n):
        self.name = n
        self.piece = None

    def play(self, valid_points, board):
        return random.choice(valid_points)

    def notify_win(self, win_piece):
        pass

    def notify_status(self, board, piece):
        pass


class FastPlayer(IPlayer):
    def __init__(self, n, fast_func):
        super(FastPlayer, self).__init__(n)
        self.fast_func = fast_func

    def play(self, valid_points, board):
        return self.fast_func((board, self.piece), valid_points)

    def notify_win(self, win_piece):
        pass

    def notify_status(self, board, piece):
        pass


class HumanPlayer(IPlayer):
    def play(self, valid_points, board):
        while True:
            action_str = input("action: >>>\n")
            action = tuple([int(e) for e in action_str.split(",")])
            if action in valid_points:
                return action
            LOGGER.warn("invalid action:{}".format(action))

    def notify_status(self, board, piece):
        pass

    def notify_win(self, win_piece):
        pass


class MCSTPlayer(IPlayer):
    @staticmethod
    def hash_status(status):
        board = status[0]
        piece = status[1]
        board_str = u"|".join([u"".join([str(e) for e in line]) for line in board])
        hash_value = board_str + "_" + str(piece)
        return hash_value

    def __init__(self, n, mcst, fast_move_func, is_train=False):
        IPlayer.__init__(self, n)
        self.mcst = mcst
        self.cur_node = mcst.root_node
        self.cur_action = None
        self.is_train = is_train
        self.fast_move_func = fast_move_func

    def play(self, valid_points, board):
        if not self.cur_node or self.cur_node.is_leaf():
            LOGGER.warn("current status not trained, use random strategy")
            status = (board, self.piece)
            action = self.fast_move_func(status=status, action_list=valid_points)
            return action
        action, _, _ = self.cur_node.select(mark_piece=self.mcst.mark_piece, c=0)
        return action

    def notify_status(self, board, piece):
        node_key = common.get_status_key((board, piece))
        self.cur_node = self.mcst.node_dict.get(node_key, None)

    def notify_win(self, win_piece):
        LOGGER.info("OK, I know")
