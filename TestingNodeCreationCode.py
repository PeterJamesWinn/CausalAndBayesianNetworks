

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


# Define the nodes, their names and any initial values. Default value is 0
X = Node("X", 5)
B = Node("B")
Y = Node("Y")

# Define the connections that a node makes. AddOutConnection automatically also creats an AddInConnection call on the recieving node
X.AddOutConnection(B, 0.5)
#B.AddInConnection(X,0.5)
B.AddOutConnection(Y, 0.5)
#Y.AddInConnection(B,0.5)

#X.PrintNodeData()
#B.PrintNodeData()
#Y.PrintNodeData()
#X.PrintNodeData()

node_list = [X, B, Y]
network = CreateNetworkInstance(node_list)
network.EvaluateNetwork()
network.ConvergeNetwork()
#network.PrintNetwork()
network.WriteNetwork("NetworkParameters.csv")

# TO DO
# write data to file in an easy to view way.
# create a more complex test example. 
