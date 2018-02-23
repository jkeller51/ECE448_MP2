# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 15:41:43 2018

@author: jkell
"""

import include as inc
import copy

def add_widget(Widgets, value):
    # add widget to a list of widgets
    # don't worry, it won't add to a widget if it
    # is not the correct component
    newWidgets = copy.deepcopy(Widgets)
    for w in newWidgets:
        w.addComponent(value)
    return newWidgets

def traceback(lastnode):
    """
    Using the current node, find the path it took to get there.
    """
    
    path = []
    curnode = lastnode
    while (curnode.previous != None):
        path.insert(0,curnode)
        curnode = curnode.previous
    
    return path
    

def solve_min_stops(Widgets):
    # heuristic: average number of parts needed to
    # complete each widget
    
    print("Solving for minimum number of stops...")

    frontier = []  # this will be a list of nodes
    
    startNode1 = inc.Node('',Widgets,0,None)
    
    frontier.append(startNode1)
    prevcost = 0
    step=0
    
    while len(frontier) > 0:
        step+=1
        
        # decide what node to expand next
        mineval = 9999
        minnode = None
        for n in frontier:
            if (n.evaluation < mineval):
                mineval = n.evaluation
                minnode = n
        
        curWidgets = minnode.widgets
        
        if minnode.cost != prevcost:
            prevcost = minnode.cost
            #print("cost:",prevcost)
        
        # check if widgets are all done
        alldone = True
        for w in curWidgets:
            if w.done == False:
                alldone = False
                break
        if (alldone == True):
            break
        
        # generate new nodes
        newNodeA = inc.Node('A',add_widget(curWidgets, 'A'), minnode.cost+1, minnode)
        newNodeB = inc.Node('B',add_widget(curWidgets, 'B'), minnode.cost+1, minnode)
        newNodeC = inc.Node('C',add_widget(curWidgets, 'C'), minnode.cost+1, minnode)
        newNodeD = inc.Node('D',add_widget(curWidgets, 'D'), minnode.cost+1, minnode)
        newNodeE = inc.Node('E',add_widget(curWidgets, 'E'), minnode.cost+1, minnode)
        
        if (newNodeA.evaluation != mineval+1):  # ignore new states where nothing was accomplished
            frontier.append(newNodeA)
        if (newNodeB.evaluation != mineval+1):
            frontier.append(newNodeB)
        if (newNodeC.evaluation != mineval+1):
            frontier.append(newNodeC)
        if (newNodeD.evaluation != mineval+1):
            frontier.append(newNodeD)
        if (newNodeE.evaluation != mineval+1):
            frontier.append(newNodeE)
        
        frontier.remove(minnode)
        
    path = traceback(minnode)
    
    print("Path with minimum stops:")
    pathstr = ""
    for n in path:
        pathstr+=n.value
    print(pathstr)
    print("Stops:",minnode.cost)
    print("Nodes expanded:", step)
        
    

if __name__ == '__main__':
    Widget1 = inc.Widget("AEDCA")
    Widget2 = inc.Widget("BEACD")
    Widget3 = inc.Widget("BABCE")
    Widget4 = inc.Widget("DADBD")
    Widget5 = inc.Widget("BECBD")
    
    Widgets = [Widget1, Widget2, Widget3, Widget4, Widget5] # container for passing to function
    
    solve_min_stops(Widgets)