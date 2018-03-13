from board import Board
from agent import Agent
import random
import math
from alpha_beta import AlphaBeta

class LinearAgent(Agent):
    """ 
    Meta-class of all agents.
    """


    def __init__(self, color):
        super().__init__(color)
        self.expanded_nodes = 0
        self.type = 'linear'
        
    
    
    def fivePossible(self, color_to_check, array_to_search, start_index):
        """Return 1 (True) if it's possible to get five of the same color in that array. 0 otherwise"""

        for val in array_to_search[start_index: start_index + 5]: #looking for possible 5 slots 
            # if we've encountered an opponent's mark in one of the 5 slots.  
            if (self.cur_player_moved_here(color_to_check, val) == False) and val !=  ".": #where . represents a space
                  return 0
        return 1


    def cur_player_moved_here(self, color_of_interest, value_in_square):
        #if the color to check is red and the character used in the square is a small character, return True
        #if the color to check is blue and the character used  in the square is a big character, return True
        #else return False
        if (color_of_interest == "red") and (97 <= ord(value_in_square)  <= 122):
            return True
        if (color_of_interest == "blue") and (65 <= ord(value_in_square)  <= 90):
            return True
        return False


    

    def count_winning_windows(self, gameboard, color_of_interest):
        count = 0
        for row in range(gameboard.height):
            #count number of winning windows in that row. check [0-5], [1-6], [2-7]
           
            rowData = gameboard.board[row]
           
            count = self.fivePossible(color_of_interest, rowData, 0) + self.fivePossible(color_of_interest, rowData, 1) + self.fivePossible(color_of_interest, rowData, 2)

        for column in range(gameboard.width):
            
     
            columnData = []
            for row in range(gameboard.height):
                columnData.append(gameboard.board[row][column]) #get the elements for the column
                
            count = count + self.fivePossible(color_of_interest, columnData, 0) + self.fivePossible(color_of_interest, columnData, 1) + self.fivePossible(color_of_interest, columnData, 2)

        return count


        
    def featurize(self, gameboard):
        """Given a gameboard, get some relevant features of that position

          Returns:
          features(list): [# winning windows of player, #winning windows of opponent, # empty spaces, interaction term] e.g. [4, 7, 8, 4*8]
        """
        features  = []
        
        player_winning_windows = self.count_winning_windows(gameboard, self.color)
        opponent_winning_windows = self.count_winning_windows(gameboard, self.opponent_color)
        features.append(player_winning_windows)
        features.append(opponent_winning_windows)

        num_empty_spaces = self.num_empty_spaces(gameboard)
        interaction_term = num_empty_spaces * player_winning_windows #want to see how # of empty squares and # of winning windows interact. 

        features.append(num_empty_spaces)
        features.append(interaction_term)
        
        return features

    def true_move_value(self, gameboard):
        """This method returns the true value associated with a particular state of the board.
           In reality, this value is  an estimate of the game state; it uses alpha beta with an evaluation function
        """
        smartAgent = AlphaBeta(self.color)
        return smartAgent.find_move_value(gameboard, depth = 2)
        

    def compile_features_and_data(self, numGames = 100):
        """Combine all data used for training model"""
        allData = []
        games = self.generate_games(numGames)
        for game in games:
            #each game is an array consisting of a game state and a "true" score associated with that game state
            game[0].print_board()
            print("--------")
            newData = self.featurize(game[0])
            newData = newData + [game[1]] #an array containing values for features, and the true value of position appended at the end.
            allData.append(newData)
        return allData
        
    def generate_games(self, numGames = 100):
        """Generate games that will be used for training. """
        games = []
        for i in range(numGames):
            curGame = self.generate_one_game()
            gameData = [curGame, self.true_move_value(curGame)] #store the game and the true score of the game. 
            games.append(gameData)

        return games
    

    def generate_one_game(self):
        """Generate one game of Gomoku. The game may or may not be completed"""
        newBoard = Board()
        maxMoves = newBoard.height * newBoard.width
        numMovesToPlay = random.randint(9, maxMoves) #the number of moves we play in each game is random, but at least 9; 9 moves is minimum needed before a win can occur,
                                                     #but 9 does not guarantee that a win has in fact occured.
        numMovesToPlay =  math.ceil(numMovesToPlay/2) #a move here consists of both red and blue moving, so we need to divide by 2. ceil gives us whole number. 
        clonedAgent = Agent(self.color) #clone myself. Used to prevent running out of characters. New character set generated for new game.
        opponent = Agent(self.opponent_color)
  
        
        moveNum = 0
        while (moveNum < numMovesToPlay):
            #simulate player making move
            possibleMoves = self._all_valid_moves(newBoard)
        
            optionToChoose = random.choice(possibleMoves) #select a move to make
            clonedAgent.make_move(optionToChoose, newBoard)

        
            #simulate opponent making move
            possibleMoves = self._all_valid_moves(newBoard)
           
            if len(possibleMoves) == 0:
          
                return newBoard     #if there are no more possible moves, just return the board


            #if there are possble moves, opponent should pick one of those options. 
            optionToChoose = random.choice(possibleMoves)
           
           
            opponent.make_move(optionToChoose, newBoard)
          



            #if game is won, stop and return the board. No point in going on.            
            if self.win_lose_tie(newBoard) != "UNFINISHED": #this means game is done
                return newBoard
            
            moveNum = moveNum + 1

            
        
        return newBoard
        
        
        




learningAgent = LinearAgent("red")
allData = learningAgent.compile_features_and_data(50)
for row in allData:
    print(row)
    #The first four elements in a row are the features (the independent variables), the last element is the value of the position  (the dependent variable).
    #Need to perform OLS and show results. 

