#!usr/bin/env python3
# -*- coding:utf-8 -*-


from board import Board
from agent import Agent
from reflex import Reflex


if __name__ == '__main__':
    # Initialize game board
    gameboard = Board()
    RED = Reflex('red')
    BLUE = Reflex('blue')
    RED.make_move((5,1),gameboard)
    BLUE.make_move((1,5), gameboard)

    # Mark order or two agents
    _red_ = 1
    _blue_ = 0

    # Play
    while (RED.win_lose_tie(gameboard) == 'UNFINISHED'):
        if _red_ == 1:
            pos = RED.find_move(gameboard)
            RED.make_move(pos, gameboard)

        if _blue_ == 1:
            pos = BLUE.find_move(gameboard)
            BLUE.make_move(pos, gameboard)

        _red_, _blue_ = _blue_, _red_

    # Output
    print()
    gameboard.print_board()
        
