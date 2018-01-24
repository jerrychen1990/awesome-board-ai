#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/12/18 10:53 AM
# @Author  : xiaowa
from othello import get_valid_targets
# from ox import OX
# from player import BasePlayer
#
# ox = OX()
# ox.add_player(BasePlayer(n="1"))
# ox.add_player(BasePlayer(n="2"))
# rs = ox.start()
# print(rs)
from abc import abstractmethod, abstractstaticmethod, ABCMeta


class A(metaclass=ABCMeta):
    @classmethod
    @abstractstaticmethod
    def get_a(cls):
        pass

    @classmethod
    @abstractstaticmethod
    def get_b(cls):
        pass

    @classmethod
    def get_sum(cls):
        return cls.get_a() + cls.get_b()


class B(A):
    @staticmethod
    def get_a():
        return 1

    @staticmethod
    def get_b():
        return 2


print(A.__dict__)

print(B.get_a())
print(B.get_b())
print(B.get_sum())





# print(b.get_sum())
