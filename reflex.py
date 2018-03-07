#!usr/bin/env python3
# -*- coding:utf-8 -*-


from board import Board
from agent import Agent


class Reflex(Agent):
    """ Inherit from class 'Agent', used to represent an agent."""
    def __init__(self, color):
        super().__init__(color)
        self.expanded_nodes = 0
        self.type = 'reflex'
        
    def check_going_to_win(self, position, gameboard):
        """ Check if only one more move is needed to win in terms of
        one particular position.

        Args:
            position(tuple): coordinates of current position to check
            gameboard(Board): game board
        Returns:
            moves(list): list of tuples, recording positions to win
        """
        x_pos = position[0]
        y_pos = position[1]
        moves = []

        # Check →
        h = gameboard.check_horizontal_state(position)
        if (h.count(self.color) == 4) and (h.count('x') == 1):
            relative_loc = h.index('x')
            moves.append((x_pos, y_pos + relative_loc))

        # Check ↓
        v = gameboard.check_vertical_state(position)
        if (v.count(self.color) == 4) and (v.count('x') == 1):
            relative_loc = v.index('x')
            moves.append((x_pos + relative_loc, y_pos))

        # Check ↘
        d1 = gameboard.check_diag_1_state(position)
        if (d1.count(self.color) == 4) and (d1.count('x') == 1):
            relative_loc = d1.index('x')
            moves.append((x_pos + relative_loc, y_pos + relative_loc))
        
        # Check ↙
        d2 = gameboard.check_diag_2_state(position)
        if (d2.count(self.color) == 4) and (d2.count('x') == 1):
            relative_loc = d2.index('x')
            moves.append((x_pos + relative_loc, y_pos - relative_loc))

        return moves

    def check_opponent_4(self, position, gameboard):
        """ Check if opponent has got unbroken chain of 4 stones.

        Args:
            position(tuple): coordinates of current position to check
            gameboard(Board): game board
        Returns:
            moves(list): list of tuples, recording positions to move
        """
        if self.color == 'red':
            opponent_color = 'blue'
        else:
            opponent_color = 'red'
            
        x_pos = position[0]
        y_pos = position[1]
        moves = []        
        situation = [['x'] + [opponent_color]*4,
                     [opponent_color]*4 + ['x']] # What we should find here

        # Check →
        h = gameboard.check_horizontal_state(position)
        if h in situation:
            relative_loc = h.index('x')
            moves.append((x_pos, y_pos + relative_loc))

        # Check ↓
        v = gameboard.check_vertical_state(position)
        if v in situation:
            relative_loc = v.index('x')
            moves.append((x_pos + relative_loc, y_pos))

        # Check ↘
        d1 = gameboard.check_diag_1_state(position)
        if d1 in situation:
            relative_loc = d1.index('x')
            moves.append((x_pos + relative_loc, y_pos + relative_loc))
        
        
        # Check ↙
        d2 = gameboard.check_diag_2_state(position)
        if d2 in situation:
            relative_loc = d2.index('x')
            moves.append((x_pos + relative_loc, y_pos - relative_loc))

        return moves

    def _alter_check_opponent_4(self, position, gameboard):
        """ Check if opponent has got unbroken chain of 4 stones.

        Args:
            position(tuple): coordinates of current position to check
            gameboard(Board): game board
        Returns:
            moves(list): list of tuples, recording positions to move
        """
        if self.color == 'red':
            opponent_color = 'blue'
        else:
            opponent_color = 'red'
            
        x_pos = position[0]
        y_pos = position[1]
        moves = []        
        situation = [['x'] + [opponent_color]*4,
                     [opponent_color]*4 + ['x'],
                     [opponent_color] + ['x'] + [opponent_color]*3,
                     [opponent_color]*2 + ['x'] + [opponent_color]*2,
                     [opponent_color]*3 + ['x'] + [opponent_color]] # What we should find here

        # Check →
        h = gameboard.check_horizontal_state(position)
        if h in situation:
            relative_loc = h.index('x')
            moves.append((x_pos, y_pos + relative_loc))

        # Check ↓
        v = gameboard.check_vertical_state(position)
        if v in situation:
            relative_loc = v.index('x')
            moves.append((x_pos + relative_loc, y_pos))

        # Check ↘
        d1 = gameboard.check_diag_1_state(position)
        if d1 in situation:
            relative_loc = d1.index('x')
            moves.append((x_pos + relative_loc, y_pos + relative_loc))
        
        
        # Check ↙
        d2 = gameboard.check_diag_2_state(position)
        if d2 in situation:
            relative_loc = d2.index('x')
            moves.append((x_pos + relative_loc, y_pos - relative_loc))

        return moves

    def check_opponent_3(self, position, gameboard):
        """ Check if opponent has got unbroken chain of 3 stones and
        have spaces on both sides.

        Args:
            position(tuple): coordinates of current position to check
            gameboard(Board): game board
        Returns:
            moves(list): list of tuples, recording positions to move
        """
        if self.color == 'red':
            opponent_color = 'blue'
        else:
            opponent_color = 'red'
            
        x_pos = position[0]
        y_pos = position[1]
        moves = []        
        situation = ['x'] + [opponent_color]*3 + ['x'] # What we should find here

        # Check →
        h = gameboard.check_horizontal_state(position)
        if h == situation:
            moves.append((x_pos, y_pos))

        # Check ↓
        v = gameboard.check_vertical_state(position)
        if v == situation:
            relative_loc = 4
            moves.append((x_pos + relative_loc, y_pos))

        # Check ↘
        d1 = gameboard.check_diag_1_state(position)
        if d1 == situation:
            moves.append((x_pos, y_pos))
        
        
        # Check ↙
        d2 = gameboard.check_diag_2_state(position)
        if d2 == situation:
            relative_loc = 4
            moves.append((x_pos + relative_loc, y_pos - relative_loc))

        return moves

    def check_winning_blocks(self, position, gameboard):
        """ Check winning blocks on the agent side.

        Args:
            position(tuple): coordinates of current position to check
            gameboard(Board): game board
        Returns:
            moves(list): list of tuples, [(x_pos, y_pos, count), ...]
        """
        if self.color == 'red':
            opponent_color = 'blue'
        else:
            opponent_color = 'red'
            
        x_pos = position[0]
        y_pos = position[1]
        moves = []

        # Check →
        h = gameboard.check_horizontal_state(position)
        if h.count(self.color) + h.count('x') == 5:
            if h.count(self.color) <= 0:
                pass
            else:
                for i in range(4):
                    if h[i] != h[i + 1]:
                        if h[i] == 'x':
                            relative_loc = i
                        else:
                            relative_loc = i + 1
                        moves.append((x_pos, y_pos + relative_loc, h.count(self.color)))

        # Check ↓
        v = gameboard.check_vertical_state(position)
        if v.count(self.color) + v.count('x') == 5:
            if v.count(self.color) <= 0:
                pass
            else:
                for i in range(4):
                    if v[i] != v[i + 1]:
                        if v[i] == 'x':
                            relative_loc = i
                        else:
                            relative_loc = i + 1
                        moves.append((x_pos + relative_loc, y_pos, v.count(self.color)))
        
        # Check ↘
        d1 = gameboard.check_diag_1_state(position)
        if d1.count(self.color) + d1.count('x') == 5:
            if d1.count(self.color) <= 0:
                pass
            else:
                for i in range(4):
                    if d1[i] != d1[i + 1]:
                        if d1[i] == 'x':
                            relative_loc = i
                        else:
                            relative_loc = i + 1
                        moves.append((x_pos + relative_loc, y_pos + relative_loc, d1.count(self.color)))
        
        # Check ↙
        d2 = gameboard.check_diag_2_state(position)
        if d2.count(self.color) + d2.count('x') == 5:
            if d2.count(self.color) <= 0:
                pass
            else:
                for i in range(4):
                    if d2[i] != d2[i + 1]:
                        if d2[i] == 'x':
                            relative_loc = i
                        else:
                            relative_loc = i + 1
                        moves.append((x_pos + relative_loc, y_pos - relative_loc, d2.count(self.color)))

        return moves

    def find_move(self, gameboard):
        """
        Find next move, following the four steps.

        Args:
            gameboard(Board): game board
        Returns:
            best_move(tuple): coordinate to place a stone
        """
        best_move = None
        moves = []
        # step 1
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                position = (x, y)
                temp = self.check_going_to_win(position, gameboard)
                if len(temp) != 0:
                    moves += temp

        if len(moves) > 0:
            best_move = self.choose_move(moves)
            return best_move
        
        # step 2
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                position = (x, y)
                temp = self.check_opponent_4(position, gameboard)
                if len(temp) != 0:
                    moves += temp
        
        if len(moves) > 0:
            best_move = self.choose_move(moves)
            return best_move

        # step 3
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                position = (x, y)
                temp = self.check_opponent_3(position, gameboard)
                if len(temp) != 0:
                    moves += temp
        
        if len(moves) > 0:
            best_move = self.choose_move(moves)
            return best_move
        
        # step 4, iterate over all positions, variable 'moves'
        #         is defined differently here!!!
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                position = (x, y)
                temp = self.check_winning_blocks(position, gameboard)
                if len(temp) != 0:
                    moves += temp

        if len(moves) > 0:
            moves = list(set(moves))
            moves.sort(key=lambda x: x[2], reverse=True)
            max_count = moves[0][2]
            new_moves = []

            for t in moves:
                if t[2] < max_count:
                    break
                else:
                    new_moves.append((t[0], t[1]))

            moves = new_moves.copy()

        if len(moves) > 0:
            best_move = self.choose_move(moves)
            return best_move
        
        # step 5
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                position = (x, y)
                if gameboard.board[x][y] == '.':
                    moves.append(position)

        if len(moves) > 0:
            best_move = self.choose_move(moves)
            return best_move
        else:
            return None
            
