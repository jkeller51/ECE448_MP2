# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 12:51:13 2018

@author: jkell
"""

class Node():
    
    evaluation = None
    cost = None
    previous = None
    widgets = []
    
    def __init__(self, widgets, cost, evaluation, previous):
        """
        widgets : list of widgets
        cost  : cost to get to this point
        evaluation : cost plus heuristic to reach the goal
        previous : previous Node, for traceback
        widgets : 
        """
        self.widgets = widgets
        self.cost = cost
        self.previous = previous
        self.evaluation = evaluation
        

class Widget():
    """ Our widget object
        Contains variables and methods for components
    """
    
    components=[]
    componentStructure=[]
    done=False
    
    def __init__(self, componentString):
        """
        Use componentString to define how to build this widget
        """
        print(componentString)
        for i in range(0,len(componentString)):
            self.componentStructure.append(componentString[i])
            print("adding",componentString[i])
            
    def addComponent(self, component):
        """
        args
            component : a character for the component to add
            
        return value:
            True if component added correctly
            False otherwise
        """
        if (self.nextComponent() == component):
            self.components.append(component)
            if (self.components == self.componentStructure):
                self.done=True
            return True
        else:
            #print("--> Could not add component! Check that it is the correct component.")
            return False
        
    def nextComponent(self):
        """
        Returns the next component this widget needs
        """
        if self.done == False:
            return self.componentStructure[len(self.components)]
        else:
            return None