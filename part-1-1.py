# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 15:41:43 2018

@author: jkell
"""

import include as inc

def solve_min_stops(Widgets):
    # heuristic: average number of parts needed to
    # complete each widget

    frontier = []  # this will be a list of nodes
    
    startNode1 = inc.Node("A",0,5,None)
    startNode2 = inc.Node("B",0,5,None)
    startNode3 = inc.Node("C",0,5,None)
    startNode4 = inc.Node("D",0,5,None)
    startNode5 = inc.Node("E",0,5,None)
    
    frontier.append(startNode1)
    frontier.append(startNode2)
    frontier.append(startNode3)
    frontier.append(startNode4)
    frontier.append(startNode5)
    
    

if __name__ == '__main__':
    Widget1 = inc.Widget("AEDCA")
    Widget2 = inc.Widget("BEACD")
    Widget3 = inc.Widget("BABCE")
    Widget4 = inc.Widget("DADBD")
    Widget5 = inc.Widget("BECBD")
    
    Widgets = [Widget1, Widget2, Widget3, Widget4, Widget5] # container for passing to function