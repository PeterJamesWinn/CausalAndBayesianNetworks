# This is protoype code to define nodes in a causal network, and then to generate data. 
# The aim is to be able to explore different network topologies and node relationships to allow
# a better understanding of corellational confounding, correcting for confounding by conditioning, 
# and the rules of do calculus. This is in response to reading Jude Pearl and Dana Mackenzie's Book of Why,
# on the topic of causal inference.

# The EvaluateNetwork() call has initially been written to give a node the value of the sum of all incoming nodes, but future 
# iterations of the code would allow for more complex relationships. 

# The code below defines functions, classes and methods to generate networks, and has two simple networks as example networks
# to test the code and exemplify its usage. 

# Style conventions used
# Class, Method names and object attributes use CamelNotation
# Simple Instances/Variable names use underscore_notation

import numpy as np
import pandas as pd


class Node:
    def __init__(self, name, value=0):
        self.NodeValue = value
        self.NodePreviousValue = value
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
    
    def SetPreviousValue(self, value):
        self.NodePreviousValue = value

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

    
class CreateNetworkInstance:
    def __init__(self, node_list):
        self.node_list = node_list    
    
    #def NetworkSummaryDataFrame(self):   

    def EvaluateNetwork(self):
            for node in node_list:
                value = 0
                if not node.InConnections: # start node that is not dependent on any input and so does not need updating
                    #print(node.Name, "No Keys")
                    continue
                else:  # needs updating according to incoming connections
                        for in_connection in node.InConnections.keys(): # for this node go through all inputs and evaluate it's value
                            value = value + in_connection.NodeValue * node.InConnections[in_connection]
                node.SetValue(value)

    def ConvergeNetwork(self):
        # check value at all nodes. 
        # re-evaluate
        # check if different from previous evaluation. If so repeat, else return.   
        for node in node_list:
            node.SetPreviousValue(node.NodeValue)
        network.EvaluateNetwork()
        for node in node_list:

            while  abs(node.NodePreviousValue - node.NodeValue) > 0.01:
                node.SetPreviousValue(node.NodeValue)
                #print("re-evaluate")
                network.EvaluateNetwork()
        



    def PrintNetwork(self):
        for node in node_list:
            #print(node.Name)
            node.PrintNodeData()  

    def WriteNetwork(self,filename):
        filepointer=open(filename, "w")
        network_dataframe = pd.DataFrame(columns = ['Name', 'Value'])
        DataList=["NodeName", "CurrentValue", "InComingConnectionFromNodes", "InComingValues"]
        filepointer.write(str(DataList) + " \n")
        for node in node_list:
            #print(node.Name, node.NodeValue)
            DataList=[node.Name, node.NodeValue]
            #network_dataframe.append(pd.Series(DataList, index=network_dataframe.columns), ignore_index=True)
            for in_connection in node.InConnections:
                DataList.append(in_connection.Name) # in_connection is a dictionary key but that key is a node object.
                DataList.append(node.InConnections[in_connection]) 
            #print(network_dataframe)
            filepointer.write(str(DataList) + " \n")
        #print(network_dataframe)    
        filepointer.close()

    def MakeNetWorkDataFrame(self):
        DataList = []
        for node in node_list:
            DataListRow=[node.Name, node.NodeValue]
            for in_connection in node.InConnections:
                if in_connection.Name:
                    DataListRow.append(in_connection.Name) # in_connection is a dictionary key but that key is a node object.
                    DataListRow.append(node.InConnections[in_connection])
            DataList.append(DataListRow)
        # This section to sort out column names. Could be tidied up by considering the dimension of the rows and adjusting the headings dynamically.  
        #column_names = ["NodeName", "CurrentValue", "InComingConnectionFromNodes", "InComingValues"]
        network_dataframe = pd.DataFrame(DataList)
        network_dataframe.rename(columns = {0:'NodeName', 1:'CurrentValue', 2:'InComingConnectionFromNodes', 3:'InComingValues'}, inplace = True)
        return network_dataframe
    

# Define the nodes, their names and any initial values. Default value is 0
X = Node("X", 5)
B = Node("B")
Y = Node("Y")

# Define the connections that a node makes. AddOutConnection automatically also creats an AddInConnection call on the recieving node
# The below defines a simple network such that X->B->Y such that initially defining the value of X propagates through to define the values
# of B and y.  
X.AddOutConnection(B, 0.5)
#B.AddInConnection(X,0.5)
B.AddOutConnection(Y, 0.5)
#Y.AddInConnection(B,0.5)

#X.PrintNodeData()
#B.PrintNodeData()
#Y.PrintNodeData()
#X.PrintNodeData()

node_list = [X, B, Y]  # defining the node list in the order of influence, X->B->Y means that the network values with be consistent after one evaluation of the network. 
network = CreateNetworkInstance(node_list)
network.EvaluateNetwork()
network.ConvergeNetwork()
#network.PrintNetwork()
#network.WriteNetwork("NetworkParameters.csv")
network_dataframe = network.MakeNetWorkDataFrame()
print(network_dataframe)
network_dataframe.to_csv("NetworkParameters.csv", index=False, na_rep='None')

 

# Game 5 from Chapter 4 (Confounding and Deconfounding ...) of The Book of Why

A = Node("A", 5)
B = Node("B")
C = Node("C", 1)
Y = Node("Y")
X = Node("X")

A.AddOutConnection(B, 0.5)
A.AddOutConnection(X, 0.5)
B.AddOutConnection(X, 0.5)
C.AddOutConnection(B, 0.5)
C.AddOutConnection(Y, 0.5)
X.AddOutConnection(Y, 0.5)

#node_list = [A, C, B, X, Y] # giving nodes in this order leads to convergence after one iteration
node_list = [A, C, B, Y, X]  # this is a suboptimal order but network converges on second pass, which should be true of any order except the optimal
node_list = [A, B, Y, X, C]
network = CreateNetworkInstance(node_list)
network.EvaluateNetwork()
network_dataframe_game5 = network.MakeNetWorkDataFrame()
print(network_dataframe_game5)
network.ConvergeNetwork()
network_dataframe_game5 = network.MakeNetWorkDataFrame()
print(network_dataframe_game5)
network_dataframe_game5.to_csv("NetworkParameters_game5.csv", index=False, na_rep='None')

# To Do - use network definition to generate a data set. 1. Initially just randomise the key inputs and write out dataset. 2. Add noise to the outputs. 