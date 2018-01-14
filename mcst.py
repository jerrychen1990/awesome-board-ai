#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/12/18 2:45 PM
# @Author  : xiaowa
import random


class MCST_NODE:
    def __init__(self, parent_node, status=None):
        self.status = status
        self.parent_node = parent_node
        self.win_time = 0
        self.visit_time = 0
        self.action_dict = {}
        pass

    def expand(self, action_list):
        if not action_list:
            tmp_node = MCST_NODE(self)
            self.action_dict[None] = tmp_node
        else:
            for action in action_list:
                tmp_node = MCST_NODE(self)
                self.action_dict[action] = tmp_node


    def back_reward(self):
        self.win_time += 1
        if self.parent_node:
            self.parent_node.back_reward()


class MCST:
    def __init__(self):
        self.root_node = MCST_NODE(None)
        self.current_node = None
        self.node_dict = {}

    def search_dict(self, status):
        node = self.node_dict.get(status, None)
        if node:
            return node
        node = MCST_NODE(status, None)
        return node

    def expand(self, action_list):
        if not self.current_node.children_nodes:
            self.current_node.expand(action_list)

    def move(self):
        self.current_node.visit_time += 1
        if self.current_node.action_dict:
            next_action, next_node = random.choice(self.current_node.action_dict.items())
            self.current_node = next_node
            return next_action
        else:
            print(u"has no way to move!")
            return None

    def back_reward(self):
        self.current_node.back_reward()
