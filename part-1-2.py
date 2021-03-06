# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 12:44:45 2018

@author: jkell
"""
"""
====== Solution: =======
Layer: 0
Fluents: 5
Mutex links: 0
Goal fluents mutex: True
Possible solution: No

Layer: 1
Fluents: 10
Mutex links: 13
Goal fluents mutex: True
Possible solution: No

Layer: 2
Fluents: 15
Mutex links: 37
Goal fluents mutex: True
Possible solution: No

Layer: 3
Fluents: 20
Mutex links: 69
Goal fluents mutex: True
Possible solution: No

Layer: 4
Fluents: 25
Mutex links: 110
Goal fluents mutex: True
Possible solution: No

Layer: 5
Fluents: 30
Mutex links: 161
Goal fluents mutex: True
Possible solution: No

Layer: 6
Fluents: 30
Mutex links: 111
Goal fluents mutex: True
Possible solution: No

Layer: 7
Fluents: 30
Mutex links: 86
Goal fluents mutex: True
Possible solution: No

Layer: 8
Fluents: 30
Mutex links: 75
Goal fluents mutex: False
Possible solution: No

Layer: 9
Fluents: 30
Mutex links: 75
Goal fluents mutex: False
Possible solution: No

Layer: 10
Fluents: 30
Mutex links: 75
Goal fluents mutex: False
Possible solution: No

Layer: 11
Fluents: 30
Mutex links: 75
Goal fluents mutex: False
Possible solution: Yes
Shortest Path: DABEDCABCED
Mileage: 7671

Layer: 12
Fluents: 30
Mutex links: 75
Goal fluents mutex: False
Possible solution: Yes
Shortest Path: DEBAEDCBACED
Mileage: 6934

Layer: 13
Fluents: 30
Mutex links: 75
Goal fluents mutex: False
Possible solution: Yes
Shortest Path: BEDCAEDEBCAED
Mileage: 6081

Layer: 14
Fluents: 30
Mutex links: 75
Goal fluents mutex: False
Possible solution: Yes
Shortest Path: DEBEACEDEBCAED
Mileage: 5816

Layer: 15
Fluents: 30
Mutex links: 75
Goal fluents mutex: False
Possible solution: Yes
Shortest Path: DEBEACEDEBECAED
Mileage: 5594

Layer: 16
Fluents: 30
Mutex links: 75
Goal fluents mutex: False
Possible solution: Yes
Shortest Path: DEBEAEDEBECAEBED
Mileage: 5473

Layer: 17
Fluents: 30
Mutex links: 75
Goal fluents mutex: False
Possible solution: Yes
Shortest Path: DEBEAEDEBECAEBEDD
Mileage: 5473
Done.
===================================
"""
import include as inc
import copy
import matplotlib.pyplot as plt

MINMILES=5473 # from 1-1

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
            #if i != self.location:  # we don't waste time with duplicate states
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
    # remove component to a list of widgets
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
        
def print_path_short(path):
    path=path[::-1]
    st = ""
    for state,idx in path:
        st = st+state.location
    return st
        
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
        
        
#def print_frontier(frontier):
#    i=0
#    for state,idx,path in frontier:
#        print(state.widgetcount, idx)
#        print_path(path)
#        print("")
#        i+=1
#        if (i>5):
#            break
        
def path_mileage(path):
    # return the total mileage of the input path
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
    
    minpath=[]
    
    frontier = []
    
    for i in ['A','B','C','D','E']:
        # add all possible goal states to the frontier
        currentState = layers[currentidx].findState(goal,i)
        if (currentState != None):
            frontier.append([currentState,currentidx, copy.copy(path)])
            
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
#            print(print_path_short(path))
#            print("Mileage:",miles)
#            print("Steps:", len(path))
            #print_path_steps(path)
            if (miles < minmiles):
                minmiles = miles
                minpath=path
            
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
        return minpath
    
        
def mileage_chars(inp):
    summ=0
    for i in range(1,len(inp)):
        summ+=inc.get_miles(inp[i-1],inp[i])
#        print(inp[i-1]+"->"+inp[i],inc.get_miles(inp[i-1],inp[i]))
    return summ
        

#def print_previous(state):
#    print("Previous States:")
#    for s in state.previousStates:
#        s.printState()
    
    
if __name__ == '__main__':
    # create widgets
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
    
    xdata = []
    ydata = []
    fluents_levels = []
    mutexlinks_levels = []
    
    # main loop
    
    while True:
        # calculate # fluents
        fluents=[]
        mutexlinks=[]
        for s in layers[len(layers)-1].states:
            for i in range(len(s.widgetcount)):
                if ((i, s.widgetcount[i]) not in fluents):
                    fluents.append((i, s.widgetcount[i]))
                    
        # count mutex links
        for wid, count in fluents:
            for wid2, count2 in fluents:
                # ^ not particularly efficient since we are double looping over some items
                if (wid2<=wid):
                    continue
                if ((wid, count, wid2, count2) in mutexlinks):
                    continue
                
                mutex=True
                for s in layers[len(layers)-1].states:
                    if (s.widgetcount[wid] == count and s.widgetcount[wid2] == count2):
                        mutex=False
                        break
                        
                if (mutex == True):
                    mutexlinks.append((wid, count, wid2, count2))
        
        goal_mutex = False
        for wid in [0,1,2,3,4]:
            for wid2 in [0,1,2,3,4]:
                if (wid2<=wid):
                    continue
                if((wid, 5, wid2, 5) in mutexlinks or (wid, 5) not in fluents or (wid2, 5) not in fluents):
                    goal_mutex = True
                    break
            if (goal_mutex == True):
                break
        
        print("Layer:", len(layers)-1)
        print("Fluents:", len(fluents))
        print("Mutex links:", len(mutexlinks))
        print("Goal fluents mutex:", str(goal_mutex))
        
        # update graph data
        fluents_levels.append(len(fluents))
        mutexlinks_levels.append(len(mutexlinks))
        xdata.append(len(layers)-1)
        
        if (check_widgets_finished(layers[len(layers)-1]) and asolution==False):
            # this is the first layer with a possible solution
            asolution=True
            #print("Minimum step solution found ("+str(len(layers)-1)+")")
        
        if (asolution == True):
            # after we've found a possible solution layer, start backtracing each layer
            #print("Backtracing layer",len(layers)-1)
            print("Possible solution: Yes")
            result = backtrace(layers)
            print("Shortest Path:", print_path_short(result))
            mm = path_mileage(result)
            print("Mileage:", mm)
            
            
            
            ydata.append(mm)
            if (len(layers) == 18):
                break
        else:
            print("Possible solution: No")
            ydata.append(float('nan'))
            
        layers.append(layers[len(layers)-1].nextLayer())
        print()
    
    print("Done.")
    
    plt.figure()
    plt.plot(xdata, ydata)
    plt.title('Minimum Mileage')
    plt.ylabel("Miles")
    plt.xlabel("Layer")
    
    plt.figure()
    plt.plot(xdata, fluents_levels)
    plt.title('Fluents')
    plt.xlabel("Layer")
    
    plt.figure()
    plt.plot(xdata, mutexlinks_levels)
    plt.title('Mutex Links')
    plt.xlabel("Layer")
    
    
#    if (result != None):
#        print("Problem solved.")
#        print_path_steps(result)
#        print("Mileage:",path_mileage(result))