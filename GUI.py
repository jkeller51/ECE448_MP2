#!usr/bin/env python3
# -*- coding:utf-8 -*


#Gomoku GUI program
#Can extend by adding menu item to allow you to choose difficulty level



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
    """
       Human vs Computer driver. This class manages a single game. 
    """
    def __init__(self, gameboard, buttons, buttonColor,  label):
        self.board = gameboard

        #values set to None will be replaced when user chooses color (e.g. red or blue).
        
        self.gameStarted = False #keep track of if game has begun. 
        
        self.playerColor = None #should be set to red or blue
        
        self.playerTurn = None #should be set to true or false

        self.computerAgent = None #should be set to alphabeta or reflex or some other agent other than human. 
            
        self.humanAgent = None

        

        self.gameSquares = buttons
        self.gameLabel = label #label to give updates to the player. 
        self.gameDone = False
        
       

        
            
        self.computerAgent = None
        self.computerPreviousSquare  = None #the last square the computer played on. 
        self.originalBackgroundColor = buttonColor #refers to button colors




    def playRound(self, event):
        
       if self.gameStarted == False:
           return; 

       #we check to see if game is done before either player is allowed to move
       if (self.gameDone == False):
            self.playerMove(event)
            self.gameDone = self.isGameDone() #check if game is finished
       

       if (self.gameDone == False):
           
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

        
    def getSymbol(self):
        """Return either X or O to be printed."""
        if self.playerTurn == True and self.playerColor == "red":
            return "X"
        elif self.playerTurn == False and self.playerColor == "red":
            return "O"
        elif self.playerTurn == True and self.playerColor == "blue":
            return "O"
        elif self.playerTurn == False and self.playerColor == "blue":
            return "X"

        return None
    

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
                buttonClicked.config(text= self.getSymbol()) #change the external representation (i.e. text displayed on the button)
                self.playerTurn = False #now it's the computer's turn to play.
        
           
                

        #after a player has moved, check to see if someone won or tied. Display message accordingly


    def computerMove(self):
        if self.playerTurn == False: #it's the computer's turn to play

            if (self.computerPreviousSquare != None):
                #if comp made a previous move which was highlighted, remove the highlight
                #comp is about to make a fresh move.
                self.computerPreviousSquare.config(background = self.originalBackgroundColor)
      
 
            self.gameLabel.config(text= "The computer is thinking...")
        
            compMove = self.computerAgent.find_move(self.board, depth = 2) #depth controls how far we should search
            print("The computer's move is {}, {}".format(compMove[0], compMove[1]))
            self.computerAgent.make_move(compMove, self.board)
            moveID = "{x}+{y}".format(x = compMove[0], y =  compMove[1])

            #For external representation, check for square computer wants and make move.
            
            for square in self.gameSquares: #a list of buttons, where each button represents a game cell
                if square.widgetID == moveID:
                    #this is the location the computer wants to play at.
                    
                    square.config(text = self.getSymbol(), background="green")
                   
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
        self.gameStatusLabel = Label(self.master, text="Play as...")
        labelfont = ('times', 20, 'bold')
        self.gameStatusLabel.config(font = labelfont)
        
        buttonList = [] #list to store buttons for game
        buttonColor = GomokuButton(self.master, textVal = "", wName = "").cget("bg") #need default color of buttons
        
        self.gameBoard = Board()
        self.manager = GameManager(self.gameBoard, buttonList, buttonColor,  self.gameStatusLabel) #this is the game manager
        

        self.gameStatusLabel.grid(row = 0, column = 0)
       

        self.humanPlayer = None
      
        self.var = IntVar() #variable to store human color

        self.RB1 = Radiobutton(self.master, text="Red", variable=self.var, value=1, command=self.setHumanColor)
        self.RB1.grid(row = 1)
        self.RB2 = Radiobutton(self.master, text="Blue", variable=self.var, value=2, command=self.setHumanColor)
        self.RB2.grid(row = 2)
        
        #buttons representing the boxes of the game
        for i in range(self.gameBoard.height): #for each row  
            for j in range(self.gameBoard.width): #for each column
                coordinates = "{},{}".format(i, j) #can display this on every button.
                widgetName = "{row}+{column}".format(row = i, column = j) #used as unique identifier for each button
                newButton =  GomokuButton(self.master, textVal = ".", wName = widgetName) 
                newButton.config(font = ('times', 20), height = 1, width = 3) #beautify the game squares. 
                buttonList.append(newButton)
                newButton.bind('<Button-1>', self.manager.playRound)
                newButton.grid(row = i + 2, column = j + 1 )

        
        

    def setHumanColor(self):
        """
          Determine user's color based on radio box selection. 
        """
        print("You selected {}".format(self.var.get()))
        compColor = ""
        
        if self.var.get() == 1:
            self.manager.playerColor = "red"
            compColor = "blue"
            self.manager.playerTurn = True
            self.gameStatusLabel.config(text = "Your turn to move")
            
            
        elif self.var.get() == 2:
            self.manager.playerColor = "blue"
            compColor = "red"
            self.manager.playerTurn = False

                                     
        self.manager.gameStarted = True
        self.RB1.grid_forget() #remove options. User already made choice. 
        self.RB2.grid_forget()

        #initialize players according to color
        self.manager.humanAgent = Human(self.manager.playerColor)
        self.manager.computerAgent = AlphaBeta(compColor)

        #After building GUI and seeing if player is red or blue, check who's turn it is to play. If it's computer, prompt its first move. 
        if self.manager.playerTurn == False and self.manager.gameStarted == True: 
            self.manager.computerMove() #in this case, the computer move first
        


        
            
           


          

        
        

         

root = Tk() #root window


#make the GUI take up full screen. 
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('%sx%s' % (width, height))

#root.geometry("600x600") #make GUI take up specific amount of space


app = Window(root)

root.mainloop() #initialize and generate window



