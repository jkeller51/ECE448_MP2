# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 12:51:13 2018

@author: jkell
"""

mileageTable = [[0, 1064, 673, 1401, 277],
                [1064, 0, 958, 1934, 337],
                [673, 958, 0, 1001, 399],
                [1401, 1934, 1001, 0, 387],
                [277, 337, 399, 387, 0]]

minMileageTable = [[0, 614, 673, 664, 277],
                   [614, 0, 736, 724, 337],
                   [673, 736, 0, 786, 399],
                   [661, 724, 786, 0, 387],
                   [277, 337, 399, 387, 0]]


class Node():
    
    
    def __init__(self, value, widgets, cost, previous, miles=False):
        """
        value : the component added at this node
        widgets : list of widgets
        cost  : cost to get to this point
        evaluation : cost plus heuristic to reach the goal
        previous : previous Node, for traceback
        widgets : 
        """
        
        self.value = value
        self.widgets = widgets
        self.cost = cost
        self.previous = previous
        if (miles == False):
            self.evaluation = self.cost+average_parts_needed(widgets)
        else:
            if (self.value == ''): # start node
                self.evaluation=0  # don't care.
            else:
                self.evaluation = self.cost+minimum_miles_needed(widgets, self.value)

class Widget():
    """ Our widget object
        Contains variables and methods for components
    """
    
    def __init__(self, componentString):
        """
        Use componentString to define how to build this widget
        """
        self.done=False
        self.components=[]
        self.componentStructure=[]
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
            if (self.components == self.componentStructure):
                self.done=True
            return True
        else:
            #print("--> Could not add component! Check that it is the correct component.")
            return False
        
    def removeComponent(self, component):
        """
        args
            component : a character for the widget to remove
            
        return value:
            True if component removed correctly
            False if couldn't remove
        """
        if (len(self.components) == 0):
            return False
        if (self.components[len(self.components)-1] == component):
            self.components.pop(len(self.components)-1)
            if (self.components != self.componentStructure):
                self.done=False
            return True
        else:
            return False
        
    def nextComponent(self):
        """
        Returns the next component this widget needs
        """
        if self.done == False:
            return self.componentStructure[len(self.components)]
        else:
            return None
        
        
def average_parts_needed(Widgets):
    # generate the average number of parts left to add to widgets
    summ=0
    for w in Widgets:
        summ+=len(w.componentStructure)-len(w.components)
        
    return summ/len(Widgets)

def get_miles(start, end):
    if (start == ''):
        return 0
    start_int = ord(start)-ord('A')
    end_int = ord(end) - ord('A')
    
    return mileageTable[start_int][end_int]

def get_min_miles(start, end):
    if (start == ''):
        return 0
    start_int = ord(start)-ord('A')
    end_int = ord(end) - ord('A')
    
    return minMileageTable[start_int][end_int]
    
def minimum_miles_needed(Widgets,curplace):
    """
    Find the widget that needs the most parts
    and add up the mileage to get the parts
    for just that widget
    """
    mincomponents=99
    minwidget = None
    for w in Widgets:
        if (len(w.components) < mincomponents):
            mincomponents = len(w.components)
            minwidget = w
    
    summ=0
    for i in range(len(minwidget.components),len(minwidget.componentStructure)):
        if (i == len(minwidget.components)):
            pl = curplace
        else:
            pl = minwidget.componentStructure[i-1]
            
        summ+=get_min_miles(pl, minwidget.componentStructure[i])
        
    return summ

#def minimum_miles_needed(Widgets,curplace):
#    """
#    Find the widget that needs the most parts
#    and add up the mileage to get the parts
#    for just that widget
#    """
#    mincomponents=99
#    minwidget = None
#    for w in Widgets:
#        if (len(w.components) < mincomponents):
#            mincomponents = len(w.components)
#            minwidget = w
#    
#    summ=0
#    for i in range(len(minwidget.components),len(minwidget.componentStructure)):
#        if (i == len(minwidget.components)):
#            pl = curplace
#        else:
#            pl = minwidget.componentStructure[i-1]
#            
#        #summ+=get_miles(pl, minwidget.componentStructure[i])
#        summ+=277 # minimum miles you'll have to travel per step
#        
#    return summ