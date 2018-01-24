#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/18/18 11:01 AM
# @Author  : xiaowa
import copy
import random
from abc import abstractstaticmethod, abstractmethod
from logger import LOGGER

BLACK = 1
WHITE = -1
BLANK = 0


class IChessGame:
    @staticmethod
    def is_full(board):
        return len([e for line in board for e in line if e == BLANK]) == 0

    @classmethod
    @abstractstaticmethod
    def transform(cls, status, action):
        pass

    @staticmethod
    @abstractstaticmethod
    def judge(status):
        pass

    @staticmethod
    @abstractstaticmethod
    def get_action_list(status):
        pass

    @classmethod
    @abstractstaticmethod
    def fast_move(cls, status, action_list):
        pass

    @classmethod
    def get_board_str(cls, board):
        rs_str = "\n"
        for line in board:
            line_str = u" ".join([u"%3.0d" % e for e in line])
            line_str += u"\n"
            rs_str += line_str
        return rs_str

    @classmethod
    def fast_finish(cls, status, move_func):
        iter_status = status
        while True:
            is_finish, win_piece = cls.judge(iter_status)
            if is_finish:
                return win_piece
            action_list = cls.get_action_list(iter_status)
            action = move_func(iter_status, action_list)
            iter_status = cls.transform(iter_status, action)

    def __init__(self):
        self.board = []
        self.next_piece = BLACK
        self.init_board()
        self.players = []
        self.round = 0

    @abstractmethod
    def init_board(self):
        pass

    def add_player(self, player):
        self.players.append(player)

    def get_status(self):
        return self.board, self.next_piece


class OxGame(IChessGame):
    board_size = 3
    player_num = 2
    piece_pool = (BLACK, WHITE)

    @staticmethod
    def get_action_list(status):
        board, next_piece = status
        action_list = []
        for r, line in enumerate(board):
            for c, v in enumerate(line):
                if board[r][c] == BLANK:
                    action_list.append((r, c))
        return action_list

    @staticmethod
    def judge(status):
        board, next_piece = status
        judge_list = []
        judge_list.extend(board)
        judge_list.extend([[line[r] for line in board] for r in range(OxGame.board_size)])
        judge_list.append([board[i][i] for i in range(OxGame.board_size)])
        judge_list.append([board[OxGame.board_size - 1 - i][i] for i in range(OxGame.board_size)])

        def is_same(line):
            return len(set(line)) == 1

        for to_judge in judge_list:
            if is_same(to_judge) and to_judge[0] != BLANK:
                return True, to_judge[0]
        return IChessGame.is_full(board), None

    @staticmethod
    def __line_score(line, piece):
        score = 0
        for e in line:
            if e == piece:
                score += 1
            elif e == BLANK:
                continue
            else:
                return 0
        if score == OxGame.board_size:
            return score * 10
        return score

    @staticmethod
    def related_line(board, action):
        r, c = action
        size = len(board)
        related = [board[r], [board[i][c] for i in range(size)]]
        if r == c:
            related.append([board[i][i] for i in range(size)])
        if r + c == size - 1:
            related.append([board[i][size - 1 - i] for i in range(size)])
        return related

    @classmethod
    def fast_move(cls, status, action_list):
        board, piece = status
        other_piece = OxGame.get_next_piece(piece)
        score_list = []
        for action in action_list:
            related_lines = OxGame.related_line(board, action)
            pre_score = sum([OxGame.__line_score(e, piece) for e in related_lines]) - sum(
                    [OxGame.__line_score(e, other_piece) for e in related_lines])

            test_board, _ = OxGame.transform(status, action)

            related_lines = OxGame.related_line(test_board, action)
            next_score = sum([OxGame.__line_score(e, piece) for e in related_lines]) - sum(
                    [OxGame.__line_score(e, other_piece) for e in related_lines])

            score_list.append((action, (next_score - pre_score)))

        _, max_score = max(score_list, key=lambda e: e[1])
        max_list = [e for e in score_list if e[1] == max_score]
        return random.choice(max_list)[0]

    @staticmethod
    def get_empty_board():
        board = []
        for idx in range(OxGame.board_size):
            board.append([BLANK] * OxGame.board_size)
        return board

    @staticmethod
    def is_action_valid(board, r, c):
        if r < 0 or c < 0 or r >= OxGame.board_size or c >= OxGame.board_size:
            return False
        if board[r][c] != BLANK:
            return False
        return True

    @staticmethod
    def get_next_piece(piece):
        if piece == WHITE:
            return BLACK
        if piece == BLACK:
            return WHITE
        return BLANK

    @classmethod
    def transform(cls, status, action):
        board, piece = status
        r, c = action

        next_board = copy.deepcopy(board)
        next_piece = cls.get_next_piece(piece)

        if not OxGame.is_action_valid(board=board, r=r, c=c):
            print("invalid action!")
        else:
            next_board[r][c] = piece
        return next_board, next_piece

    def __init__(self):
        super().__init__()

    def init_board(self):
        self.board = []
        for _ in range(OxGame.board_size):
            self.board.append([BLANK] * OxGame.board_size)

    def start(self):
        if len(self.players) != OxGame.player_num:
            LOGGER.error(u"invalid player num:{}, expected:{}".format(len(self.players), OxGame.player_num))
            return
        LOGGER.info(u"OX game started!")

        LOGGER.info(u"choosing player...")
        offset = random.randint(0, OxGame.player_num - 1)
        for idx, p in enumerate(OxGame.piece_pool):
            tmp_player = self.players[(idx + offset) % len(self.players)]
            tmp_player.set_piece(p)

        self.round = 0
        LOGGER.info(u"start moving...")
        winner = None
        win_piece = None

        while True:
            cur_player = self.players[(self.round + offset) % len(self.players)]
            cur_piece = cur_player.piece

            LOGGER.info(u"current round:{},current piece :{}".format(self.round, cur_piece))
            LOGGER.info(u"current board")
            LOGGER.info(self.get_board_str(self.board))
            cur_status = (self.board, cur_piece)
            is_finish, win_piece = OxGame.judge(cur_status)
            if is_finish:
                break
            for player in self.players:
                player.notify_status(*cur_status)

            LOGGER.info(u"player[{}] putting {}... ".format(cur_player, cur_player.piece))
            valid_points = OxGame.get_action_list(cur_status)
            LOGGER.debug(u"valid points:{}".format(valid_points))
            self.round += 1
            action = cur_player.play(valid_points, self.board)
            if action not in valid_points:
                LOGGER.error("invalid action :{}, pass this round".format(action))

            LOGGER.info(u"player[{}] put {} to point {}".format(cur_player, cur_piece, action))
            self.board, _ = self.transform(status=cur_status, action=action)

        for player in self.players:
            player.notify_win(win_piece)
            if player.piece == win_piece:
                winner = player
                LOGGER.info(u"player:[{}] win".format(winner))
        if not winner:
            LOGGER.info(u"it's a draw game!")
        LOGGER.info(u"game finish!")
        return winner
