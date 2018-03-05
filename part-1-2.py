# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 12:44:45 2018

@author: jkell
"""

import include as inc
import copy

MINMILES=5710

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
                    if (a.widgetcount == cs.widgetcount and a.location == cs.location):
                        add=False
                        a.previousStates.append(s)
                        break
                if (add == True):
                    newstates.append(cs)
                    cs.previousStates.append(s)
        
        return Layer(newstates)
    
    def findState(self, wcount, loc):
        # find a state with the same wcount and location
        # or return None
        rstate = None
        for s in self.states:
            if s.widgetcount == wcount and s.location == loc:
                rstate = s
                break
                
        return rstate
        
        
class State:
    # all actions are mutex. we only have one action per time step.
    
    def __init__(self, widgets, location):
        self.location = location
        self.widgets = widgets
        self.widgetcount = [len(widgets[0].components),
                            len(widgets[1].components),
                            len(widgets[2].components),
                            len(widgets[3].components),
                            len(widgets[4].components)]
        self.previousStates = []
        
    def generateChildren(self):
        childstates = []
        for i in ['A','B','C','D','E']:
            if i != self.location:  # we don't waste time with duplicate states
                childstates.append(State(add_component(self.widgets, i),i))
        return childstates
    
    def printState(self):
        print(self.location,self.widgetcount)
    
    
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
        
def print_path_steps(path):
    newpath = path[::-1]
    for state,idx in newpath:
        if (idx == 0):
            continue
        
                
        print("A"+str(idx)+": Go to",state.location)
        print("S"+str(idx)+":",state.widgetcount)
#        print("---->previous: ")
#        for s in state.previousStates:
#            s.printState()
        
        
def print_frontier(frontier):
    i=0
    for state,idx,path in frontier:
        print(state.widgetcount, idx)
        print_path(path)
        print("")
        i+=1
        if (i>5):
            break
        
def path_mileage(path):
    mileage=0
    newpath = path[::-1]
    q=0
    for state,idx in newpath:
        if (q == 0):
            lastplace=''
            q+=1
            continue
            
        if (state.location == ''):
            pass
        else:
#            print(lastplace+"->"+state.location,inc.get_miles(lastplace,state.location))
            mileage+=inc.get_miles(lastplace,state.location)
            lastplace=state.location
        
    return mileage

def backtrace(layers,goal=[5,5,5,5,5]):
    # find a valid path to the goal state
    # using modified DFS
    
    currentidx = len(layers)-1
    
    
    path = []
    foundsolution=False
    minmiles = 999999
    
    frontier = []
    
    for i in ['A','B','C','D','E']:
        currentState = layers[currentidx].findState(goal,i)
        if (currentState != None):
            frontier.append([currentState,currentidx, path])
    
    while len(frontier) > 0:
        # go back 1 layer
        currentState = frontier[0][0]
        currentidx = frontier[0][1]
        path = frontier[0][2]
        path.append([currentState, currentidx])
        
        frontier.pop(0)
        
        miles = path_mileage(path)
        if (miles > minmiles):
            continue
        if (currentidx == 0):
            # we've reached the initial layer
#            print("----- Path Found ------")
#            print("Mileage:",miles)
#            print("Steps:", len(path))
            #print_path_steps(path)
            if (miles < minmiles):
                minmiles = miles
            
            if (miles > MINMILES):
                #we know from 1-1 that this is the minimum
            
                continue
            else:
                foundsolution=True
                break
        
        
        for s in currentState.previousStates:
            frontier.insert(0, [s,currentidx-1, copy.copy(path)])
            # insert at beginning (DFS)
    

    if (foundsolution == True):
        return path
    else:
        return None
    
        
def mileage_chars(inp):
    summ=0
    for i in range(1,len(inp)):
        summ+=inc.get_miles(inp[i-1],inp[i])
#        print(inp[i-1]+"->"+inp[i],inc.get_miles(inp[i-1],inp[i]))
    return summ
        

def print_previous(state):
    print("Previous States:")
    for s in state.previousStates:
        s.printState()
    
    
if __name__ == '__main__':
    Widget1 = inc.Widget("AEDCA")
    Widget2 = inc.Widget("BEACD")
    Widget3 = inc.Widget("BABCE")
    Widget4 = inc.Widget("DADBD")
    Widget5 = inc.Widget("BECBD")
    
    Widgets = [Widget1, Widget2, Widget3, Widget4, Widget5] # container for passing to function
    
    layers = []
    InitState = State(Widgets,'')
    InitLayer = Layer([InitState])
    
    layers.append(InitLayer)
    asolution = False
    
    while True:
        if (check_widgets_finished(layers[len(layers)-1]) and asolution==False):
            asolution=True
            print("Minimum step solution found.")
        
        if (asolution == True):
            print("Backtracing layer",len(layers)-1)
            print("Fluents:", len(layers[len(layers)-1].states))
            print()
            result = backtrace(layers)
#            custombacktrace(layers)
            if (result != None):
                break
            
        layers.append(layers[len(layers)-1].nextLayer())
    
    
    print("Problem solved.")
    print_path_steps(result)
    print("Mileage:",path_mileage(result))