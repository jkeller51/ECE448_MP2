#!usr/bin/env python3
# -*- coding:utf-8 -*-


from board import Board
import numpy as np


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
        pass

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

    def num_empty_spaces(self, gameboard):
        """Return the number of empty spaces on the board"""
        count = 0
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                if gameboard.board[x][y] == '.':
                   count = count + 1
        return count
        

        
    def  has_valid_move(self, gameboard):
        """
         Determine if there is at least one valid move that can be played.
         If so, return True, else False. Similar to all_valid_moves()
        """
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                if gameboard.board[x][y] == '.':
                    return True 
        return False

    def move_valid(self, move, gameboard):
        """
          Determine if a particular move is valid.

          Returns:
          True if valid, False otherwise
        """
        x = move[0]
        y = move[1]
        if gameboard.board[x][y] == '.':
            return True
        else:
            return False

        
    

    def win_lose_tie(self, gameboard):
        """ Check the agent wins or loses or ties

        Args:
            gameboard(Board): game board
        Returns:
            result(str): 'win' or 'lose' or 'tie'
        """
        result = 'UNFINISHED'

        # Define end state
        _win_ = [self.color] * 5
        _lose_ = [self.opponent_color] * 5
        
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                position = (x, y)
                # check horizontal state
                h = gameboard.check_horizontal_state(position)
                if h == _win_:
                    result = 'win'
                    break
                elif h == _lose_:
                    result = 'lose'
                    break

                # check vertical state
                v = gameboard.check_vertical_state(position)
                if v == _win_:
                    result = 'win'
                    break
                elif v == _lose_:
                    result = 'lose'
                    break

                # check 1st diagonal state
                d1 = gameboard.check_diag_1_state(position)
                if d1 == _win_:
                    result = 'win'
                    break
                elif d1 == _lose_:
                    result = 'lose'
                    break

                # check 2nd diagonal state
                d2 = gameboard.check_diag_2_state(position)
                if d2 == _win_:
                    result = 'win'
                    break
                elif d2 == _lose_:
                    result = 'lose'
                    break

        moves = self._all_valid_moves(gameboard)
        if (result == 'UNFINISHED') and (len(moves) == 0):
            result = 'tie'

        return result
    
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

    def random_move(self, gameboard):
        """
        Randomly choose a move

        Args:
            gameboard(Board): game board
        Returns:
            (None)
        """
        move = self._all_valid_moves(gameboard)
        position_idx = np.random.choice(len(move), 1)[0]
        position = move[position_idx]
        self.make_move(position, gameboard)

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
        pass


    def evaluation(self, gameboard):
        """
        Estimate a utility score of one game state

        Args:
            gameboard(Board): game board
        Returns:
            score(int): score
        """
        score = 0
        five_stones = [[self.color] * 5]
        five_opponent_stones = [[self.opponent_color] * 5]
        four_stones = [[self.color] * 4 + ['x'],
                       [self.color] * 3 + ['x'] + [self.color],
                       [self.color] * 2 + ['x'] + [self.color] * 2,
                       [self.color] + ['x'] + [self.color] * 3,
                       ['x'] + [self.color] * 4]
        four_opponent_stones = [[self.opponent_color] * 4 + ['x'],
                                [self.opponent_color] * 3 + ['x'] + [self.opponent_color],
                                [self.opponent_color] * 2 + ['x'] + [self.opponent_color] * 2,
                                [self.opponent_color] + ['x'] + [self.opponent_color] * 3,
                                ['x'] + [self.opponent_color] * 4]
        three_open = [['x'] + [self.color] * 3 + ['x']]
        three_opponent_open = [['x'] + [self.opponent_color] * 3 + ['x']]

        # Find patterns
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                position = (x, y)
                h = gameboard.check_horizontal_state(position)
                v = gameboard.check_vertical_state(position)
                d1 = gameboard.check_diag_1_state(position)
                d2 = gameboard.check_diag_2_state(position)

                for pattern in [h, v, d1, d2]:
                    if pattern == []:
                        continue
                    

                    if pattern in five_stones:
                        score += 1000
                    elif pattern in five_opponent_stones:
                        score -= 1000
                    elif pattern in four_stones:
                        score += 100
                    elif pattern in four_opponent_stones:
                        score -= 100
                    elif pattern in three_open:
                        score += 50
                    elif pattern in three_opponent_open:
                        score -= 50
                    elif (pattern.count('x') + pattern.count(self.color) == 5):
                        score += 1
                    
        return score
