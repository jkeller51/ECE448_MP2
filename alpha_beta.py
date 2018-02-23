#!usr/bin/env python3
# -*- coding:utf-8 -*-


from board import Board
from agent import Agent


class AlphaBeta(Agent):
    """ Inherit from class 'Agent', used to represent an agent."""
    def __init__(self, color):
        super().__init__(color)
        self.expanded_nodes = 0
        self.type = 'alpha_beta'
    pass
