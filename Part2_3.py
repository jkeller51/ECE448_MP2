#!usr/bin/env python3
# -*- coding:utf-8 -*-


import time
from board import Board
from agent import Agent
from reflex import Reflex
from minimax import Minimax
from alpha_beta import AlphaBeta
from stochastic import Stochastic


if __name__ == '__main__':
    start = time.time()
    
    # Initialize game board
    gameboard = Board()

    # Initialize red agent
    idx = input('Please choose a type for RED:\n'
                '1. Stochastic\n'
                '2. Alpha Beta\n')
    if idx == '1':
        RED = Stochastic('red')
    elif idx == '2':
        RED = AlphaBeta('red')

    # Initialize blue agent
    idx = input('Please choose a type for BLUE:\n'
                '1. Stochastic\n'
                '2. Alpha Beta\n')
    if idx == '1':
        BLUE = Stochastic('blue')
    elif idx == '2':
        BLUE = AlphaBeta('blue')

    # Mark order or two agents
    _red_ = 1
    _blue_ = 0

    # Count number of moves
    red_moves = 0
    blue_moves = 0

    # Play
    while (RED.win_lose_tie(gameboard) == 'UNFINISHED'):
        if _red_ == 1:
            if RED.type == 'stochastic':
                pos = RED.find_move(gameboard, N=10)
            elif RED.type == 'alpha_beta':
                pos = RED.find_move(gameboard, depth=2)
            RED.make_move(pos, gameboard)
            red_moves += 1
            if RED.type == 'stochastic':
                print('red {0}-th move \t {1} nodes expanded \t prob {2:.2f}'.format(
                      red_moves, RED.expanded_nodes, RED.probability))
            else:
                print('red {0}-th move \t {1} nodes expanded'.format(
                      red_moves, RED.expanded_nodes))
            RED.expanded_nodes = 0

        if _blue_ == 1:
            if BLUE.type == 'stochastic':
                pos = BLUE.find_move(gameboard, N=10)
            elif BLUE.type == 'alpha_beta':
                pos = BLUE.find_move(gameboard, depth=2)
            BLUE.make_move(pos, gameboard)
            blue_moves += 1
            if BLUE.type == 'stochastic':
                print('blue {0}-th move \t {1} nodes expanded \t prob {2:.2f}'.format(
                      blue_moves, BLUE.expanded_nodes, BLUE.probability))
            else:
                print('blue {0}-th move \t {1} nodes expanded'.format(
                      blue_moves, BLUE.expanded_nodes))
            BLUE.expanded_nodes = 0

        _red_, _blue_ = _blue_, _red_

    # Output
    print()
    gameboard.print_board()
    end = time.time()
    print()
    print('Time used: {0:.3f} minutes.'.format((end - start) / 60))
    print('RED {0}s!'.format(RED.win_lose_tie(gameboard)))
