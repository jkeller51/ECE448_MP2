#!usr/bin/env python3
# -*- coding:utf-8 -*-


from board import Board


class Agent(object):
    """ 
    Meta-class of all agents.
    """
    def __init__(self, color):
        self.color = color
        if color == 'red':
            self.opponent_color = 'blue'
        else:
            self.opponent_color = 'red'
        self.count_step = 0
        self.steps = []

        # Initialize agent steps
        if color == 'red':
            for i in range(ord('a'), ord('z')+1):
                self.steps.append(chr(i))
        elif color == 'blue':
            for i in range(ord('A'), ord('Z')+1):
                self.steps.append(chr(i))

    def _all_valid_moves(self, gameboard):
        """
        Find all possible moves.

        Args:
            gameboard(Board): game board
        Returns:
            moves(list): list of coordinates to place a stone
        """
        moves = []
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                if gameboard.board[x][y] == '.':
                    moves.append((x,y))
        return moves

    def choose_move(self, moves):
        """ Choose a move from a list, which follows all rules.

        Args:
            moves(list): list of tuples, each tuple is a coordinate pair
        Returns:
            best_move(tuple)
        """
        temp = list(set(moves))
        temp.sort(key=lambda x: (x[1], -1*x[0]))
        best_move = temp[0]
        return best_move

    def make_move(self, position, gameboard):
        """
        Make a move

        Args:
            position(tuple): coordinates of an intersection
            gameboard(Board): game board
        Returns:
            (None)
        """
        x_pos = position[0]
        y_pos = position[1]
        char = self.steps[0]
        self.count_step += 1
        gameboard.mark(x_pos, y_pos, char)

        # Remove this marker
        self.steps.remove(char)
