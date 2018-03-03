from tkinter import *
from board import Board
from alpha_beta import AlphaBeta
from human import Human

class GomokuButton(Button):
    """
      Almost identical to tkinter button, but this version allows us to store a unique ID for buttons in the program. 
    """
    def __init__(self, master = None, textVal = "", wName = ""):
        Button.__init__(self, master, text =  textVal)
        self.widgetID = wName #unique identifier for each button. 


class GameManager():
    def __init__(self, gameboard, buttons, buttonColor,  label):
        self.board = gameboard
        self.gameStarted = True #only allow buttons and other things to work if game has officially started. 
        self.playerTurn = True #it's the human player's turn to play.
        self.playerColor = "red"
        self.humanAgent = Human(self.playerColor)
        self.gameSquares = buttons
        self.gameLabel = label #label to give updates to the player. 
        self.gameDone = False
        
       

        #set the computer's color.
        computerColor = None
        if self.playerColor == "red":
            computerColor = "blue"
        else:
            computerColor = "red"
            
        self.computerAgent = AlphaBeta(computerColor)
        self.computerPreviousSquare  = None #the last square the computer played on. 
        self.originalBackgroundColor = buttonColor #refers to button colors



    def playRound(self, event):
       print(self.originalBackgroundColor)

       #we check to see if game is done before either player is allowed to move
       if (self.gameDone == False):
            self.playerMove(event)
            self.gameDone = self.isGameDone() #check if game is finished
       

       if (self.gameDone == False):
           
            if (self.computerPreviousSquare != None):
                #if comp made a previous move which was highlighted, remove the highlight
                #comp is about to make a fresh move.
                self.computerPreviousSquare.config(background = self.originalBackgroundColor)


            self.computerMove()
            self.gameDone = self.isGameDone()

     


        
    def isGameDone(self):
        """
            Check if game is finished. If so, display a message about the winner.
        """
        result = self.humanAgent.win_lose_tie(self.board)
        if (result == "UNFINISHED"):
            return False

        
        self.showResults(result)
        return True

    

    def showResults(self, result):
        """
           When the game is done, display the result on the screen.
           
        """
        
        message = ""
        if result == "win":
            message = "Congratulations! You won"
        elif result == "lose":
            message = "Sorry you lost"
        elif result == "tie":
            message = "You tied with the computer"

        self.gameLabel.config(text=message)
            
        

    def playerMove(self, event):
        """
              Method to allow player to make a move. Will update the gameboard accordingly
        """
        
        buttonClicked = event.widget

        
        
        if self.playerTurn == True:
            #change both internal and external state
            humanMove = self.processText(buttonClicked.widgetID)
            
            if self.humanAgent.move_valid(humanMove, self.board):
                #only make human move if it's valid

            
                self.humanAgent.make_move(humanMove, self.board) #change the internal representation
                buttonClicked.config(text= "X") #change the external representation (text displayed)
                self.playerTurn = False #now it's the computer's turn to play.
        
           
                

        #after a player has moved, check to see if someone won or tied. Display message accordingly


    def computerMove(self):
        if self.playerTurn == False: #it's the computer's turn to play

            
            self.gameLabel.config(text= "The computer is thinking...")
        
            compMove = self.computerAgent.find_move(self.board, depth = 2)
            self.computerAgent.make_move(compMove, self.board)
            moveID = "{x}+{y}".format(x = compMove[0], y =  compMove[1])

            #For external representation, check for square computer wants and make move.
            
            for square in self.gameSquares: #a list of buttons, where each button represents a game cell
                if square.widgetID == moveID:
                    #this is the location the computer wants to play at.
                    square.config(text = "O", background="green")

                    self.computerPreviousSquare = square
                    self.playerTurn = True
                    self.gameLabel.config(text = "Your turn to move")
            

        


                
            
       # buttonClicked.config(text="X") #change the text displayed

    
    def processText(self, buttonID):
        """
              Converts button ID, such as 1+3 into a move (i.e. a position on the game board).          
        """
        values = buttonID.split("+")
        rowNum = int(values[0])
        columnNum = int(values[1])
        return (rowNum, columnNum)
        
    


class Window(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        

    def init_window(self):
        self.master.title("Gomoku")


       
            
        #label to give game updates
        self.gameStatusLabel = Label(self.master, text="Play your first move")

        buttonList = [] #list to store buttons for game
        buttonColor = GomokuButton(self.master, textVal = "", wName = "").cget("bg") #need default color of buttons
        
        self.gameBoard = Board()
        self.manager = GameManager(self.gameBoard, buttonList, buttonColor,  self.gameStatusLabel) #this is the game manager
        

        self.gameStatusLabel.grid(row = 0, column = 0)
       

      
        
        
        #buttons representing the boxes of the game
        for i in range(self.gameBoard.height): #for each row  
            for j in range(self.gameBoard.width): #for each column
                test = "{},{}".format(i, j)
                widgetName = "{row}+{column}".format(row = i, column = j) #used as unique identifier for each button
                newButton =  GomokuButton(self.master, textVal = test, wName = widgetName)
                buttonList.append(newButton)
                newButton.bind('<Button-1>', self.manager.playRound)
                newButton.grid(row = i + 1, column = j + 1 )

        
                
               


   

        
        

         

root = Tk() #root window

root.geometry("600x600")

app = Window(root)

root.mainloop() #initialize and generate window



