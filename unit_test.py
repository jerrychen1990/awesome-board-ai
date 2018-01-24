#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/18/18 11:19 AM
# @Author  : xiaowa

import unittest
from game import OxGame, BLACK, WHITE, BLANK
import common


class GameTest(unittest.TestCase):
    def test_ox_transform(self):
        board = OxGame.get_empty_board()
        status = (board, BLACK)
        action = (1, 2)
        next_board, next_piece = OxGame.transform(status=status, action=action)
        board[1][2] = BLACK
        self.assertEqual(board, next_board)
        self.assertEqual(WHITE, next_piece)


class OxGameTest(unittest.TestCase):
    def test_related_line(self):
        board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        related_line = OxGame.related_line(board=board, action=(1, 1))
        self.assertEqual([[4, 5, 6], [2, 5, 8], [1, 5, 9], [3, 5, 7]], related_line)
        related_line = OxGame.related_line(board=OxGameTest.board, action=(2, 0))
        self.assertEqual([[7, 8, 9], [1, 4, 7], [3, 5, 7]], related_line)

    def test_fast_move(self):
        board = [[BLANK, BLANK, BLANK], [BLANK, BLACK, WHITE], [BLANK, BLANK, BLANK]]
        piece = BLACK
        status = board, piece
        action_list = OxGame.get_action_list(status)
        action, score = OxGame.fast_move(status, action_list)
        self.assertEqual(score, 3)

class CommonTest(unittest.TestCase):
    def test_get_status_key(self):
        board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        status = (board, BLACK)
        node_key = common.get_status_key(status)
        print(node_key)




if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestSuite()
    # suite.addTests([OxGameTest("test_fast_move")])
    suite.addTests([CommonTest("test_get_status_key")])
    runner.run(suite)


    # unittest.main()
