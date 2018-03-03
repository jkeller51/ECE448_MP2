from tkinter import *
from board import Board

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
        
       


       
      
        #buttons representing the boxes of the game
        for i in range(self.gameBoard.height): #for each row
            for j in range(self.gameBoard.width): #for each column
                test = "{},{}".format(i, j)
                widgetName = "{row}+{column}".format(row = i, column = j) #used as unique identifier for each button
                newButton =  Button(self.master, text = test, name = widgetName)
                newButton.bind('<Button-1>', printInfo)
                newButton.grid(row = i + 1, column = j + 1 )
                
                print(type(newButton))
                
               


   

        
        
def printInfo(event):
        print("Hello, it works!")
       
         

root = Tk() #root window

root.geometry("600x600")

app = Window(root)

root.mainloop() #initialize and generate window



