#!usr/bin/env python3
# -*- coding:utf-8 -*-


import copy


class Board(object):
    """
    A class used to represent game board of Gomoku.
    """
    def __init__(self, width=7, height=7):
        self.width = width
        self.height = height
        
        # Initialize game board
        self.board = []
        for i in range(height):
            line = []
            for j in range(width):
                line.append('.')
            self.board.append(line)

    def copy(self):
        """Copy function."""
        temp = Board(self.width, self.height)
        temp.board = copy.deepcopy(self.board)
        return temp

    def check_horizontal_state(self, position):
        """
        Check horizontal state for a position →

        Args:
            position(tuple): coordinates
        Returns:
            state(list): x for space
                         eg. ['red', 'red', 'x', 'blue', 'red']
        """
        state = []
        x_pos = position[0]
        y_pos = position[1]
        

        if y_pos > self.width - 5:
            return state

        for i in range(y_pos, y_pos + 5):
            char = self.board[x_pos][i]
            if char.islower():
                state.append('red')
            elif char.isupper():
                state.append('blue')
            else:
                state.append('x')
        return state

    def check_vertical_state(self, position):
        """
        Check vertical state for a position ↓

        Args:
            position(tuple): coordinates
        Returns:
            state(list): x for space
                         eg. ['red', 'red', 'x', 'blue', 'red']
        """
        state = []
        x_pos = position[0]
        y_pos = position[1]

        if x_pos > self.height - 5:
            return state

        for i in range(x_pos, x_pos + 5):
            char = self.board[i][y_pos]
            if char.islower():
                state.append('red')
            elif char.isupper():
                state.append('blue')
            else:
                state.append('x')
        return state

    def check_diag_1_state(self, position):
        """
        Check diagonal state for a position from top left
        to bottom right ↘

        Args:
            position(tuple): coordinates
        Returns:
            state(list): x for space
                         eg. ['red', 'red', 'x', 'blue', 'red']
        """
        state = []
        x_pos = position[0]
        y_pos = position[1]

        if (x_pos > self.height - 5) or (y_pos > self.width - 5):
            return state

        for i in range(5):            
            char = self.board[x_pos + i][y_pos + i]
            if char.islower():
                state.append('red')
            elif char.isupper():
                state.append('blue')
            else:
                state.append('x')
        return state

    def check_diag_2_state(self, position):
        """
        Check diagonal state for a position from top right
        to bottom left ↙

        Args:
            position(tuple): coordinates
        Returns:
            state(list): x for space
                         eg. ['red', 'red', 'x', 'blue', 'red']
        """
        state = []
        x_pos = position[0]
        y_pos = position[1]

        if (x_pos > self.height - 5) or (y_pos < 4):
            return state

        for i in range(5):            
            char = self.board[x_pos + i][y_pos - i]
            if char.islower():
                state.append('red')
            elif char.isupper():
                state.append('blue')
            else:
                state.append('x')
        return state

    def mark(self, x, y, char):
        """
        Mark an intersection by coordinates.

        Args:
            x(int): x-th line
            y(int): y-th position
            char(char): symbol used to mark
        Returns:
            (None)
        """
        self.board[x][y] = char

    def print_board(self):
        """
        Print out game board

        Args: (None)
        Returns: (None)
        """
        for line in self.board:
            print(''.join(line))
