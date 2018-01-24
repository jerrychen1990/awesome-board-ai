#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/12/18 2:45 PM
# @Author  : xiaowa
import math
import common
import copy
from logger import LOGGER
import random


class MCST_NODE:
    def __init__(self, status=None):
        self.status = copy.deepcopy(status)
        self.piece = status[1]
        self.win_time = 0
        self.visit_time = 0
        self.action_dict = {}
        pass

    def is_leaf(self):
        return not self.action_dict

    def get_value(self, is_same_piece):
        if self.visit_time == 0:
            return 0.5
        score = self.win_time / self.visit_time
        if not is_same_piece:
            score = 1 - score
        return score

    def select(self, mark_piece, c):
        smooth = 0.01
        father_visit = self.visit_time + len(self.action_dict.items()) * smooth

        def get_score(node, c_value, fv, is_same_piece):
            return node.get_value(is_same_piece) + c_value * pow((math.log(fv) / (node.visit_time + smooth)), 0.5)

        select_list = [(action, node, get_score(node, c, father_visit, self.piece == mark_piece)) for action, node in
                       self.action_dict.items()]

        _, _, max_score = max(select_list, key=lambda e: e[2])
        sorted_select_list = sorted(select_list, key=lambda e: e[2], reverse=True)

        LOGGER.info(u"|".join("{}:[{}/{}]{:.3f}".format(action, node.win_time, node.visit_time,
                                                        value) for action, node, value in sorted_select_list))
        max_nodes = [e for e in sorted_select_list if e[2] == max_score]

        selected = random.choice(max_nodes)
        LOGGER.info("select:{}".format(selected))
        return selected

    def rand_select(self):
        action, next_node = random.choice(list(self.action_dict.items()))
        return next_node

    def update(self, win_score):
        self.visit_time += 1
        self.win_time += win_score

    def expand(self, action_list, transform_func):
        for action in action_list:
            next_status = transform_func(status=self.status, action=action)
            tmp_node = MCST_NODE(status=next_status)
            self.action_dict[action] = tmp_node

    def __repr__(self):
        return u"{}/{},{}".format(self.win_time, self.visit_time, self.status)


class MCST:
    def __init__(self, mark_piece, c=1.96, hash_func=lambda e: e):
        self.mark_piece = mark_piece
        self.root_node = None
        self.node_dict = {}
        self.total_round = 0
        self.c = c
        self.hash_func = hash_func
        self.node_stack = []

    def selection(self, node):
        self.node_stack.append(node)
        if node.is_leaf():
            return node
        _, next_node, _ = node.select(mark_piece=self.mark_piece, c=self.c)
        return self.selection(next_node)

    @staticmethod
    def expansion(node, action_list, transform_func):
        node.expand(action_list=action_list, transform_func=transform_func)

    def back_progression(self, win_piece):
        win_score = 0
        # draw
        if not win_piece:
            win_score = 0.5
        elif win_piece == self.mark_piece:
            win_score = 1
        while self.node_stack:
            cur_node = self.node_stack.pop()
            cur_node.update(win_score)
            self.register_node(cur_node)

    def register_node(self, node):
        node_key = common.get_status_key(node.status)
        if node_key not in self.node_dict.keys():
            self.node_dict[node_key] = node

    def train(self, game, fast_move_func):
        self.node_stack = []
        leaf_node = self.selection(self.root_node)
        is_finish, win_piece = game.judge(leaf_node.status)
        if is_finish:
            LOGGER.info("game finish")
            self.back_progression(win_piece)
            return
        action_list = game.get_action_list(leaf_node.status)
        self.expansion(node=leaf_node, action_list=action_list, transform_func=game.transform)
        new_node = leaf_node.rand_select()
        self.node_stack.append(new_node)
        win_piece = game.fast_finish(status=new_node.status, move_func=game.fast_move)
        LOGGER.info("{} win".format(win_piece))
        self.back_progression(win_piece)
