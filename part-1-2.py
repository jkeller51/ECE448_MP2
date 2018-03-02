# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 12:44:45 2018

@author: jkell
"""

import include as inc
import copy


class Layer:
    # layer contains all possible states at that step
    def __init__(self, states=None):
        self.states = states
        
    def nextLayer(self):
        newstates = []
        for s in self.states:
            children = s.generateChildren()
            for cs in children:
                add = True
                for a in newstates:
                    if (a.widgetcount == cs.widgetcount):
                        add=False
                        break
                if (add == True):
                    newstates.append(cs)
        
        return Layer(newstates)
    
    def findState(self, wcount):
        # find a state with the same wcount
        # or return None
        rstate = None
        for s in self.states:
            if s.widgetcount == wcount:
                rstate = s
                
        return rstate
        
        
class State:
    # all actions are mutex. we only have one action per time step.
    
    def __init__(self, widgets):
        self.widgets = widgets
        self.widgetcount = [len(widgets[0].components),
                            len(widgets[1].components),
                            len(widgets[2].components),
                            len(widgets[3].components),
                            len(widgets[4].components)]
        
    def generateChildren(self):
        newStateA = State(add_component(self.widgets, 'A'))
        newStateB = State(add_component(self.widgets, 'B'))
        newStateC = State(add_component(self.widgets, 'C'))
        newStateD = State(add_component(self.widgets, 'D'))
        newStateE = State(add_component(self.widgets, 'E'))
        return [newStateA, newStateB, newStateC, newStateD, newStateE]
    
    def printState(self):
        print(self.widgetcount)
    
    
def add_component(Widgets, value):
    # add component to a list of widgets
    # don't worry, it won't add to a widget if it
    # is not the correct component
    newWidgets = copy.deepcopy(Widgets)
    for w in newWidgets:
        w.addComponent(value)
    return newWidgets

def remove_component(Widgets, value):
    # add component to a list of widgets
    # don't worry, it won't add to a widget if it
    # is not the correct component
    newWidgets = copy.deepcopy(Widgets)
    for w in newWidgets:
        w.removeComponent(value)
    return newWidgets


def check_widgets_finished(layer):
    # returns true when it is possible to finish all widgets at this stage
    for s in layer.states:
        if (s.widgetcount == [5,5,5,5,5]):
            return True
    
    return False


def print_path(path):
    for state,idx in path:
        print(str(idx)+":",state.widgetcount)
        
def print_frontier(frontier):
    i=0
    for state,idx,path in frontier:
        print(state.widgetcount, idx)
        print_path(path)
        print("")
        i+=1
        if (i>5):
            break

def backtrace(layers,goal=[5,5,5,5,5]):
    # find a valid path to the goal state
    # using modified DFS
    
    currentidx = len(layers)-1
    currentState = layers[currentidx].findState(goal)
    
    path = []
    
    frontier = [[currentState,currentidx, path]]
    
    while len(frontier) > 0:
        # go back 1 layer
        currentState = frontier[0][0]
        currentidx = frontier[0][1]
        path = frontier[0][2]
        path.append([currentState, currentidx])
        
        frontier.pop(0)
        if (currentidx == 0):
            # we've reached the initial layer
            # TODO: see if it satisfies constraints
            # if not we will...
            print("----- Path Found ------")
            print_path(path)
            print("")
            
            continue
        previousStates = []
        foundchildren = False
        for i in ['A','B','C','D','E']:
            tempwidgets = remove_component(currentState.widgets, i)
            tempcount = [len(tempwidgets[0].components),
                         len(tempwidgets[1].components),
                         len(tempwidgets[2].components),
                         len(tempwidgets[3].components),
                         len(tempwidgets[4].components)]
    
            this_state = layers[currentidx-1].findState(tempcount)
            if (this_state != None and this_state not in previousStates):
                previousStates.append(this_state)
                frontier.insert(0, [this_state,currentidx-1, copy.deepcopy(path)])
                # insert at beginning (DFS)
                foundchildren = True
        if foundchildren == True:
            pass
        else:
            print("No more children (idx=",currentidx,")")
            break
        

        
    return previousStates

if __name__ == '__main__':
    Widget1 = inc.Widget("AEDCA")
    Widget2 = inc.Widget("BEACD")
    Widget3 = inc.Widget("BABCE")
    Widget4 = inc.Widget("DADBD")
    Widget5 = inc.Widget("BECBD")
    
    Widgets = [Widget1, Widget2, Widget3, Widget4, Widget5] # container for passing to function
    
    layers = []
    InitState = State(Widgets)
    InitLayer = Layer([InitState])
    
    layers.append(InitLayer)
    
    while True:
        if (check_widgets_finished(layers[len(layers)-1])):
            break
        layers.append(layers[len(layers)-1].nextLayer())
    
    print("A solution has been found.")
    
    previous = backtrace(layers)
    