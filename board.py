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

    def terminate(self):
        """ Check if game terminates"""
        if self.check_tie() or self.check_win():
            return True
        else:
            return False

    def check_tie(self):
        """
        Check if current state is a tie.

        Args: (None)
        Returns: (Boolean)
        """
        for line in self.board:
            if '.' in line:
                return False
        return True

    def check_win(self):
        """
        Check if either side wins

        Args: (None)
        Returns: (Boolean)
        """
        situation = [['red'] * 5,
                     ['blue'] * 5]
        
        for x in range(self.height):
            for y in range(self.width):
                position = (x, y)
                h = self.check_horizontal_state(position)
                if h in situation:
                    return True

                v = self.check_vertical_state(position)
                if v in situation:
                    return True

                d1 = self.check_diag_1_state(position)
                if d1 in situation:
                    return True

                d2 = self.check_diag_2_state(position)
                if d2 in situation:
                    return True

        return False

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
