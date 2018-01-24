#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/11/18 7:16 PM
# @Author  : xiaowa
from config import BOARD_SIZE, BLANK, BLACK, WHITE
import random
from logger import LOGGER


def get_valid_points(board, piece):
    valid_points = []
    for r in range(len(board)):
        line = board[r]
        for c in range(len(line)):
            if board[r][c] != BLANK:
                continue
            targets = get_valid_targets(board, r, c, piece)
            if targets:
                valid_points.append((r, c))
    return valid_points


def get_score(board):
    return sum([sum(e) for e in board])


def get_piece_num(board):
    return len([e for line in board for e in line if e != BLANK])


def is_point_valid(board_len, r, c):
    if r < 0 or r >= board_len:
        return False
    if c < 0 or c >= board_len:
        return False
    return True


def get_valid_targets(board, r, c, piece):
    drc = [-1, 0, 1]
    valid_targets = []

    for rd in drc:
        for cd in drc:
            if rd == 0 and cd == 0:
                continue
            step = 1
            while True:
                tmp_r = r + rd * step
                tmp_c = c + cd * step
                if not is_point_valid(len(board), tmp_r, tmp_c):
                    break
                t_piece = board[tmp_r][tmp_c]
                if t_piece == BLANK:
                    break
                if t_piece == piece:
                    if step > 1:
                        valid_targets.append((rd, cd, tmp_r, tmp_c))
                    break
                step += 1
    return valid_targets


def board2str(board):
    rs_str = "\n"
    for line in board:
        line_str = u" ".join([u"%3.0d" % e for e in line])
        line_str += u"\n"
        rs_str += line_str
    return rs_str


class Othello:
    piece_pool = [BLACK, WHITE]
    player_num = 2

    def __init__(self):
        self.board_size = BOARD_SIZE
        self.round = 0
        self.players = []
        self.board = []
        self.init_board()

    def init_board(self):
        # init board
        self.board = []
        half_small = int(self.board_size / 2) - 1
        half_big = int(self.board_size / 2)
        for i in range(self.board_size):
            self.board.append([BLANK] * self.board_size)
        self.board[half_small][half_small] = BLACK
        self.board[half_big][half_big] = BLACK
        self.board[half_small][half_big] = WHITE
        self.board[half_big][half_small] = WHITE

    def add_player(self, player):
        self.players.append(player)

    def put_piece(self, r, c, piece):
        targets = get_valid_targets(self.board, r, c, piece)
        for rd, cd, tr, tc in targets:
            tmp_r = r
            tmp_c = c
            while tmp_r != tr or tmp_c != tc:
                self.board[tmp_r][tmp_c] = piece
                tmp_r += rd
                tmp_c += cd

    def start(self):
        if len(self.players) != Othello.player_num:
            LOGGER.error(u"invalid player num:{}, expected:{}".format(len(self.players), Othello.player_num))
            return
        LOGGER.info(u"Othello game started!")
        LOGGER.info(u"choosing player...")

        offset = random.randint(0, Othello.player_num - 1)

        for idx, p in enumerate(self.piece_pool):
            tmp_player = self.players[(idx + offset) % len(self.players)]
            # self.piece_dict[p] = tmp_player
            tmp_player.set_piece(p)

        self.round = 0
        pass_time = 0
        LOGGER.info(u"start moving...")
        last_player = None

        while True:
            if pass_time == len(self.players):
                LOGGER.info(u"all players has no way to go, game is finished!")
                break
            cur_player = self.players[(self.round + offset) % len(self.players)]
            cur_piece = cur_player.piece
            if last_player:
                last_player.notify_status(self.board, cur_piece)

            self.round += 1
            LOGGER.debug(u"current board")
            LOGGER.debug(board2str(self.board))
            valid_points = get_valid_points(self.board, cur_piece)
            LOGGER.debug(u"valid points:{}".format(valid_points))
            LOGGER.info(u"round{} player[{}] putting {} ".format(self.round, cur_player, cur_player.piece))

            if not valid_points:
                valid_points.append((None, None))
            action = cur_player.play(valid_points, self.board)
            last_player = cur_player
            if action not in valid_points:
                LOGGER.error("invalid action :{}, pass this round".format(action))
                pass_time += 1
                continue
            if action == (None, None):
                LOGGER.info(u"player[{}] has no way to go".format(cur_player))
                pass_time += 1
                continue

            LOGGER.info(u"player[{}] put {} to point {}".format(cur_player, cur_piece, action))
            self.put_piece(action[0], action[1], cur_piece)
            pass_time = 0

        score = get_score(self.board)
        if score > 0:
            win_piece = BLACK
        elif score < 0:
            win_piece = WHITE
        else:
            win_piece = None
            LOGGER.info(u"THIS IS A DRAW GAME!")

        winner = None
        if win_piece:
            for player in self.players:
                LOGGER.debug(u"notifying player[{}] of reward".format(player))
                player.notify_win(win_piece)
                if player.piece == win_piece:
                    LOGGER.info(u"piece:{}[player:{}] WIN! WITH SCORE={}".format(win_piece, player, abs(score)))
                    winner = player

        LOGGER.info(u"game finish!")
        return winner
