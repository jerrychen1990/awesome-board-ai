#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/12/18 4:04 PM
# @Author  : xiaowa
from othello import Othello
from player import BasePlayer

othello = Othello()
othello.show()
othello.add_player(BasePlayer(u"aaa"))
othello.add_player(BasePlayer(u"bbb"))
othello.start()
