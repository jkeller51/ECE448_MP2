# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 15:41:43 2018

@author: jkell

====== Solution: =======
Solving for minimum number of stops...
Path with minimum stops:
BDAEDCBACDE
Stops: 11
Nodes expanded: 17076


Solving for minimum mileage...
Path with least mileage:
DEBEAEDEBECAEBED
Miles: 5473
Nodes expanded: 9104
=========================
    
"""

import include as inc
import copy

def add_component(Widgets, value):
    # add component to a list of widgets
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
    

def solve(Widgets, mileage=False):
    # heuristic: average number of parts needed to
    # complete each widget
    
    if (mileage == False):
        print("Solving for minimum number of stops...")
    else:
        print("Solving for minimum mileage...")

    frontier = []  # this will be a list of nodes
    
    startNode1 = inc.Node('',Widgets,0,None)
    
    frontier.append(startNode1)
    prevcost = 0
    step=0
    
    while len(frontier) > 0:
        step+=1
        
        # decide what node to expand next
        mineval = 99999999
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
        
        if (mileage == False):
            newcost = [minnode.cost+1,minnode.cost+1,minnode.cost+1,minnode.cost+1,minnode.cost+1]
        else:
            newcost = [minnode.cost+inc.get_miles(minnode.value,'A'),
                       minnode.cost+inc.get_miles(minnode.value,'B'),
                       minnode.cost+inc.get_miles(minnode.value,'C'),
                       minnode.cost+inc.get_miles(minnode.value,'D'),
                       minnode.cost+inc.get_miles(minnode.value,'E')]
            
        # generate new nodes
        
        newNodeA = inc.Node('A',add_component(curWidgets, 'A'), newcost[0], minnode, mileage)
        newNodeB = inc.Node('B',add_component(curWidgets, 'B'), newcost[1], minnode, mileage)
        newNodeC = inc.Node('C',add_component(curWidgets, 'C'), newcost[2], minnode, mileage)
        newNodeD = inc.Node('D',add_component(curWidgets, 'D'), newcost[3], minnode, mileage)
        newNodeE = inc.Node('E',add_component(curWidgets, 'E'), newcost[4], minnode, mileage)
        
        if (newNodeA.evaluation != mineval+1 and minnode.value != 'A'):  # ignore new states where nothing was accomplished
                                                # only applies for minimum steps
            frontier.append(newNodeA)
        if (newNodeB.evaluation != mineval+1 and minnode.value != 'B'):
            frontier.append(newNodeB)
        if (newNodeC.evaluation != mineval+1 and minnode.value != 'C'):
            frontier.append(newNodeC)
        if (newNodeD.evaluation != mineval+1 and minnode.value != 'D'):
            frontier.append(newNodeD)
        if (newNodeE.evaluation != mineval+1 and minnode.value != 'E'):
            frontier.append(newNodeE)
        
        frontier.remove(minnode)
        
    path = traceback(minnode)
    
    if (mileage == False):
        print("Path with minimum stops:")
    else:
        print("Path with least mileage:")
    pathstr = ""
    for n in path:
        pathstr+=n.value
    print(pathstr)
    if (mileage == False):
        print("Stops:",minnode.cost)
    else:
        print("Miles:",minnode.cost)
    print("Nodes expanded:", step)


    

if __name__ == '__main__':
    Widget1 = inc.Widget("AEDCA")
    Widget2 = inc.Widget("BEACD")
    Widget3 = inc.Widget("BABCE")
    Widget4 = inc.Widget("DADBD")
    Widget5 = inc.Widget("BECBD")
    
    Widgets = [Widget1, Widget2, Widget3, Widget4, Widget5] # container for passing to function
    
    solve(Widgets)
    print()
    solve(Widgets,True)