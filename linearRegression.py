from board import Board
from agent import Agent

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

    

    def fivePossible(self, color_to_check, array_to_search, start_index):
        """Return 1 (True) if it's possible to get five of the same color in that array. 0 otherwise"""

        for val in range(start_index, start_index + 5): #looking for 5 matching
            #we've encountered an opponent's mark in one of the 5 slots.  
            if array_to_search[val] != color_to_check and array_to_search[val] !=  "x": #where x represents a space
                  return 0
        return 1

    def count_winning_windows(self, gameboard, color_of_interest):
        count = 0
        for row in range(gameboard.height):
            #count number of winning windows in that row. check [0-5], [1-6], [2-7]
            count = self.fivePossible(color_of_interest, row, 0) + self.fivePossible(color_of_interest, row, 1) + self.fivePossible(color_of_interest, row, 2)

        for column in range(gameboard.width):
            #count number of winning windows in that column. check  check [0-5], [1-6], [2-7]
            count = count + self.fivePossible(color_of_interest, column, 0) + self.fivePossible(color_of_interest, column, 1) + self.fivePossible(color_of_interest, column, 2)

      
        
    def featurize(self, gameboard):
        """Given a gameboard, get some relevant features of that position

          Returns:
          features(list): [1st player has 4 in row, 1st player has 4 in column, 1st player has 4 in diagonal, # winning windows 1st player,
          #winning windows 2nd player] e.g. [1,1, 0, 4, 7]
        """
        features  = []
        #check if we have a combination of four either vertically, horizontally or  diagonally
        #1 if we do, 0 if we don't
        firstPlayerFourInRow = [self.color] * 4
        for x in range(gameboard.height):
                for y in range(gameboard.width):

                    position = (x, y)
                    
                    #handle features for horizontal state
                    h = gameboard.check_horizontal_state(position)
                    if h[0:4] == firstPlayerFourInRow or h[1:5] == firstPlayerFourInRow:
                        features.append(1)
                    else:
                        features.append(0)


                    #handle features for vertical state
                    
                    v = gameboard.check_vertical_state(position)
                    if v[0:4] == firstPlayerFourInRow or v[1:5] == firstPlayerFourInRow:
                        features.append(1)
                    else:
                        features.append(0)

                    #handle features for diagonal state

                    d1 = gameboard.check_diag_1_state(position)
                    d1 = gameboard.check_vertical_state(position)
                    if d1[0:4] == firstPlayerFourInRow or d1[1:5] == firstPlayerFourInRow:
                        features.append(1)
                    else:
                        features.append(0)
        player_winning_windows = count_winning_windows(gameboard, self.color)
        opponent_winning_windows = count_winning_windows(gameboard, self.opponent_color)
        features.append(player_winning_windows)
        features.append(opponent_winning_windows)
        return features


    def generate_games(self, num = 100):
        """Generate games that will be used for training. """



