# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 12:51:13 2018

@author: jkell
"""

class Node():
    
    evaluation = None
    cost = None
    previous = None
    value = None
    
    def __init__(self, value, cost, evaluation, previous):
        """
        value : factory letter
        cost  : cost to get to this point
        evaluation : cost plus heuristic to reach the goal
        previous : previous Node, for traceback
        """
        self.value = value
        self.cost = cost
        self.previous = previous
        self.value = value
        

class Widget():
    """ Our widget object
        Contains variables and methods for components
    """
    
    components=[]
    componentStructure=[]
    
    def __init__(self, componentString):
        """
        Use componentString to define how to build this widget
        """
        
        for i in range(0,len(componentString)):
            self.componentStructure.append(componentString[i])
            
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
            return True
        else:
            #print("--> Could not add component! Check that it is the correct component.")
            return False
        
    def nextComponent(self):
        """
        Returns the next component this widget needs
        """
        return self.componentStructure[len(self.components)]