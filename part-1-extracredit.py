# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 11:03:45 2018

@author: jkell

=========== Solution =================
N = 3

Solving for minimum number of stops...
Path with minimum stops:
EBACBDE
Stops: 7
Nodes expanded: 389

Solving for minimum mileage...
Path with least mileage:
EBECAEDEB
Miles: 3134
Nodes expanded: 467


N = 4

Solving for minimum number of stops...
Path with minimum stops:
ABDCAECD
Stops: 8
Nodes expanded: 683

Solving for minimum mileage...
Path with least mileage:
BEACEDECAED
Miles: 4196
Nodes expanded: 1138


N = 5

Solving for minimum number of stops...
Path with minimum stops:
ECBEDACBDAC
Stops: 11
Nodes expanded: 20172

Solving for minimum mileage...
Path with least mileage:
CEDEBECAEBEDEAC
Miles: 5594
Nodes expanded: 10884


N = 6

Solving for minimum number of stops...
Path with minimum stops:
ADEBCEADCBED
Stops: 12
Nodes expanded: 22200

Solving for minimum mileage...
Path with least mileage:
AEDEBECEACEDEBED
Miles: 5707
Nodes expanded: 12089


N = 7

Solving for minimum number of stops...
Path with minimum stops:
CADECBEADACEDA
Stops: 14
Nodes expanded: 98638

Solving for minimum mileage...
Path with least mileage:
CAECEAEDEBEDEACEA
Miles: 6150
Nodes expanded: 10788

N = 8

Solving for minimum number of stops...
Path with minimum stops:
CAEDCBAECABDECAB
Stops: 16
Nodes expanded: 607737

Solving for minimum mileage...
Path with least mileage:
CAEDECEBEAECAEBEDECAEB
Miles: 8233
Nodes expanded: 1232501

"""

import part_1_1 as prog
import include as inc
import random
import matplotlib.pyplot as plt

def randstring(N):
    # generate a widget string of length N
    # no duplicate letters in a row
    chars = ['A','B','C','D','E']
    s = chars[random.randint(0,4)]
    for i in range(0,N-1):
        q = random.randint(0,4)
        while (chars[q] == s[len(s)-1]):
            # we don't want duplicates in a row
            q = random.randint(0,4)
        s+=chars[q]
    return s

if __name__ == '__main__':
    minstep_nodes = []
    minmile_nodes = []
    x = [3,4,5,6,7,8]
    for N in x:
        print("N =",N)
        print()
        
        # generate the widgets
        
        Widget1 = inc.Widget(randstring(N))
        Widget2 = inc.Widget(randstring(N))
        Widget3 = inc.Widget(randstring(N))
        Widget4 = inc.Widget(randstring(N))
        Widget5 = inc.Widget(randstring(N))
        
        Widgets = [Widget1, Widget2, Widget3, Widget4, Widget5] # container for passing to function
        
        # solve for minimum steps
        minstep_nodes.append(prog.solve(Widgets))
        print()
        # solve for minimum mileage
        minmile_nodes.append(prog.solve(Widgets,True))
        print()
        print()
        
    minstep_nodes = [389,  683,  20172, 22200, 98638, 607737]
    minmile_nodes = [467, 1138, 10884, 12089, 10788, 1232501]
    
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(x, minstep_nodes)
    plt.yscale('log')
    plt.title('Minimum Step Nodes Expanded')
    plt.xlabel('N')
    
    plt.subplot(2,1,2)
    plt.plot(x, minmile_nodes)
    plt.title('Minimum Mileage Nodes Expanded')
    plt.xlabel('N')
    plt.yscale('log')
    plt.tight_layout()
    plt.show()
    
    