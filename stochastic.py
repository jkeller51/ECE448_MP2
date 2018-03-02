#!usr/bin/env python3
# -*- coding:utf-8 -*-


from board import Board
from agent import Agent
from reflex import Reflex
import numpy as np


class Stochastic(Agent):
    """ Inherit from class 'Agent', used to represent an agent."""    
    def __init__(self, color):
        super().__init__(color)
        self.expanded_nodes = 0
        self.probability = 0
        self.type = 'stochastic'

    def _policy(self, gameboard):
        """ Find next move in simulation

        Args:
            gameboard(Board): game board
        Returns:
            best_move(tuple): coordinate
        """
        valid_moves = self._all_valid_moves(gameboard)
        _reflex_ = Reflex(self.color)
        best_move = None
        moves = []
        
        # step 1, check going to win
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                position = (x, y)
                temp = _reflex_.check_going_to_win(position, gameboard)
                if len(temp) != 0:
                    moves += temp

        if len(moves) > 0:
            idx = np.random.choice(len(moves), 1)[0]
            best_move = moves[idx]
            return best_move
        
        # step 2, check opponent 4
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                position = (x, y)
                temp = _reflex_._alter_check_opponent_4(position, gameboard)
                if len(temp) != 0:
                    moves += temp
        
        if len(moves) > 0:
            idx = np.random.choice(len(moves), 1)[0]
            best_move = moves[idx]
            return best_move

        # step 3, check opponent 3
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                position = (x, y)
                temp = _reflex_.check_opponent_3(position, gameboard)
                if len(temp) != 0:
                    moves += temp
        
        if len(moves) > 0:
            idx = np.random.choice(len(moves), 1)[0]
            best_move = moves[idx]
            return best_move

        # step 4, winning blocks
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                position = (x, y)
                temp = _reflex_.check_winning_blocks(position, gameboard)
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
            idx = np.random.choice(len(moves), 1)[0]
            best_move = moves[idx]
            return best_move

        # step 5, random pick one
        idx = np.random.choice(len(valid_moves), 1)[0]
        return valid_moves[idx]

    def count_winning_blocks(self, gameboard):
        """ Count winning blocks for both sides

        Args:
            gameboard(Board): game board
        Returns:
            count(dict): key(str):color; value(int):number
        """
        count = {'red':0.1, 'blue':0.1}
        for x in range(gameboard.height):
            for y in range(gameboard.width):
                position = (x, y)
                h = gameboard.check_horizontal_state(position)
                v = gameboard.check_vertical_state(position)
                d1 = gameboard.check_diag_1_state(position)
                d2 = gameboard.check_diag_2_state(position)
                for state in [h, v, d1, d2]:
                    if ((state.count('red') + state.count('x') == 5)
                        and (state.count('red') > 0)):
                        count['red'] += np.power(3, (state.count('red') - 1))
                    elif ((state.count('blue') + state.count('x') == 5)
                        and (state.count('blue') > 0)):
                        count['blue'] += np.power(3, (state.count('blue') - 1))
        return count

    def simulation(self, gameboard, N):
        """
        Generate N random games using policy, and return average value.

        Args:
            gameboard(Board): game board
            N(int): # of games
        Returns:
            avg_score: average evaluation score
        """
        MAX_DEPTH = 6
        score = 0

        # Simulation N times
        for i in range(N):
            depth = 0
            gameboard_cpy = gameboard.copy()
            
            # Create two temp angents for random moves
            _SELF_ = Stochastic(self.color)
            _OPPONENT_ = Stochastic(self.opponent_color)

            _SELF_ACTION_ = 1
            _OPPONENT_ACTION_ = 0

            while ((_SELF_.win_lose_tie(gameboard_cpy) == 'UNFINISHED')
                   and (depth < MAX_DEPTH)):
                if _SELF_ACTION_ == 1:
                    temp = _SELF_._policy(gameboard_cpy)
                    _SELF_.make_move(temp, gameboard_cpy)

                if _OPPONENT_ACTION_ == 1:
                    temp = _OPPONENT_._policy(gameboard_cpy)
                    _OPPONENT_.make_move(temp, gameboard_cpy)

                _SELF_ACTION_, _OPPONENT_ACTION_ = _OPPONENT_ACTION_, _SELF_ACTION_

                depth += 1

            result = _SELF_.win_lose_tie(gameboard_cpy)
            if result == 'win':
                score += 1.0
            elif result == 'lose':
                score += 0.0
            elif result == 'tie':
                score += 0.5
            elif depth >= MAX_DEPTH:
                count = _SELF_.count_winning_blocks(gameboard_cpy)
                score += count[_SELF_.color] / (count[_SELF_.color] + count[_SELF_.opponent_color])
        
        avg_score = score / N
        return avg_score

    def find_move(self, gameboard, N=20):
        """
        Find next move

        Args:
            gameboard(Board): game board
            N(int): number of simulations for each leaf
        Returns:
            best_move(tuple): coordinate to place a stone
        """
        # find all valid moves
        moves = self._all_valid_moves(gameboard)

        # max-agent, depth=1
        best_move = None
        best_score = float('-inf')
        beta = float('-inf')
        for pos in moves:
            temp_board = gameboard.copy()
            temp_agent = Agent(self.color)
            temp_agent.make_move(pos, temp_board)
            temp_moves = self._all_valid_moves(temp_board)

            # min-agent, depth=2
            min_move = None
            min_score = float('inf')
            for pos_2 in temp_moves:
                temp_board_2 = temp_board.copy()
                temp_agent_2 = Agent(self.opponent_color)
                temp_agent_2.make_move(pos_2, temp_board_2)
                
                score = self.simulation(temp_board_2, N)
                self.expanded_nodes += 1

                if score < min_score:
                    min_move = pos_2
                    min_score = score
                if score < beta:
                    break

            if min_score > best_score:
                best_move = pos
                best_score = min_score
            if min_score > beta:
                beta = min_score

        self.probability = best_score
        return best_move
