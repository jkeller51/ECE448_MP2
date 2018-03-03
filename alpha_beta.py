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
        self.track_sheet = [] #an array of tuples, where each tuple stores (move, movescore)
    pass



       
    def find_move_helper(self, gameboard, depth, limit, alpha, beta):
         
        
        if depth == limit or self.has_valid_move(gameboard) == False: #if we've reached our limit, or the gameboard is in a terminal state, then return a score.

            self.expanded_nodes += 1 #***concerned about increasing count when we're at a terminal state.  
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
                     
                     move_value = self.find_move_helper(temp_board, depth + 1, limit, alpha, beta)
                     if move_value > best_value:
                         best_value = move_value

                     alpha = max(alpha, best_value)
                     #select alpha,
                     #pick alpha as best move.

                     

                     #Pruning happens here.
                     if (beta <= alpha):
                         break #stop expanding down path if we reach this position which is unattainable given a rational player. 


                     if (depth == 0):
                         #we're at the topmost level.
                         #store the scores of all the child moves. 
                         move_data = [pos, move_value]
                         self.track_sheet.append(move_data)
                         
                
                 return best_value
                         
                    
                
            else: #if depth % 2 == 1, we're at a min level

                 lowest_value = float("inf") #smallest number MIN player knows how to force. 
                 moves = self._all_valid_moves(gameboard)
                 
                 for pos in moves:
                    temp_board = gameboard.copy()
                    temp_agent = Agent(self.opponent_color)
                    temp_agent.make_move(pos, temp_board)
              
                    
                    move_value =  self.find_move_helper(temp_board, depth + 1, limit, alpha, beta)
            
                    if move_value < lowest_value: #looking for the minimum score here, not max 
                         lowest_value = move_value
                         
                    beta = min(beta, lowest_value)

                   #Pruning also happens here
                    if (beta <= alpha):
                       break
                    
                  
                 return lowest_value


    def find_move(self, gameboard):
        #recursive method
        self.find_move_helper(gameboard, 0, 3, float("-inf"), float("inf"))
        
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








