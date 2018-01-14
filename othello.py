#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/11/18 7:16 PM
# @Author  : xiaowa
from prop import BOARD_SIZE, BLANK, BLACK, WHITE
from player import BasePlayer
import random


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


class Othello:
    piece_pool = [BLACK, WHITE]
    player_num = 2

    def __init__(self):
        self.board_size = BOARD_SIZE
        self.board = []
        self.round = 0
        self.players = []
        self.piece_dict = {}


        # init board
        half_small = int(self.board_size / 2) - 1
        half_big = int(self.board_size / 2)
        for i in range(self.board_size):
            self.board.append([BLANK] * self.board_size)
        self.board[half_small][half_small] = BLACK
        self.board[half_big][half_big] = BLACK
        self.board[half_small][half_big] = WHITE
        self.board[half_big][half_small] = WHITE

    def show(self):
        # print(u"current round:{}".format(self.round))
        print(u"current board")
        for line in self.board:
            line_str = u" ".join([u"%3.0d" % e for e in line])
            print(line_str)

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
            print(u"invalid player num:{}, expected:{}".format(len(self.players, Othello.player_num)))
            return
        print(u"Othello game started!")
        print(u"choosing player...")
        idx = random.randint(0, Othello.player_num - 1)
        for p in self.piece_pool:
            self.piece_dict[p] = self.players[idx % len(self.players)]
            idx += 1
        self.round = 0
        pass_time = 0

        idx = 0
        while True:
            piece = self.piece_pool[idx % len(self.piece_pool)]
            cur_player = self.piece_dict[piece]

            if pass_time == len(self.players):
                print(u"game finish!")
                score = get_score(self.board)
                if score > 0:
                    print(u"BLACK[player:{}] WIN WITH SCORE={}!".format(self.piece_dict[BLACK], score))
                elif score < 0:
                    print(u"WHITE[player:{}] WIN! WITH SCORE={}".format(self.piece_dict[WHITE], -score))
                else:
                    print(u"THIS IS A DRAW GAME!")
                break

            valid_points = get_valid_points(self.board, piece)
            if not valid_points:
                print(u"player:{} has no way to go".format(cur_player))
                pass_time += 1
            else:
                self.round += 1
                print(u"round{} player:{} playing...".format(self.round, cur_player))
                r, c = cur_player.play(valid_points, self.board, piece)
                print(u"{} put {} to  point({},{}))".format(cur_player, piece, r, c))
                self.put_piece(r, c, piece)
                pass_time = 0
                self.show()
            idx += 1


