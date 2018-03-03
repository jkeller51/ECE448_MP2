from tkinter import *
from board import Board
from alpha_beta import AlphaBeta


class GomokuButton(Button):
    def __init__(self, master = None, textVal = "", wName = ""):
        Button.__init__(self, master, text =  textVal)
        self.widgetID = wName #unique identifier for each button. 


class GameManager():
    def __init__(self, gameboard):
        self.board = gameboard
        self.gameStarted = False #only allow buttons and other things to work if game has officially started. 
        self.playerTurn = False #it's the human player's turn to play.
        self.playerColor = ""



        #set the computer's color.
        computerColor = None
        if self.playerColor == "RED":
            computerColor = "BLUE"
        else:
            computerColor = "RED"
            
        self.ComputerAgent = AlphaBeta(computerColor)


    def playerMove(self, event):
        """
              Method to allow player to make a move. Will update the gameboard accordingly
        """
        print("Hello, it works!")
        buttonClicked = event.widget
        
        print(buttonClicked.widgetID)
        #change both internal and external state
        buttonClicked.config(text="X")
        
    


class Window(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        

    def init_window(self):
        self.master.title("Gomoku")


       
            
        #label to give game updates
        self.gameStatusWindow = Label(self.master, text="Play your first move").grid(row = 0, column = 0)

        self.gameBoard = Board()
        self.manager = GameManager(self.gameBoard) #this is the game manager
       


       
      
        #buttons representing the boxes of the game
        for i in range(self.gameBoard.height): #for each row
            for j in range(self.gameBoard.width): #for each column
                test = "{},{}".format(i, j)
                widgetName = "{row}+{column}".format(row = i, column = j) #used as unique identifier for each button
                newButton =  GomokuButton(self.master, textVal = test, wName = widgetName)
                newButton.bind('<Button-1>', self.manager.playerMove)
                newButton.grid(row = i + 1, column = j + 1 )
                
           
                
               


   

        
        

         

root = Tk() #root window

root.geometry("600x600")

app = Window(root)

root.mainloop() #initialize and generate window



