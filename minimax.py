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
        self.track_sheet = [] #an array of tuples, where each tuple stores (move, move_score)



    
    def find_move_helper(self, gameboard, depth, limit):
        """
           Find best score associated with best move by recursively building game tree

           Args:
           gameboard(Board): game board
           depth(int): the current depth at which we're searching.
           limit(int): a constant which represents maximum depth we search to.

           Returns:
           an evaluation score proprogated up the tree. 
           
        """
        
        if depth == limit or self.has_valid_move(gameboard) == False: 

            self.expanded_nodes += 1  
            return self.evaluation(gameboard)

        
        else:
            #we still want to keep on expanding the tree
            
            if (depth % 2 == 0): #we're at a max level

                 best_value = float("-inf")
                 moves = self._all_valid_moves(gameboard)
                 
                 
                 for pos in moves:
                     temp_board = gameboard.copy()
                     temp_agent = Agent(self.color)
                     temp_agent.make_move(pos, temp_board)

                     
                     move_value = self.find_move_helper(temp_board, depth + 1, limit)


                     if (depth == 0):
                         #we're at the topmost level.
                         #store the scores of all the child moves. 
                         move_data = [pos, move_value]
                         self.track_sheet.append(move_data)
                         


                     if move_value > best_value:
                         best_value = move_value
                        

                    

                 return best_value
                         
                    
                
            else: #if depth % 2 == 1, we're at a min level

                 lowest_value = float("inf")
                 moves = self._all_valid_moves(gameboard)
                 
                 for pos in moves:
                    temp_board = gameboard.copy()
                    temp_agent = Agent(self.opponent_color)
                    temp_agent.make_move(pos, temp_board)
                    
                    move_value =  self.find_move_helper(temp_board, depth + 1, limit)
                    if move_value < lowest_value: #looking for the minimum score here, not max 
                         lowest_value = move_value
                        
                    
                 return lowest_value


    def find_move(self, gameboard):
        """
           Find the best move given the current position.

           Args:
           gameboard(Board): game board

           Returns:
           best_move(tuple): coordinates to place a stone 
        """
        self.find_move_helper(gameboard, 0, 3)


        #we've generated tree and scored moves. Now find the best move.
        best_move = None
        best_score = float("-inf")
        
        for move_data  in self.track_sheet:
            move = move_data[0]
            move_value = move_data[1]
            if move_value > best_score:
                best_score = move_value
                best_move = move

             
        print("At  this time, we considered {} moves".format(len(self.track_sheet)))
        self.track_sheet = [] #reset the track sheet.
        
        return best_move
