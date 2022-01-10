

import numpy as np
import pandas as pd


class Node:
    def __init__(self, name, value=0):
        self.NodeValue = value
        self.Name = name
        self.OutConnections = {}
        self.InConnections = {}

    def AddOutConnection(self,node,coupling):
        self.OutConnections[node]=coupling  # adding to the dictionary of couplings
        # Needs to add an in connection to the receiving node
        node.InConnections[self]=coupling

    def AddInConnection(self,node,coupling):
        self.InConnections[node]=coupling
        # Needs to add an out connection to the giving node 
        # - it is inefficient to write in and out arrows explicitly, since it duplicates, but should make user experience easier
        node.OutConnections[self]=coupling
    
    def SetValue(self, value):
        self.NodeValue = value

    def PrintNodeData(self):
        #print(self)
        print("\n Start node data \n")
        print("name")
        print(self.Name)
        print("value ")
        print(self.NodeValue)
        print("-----------------------\n")
        print("Out connections \n")
        for connection in self.OutConnections.keys():
            print(connection.Name)
            print(self.OutConnections[connection])
        
        print("-----------------------\n")
        print("In connections \n")
        for connection in self.InConnections.keys():
            print(connection.Name)
            print(self.InConnections[connection])
        print("Done node data \n")

X = Node("X", 5)
B = Node("B")
Y = Node("Y")
X.AddOutConnection(B, 0.5)
#B.AddInConnection(X,0.5)
B.AddOutConnection(Y, 0.5)
#Y.AddInConnection(B,0.5)

X.PrintNodeData()
B.PrintNodeData()
Y.PrintNodeData()