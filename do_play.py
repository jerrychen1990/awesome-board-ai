#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/12/18 4:04 PM
# @Author  : xiaowa
from othello import Othello
from player import BasePlayer, MCSTPlayer
from train import train_mcst
from logger import LOGGER

rd = 50
LOGGER.info(u"train for {} rounds".format(rd))
mcst = train_mcst(rd)


othello = Othello()
othello.show()
othello.add_player(BasePlayer(u"random player"))
othello.add_player(MCSTPlayer(u"MCST player", mcst))
othello.start()
