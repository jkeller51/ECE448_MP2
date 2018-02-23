#!usr/bin/env python3
# -*- coding:utf-8 -*-


from board import Board
from agent import Agent


class Minimax(Agent):
    """ Inherit from class 'Agent', used to represent an agent."""
    def __init__(self, color):
        super().__init__(color)
        self.expanded_nodes = 0
        self.type = 'minimax'

   

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

    def find_move(self, gameboard):
        """
        Find next move, following the four steps.

        Args:
            gameboard(Board): game board
        Returns:
            best_move(tuple): coordinate to place a stone
        """
        moves = self._all_valid_moves(gameboard)

        # max-agent, depth=1
        best_move = None
        best_score = float('-inf')
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
                temp_moves_2 = self._all_valid_moves(temp_board_2)

                # max-agent, depth=3
                max_move = None
                max_score = float('-inf')
                for pos_3 in temp_moves_2:
                    temp_board_3 = temp_board_2.copy()
                    temp_agent_3 = Agent(self.color)
                    temp_agent_3.make_move(pos_3, temp_board_3)

                    self.expanded_nodes += 1
                    temp_score_3 = self.evaluation(temp_board_3)
                    if temp_score_3 > max_score:
                        max_move = pos_3
                        max_score = temp_score_3

                if max_score < min_score:
                    min_move = pos_2
                    min_score = max_score

            if min_score > best_score:
                best_move = pos
                best_score = min_score
        
        return best_move
