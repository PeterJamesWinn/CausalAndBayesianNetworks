# This is protoype code to define nodes in a causal network, and then to generate data. 
# The aim is to be able to explore different network topologies and node relationships to allow
# a better understanding of corellational confounding, correcting for confounding by conditioning, 
# and the rules of do calculus. This is in response to reading Jude Pearl and Dana Mackenzie's Book of Why,
# on the topic of causal inference.


# Style conventions used
# Class, Method names and object attributes use CamelNotation
# Simple Instances/Variable names use underscore_notation

import numpy as np
import pandas as pd


class Node:
    def __init__(self, name, value=0):
        self.NodeValue = value
        self.Name = name
        self.OutConnections = {}
        self.InConnections = {}

    def AddOutConnection(self,node,coupling):
        #X = Node("X", 5)
        #B = Node("B")
        #Y = Node("Y")
        #X.AddOutConnection(B, 0.5)
        #B.AddOutConnection(Y, 0.5)'
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



class CreateNetworkInstance:
    def __init__(self, node_list):
        self.node_list = node_list
    
    #def NetworkRandomDataAssign(self):

# Create iterate over nodes method and use a wrapper. Include function in call e.g. decorator type thing. Value = 0 should be value = node.value()??

    def EvaluateNetwork(self):
        reiterate = 1
        while reiterate == 1:
            convergence_check_vector = np.ones(len(node_list))
            convergence_check_vector_pointer = 0
            value = 0
            for node in node_list:
                if node.InConnections.keys() == None: # start node that is not dependent on any input and so does not need updating
                    #print(node)
                    convergence_check_vector[convergence_check_vector_pointer] = 0
                    convergence_check_vector_pointer += 1
                    continue
                    #value = node.NodeValue()
                else:  # needs updating according to incoming connections
                        previous_value = value  # for checking convergence
                        value = 0
                        for in_connection in node.InConnections.keys(): # for this node go through all inputs and evaluate it's value
                            print("in connection data")
                            print(in_connection. Name, in_connection.NodeValue)
                            print(node.InConnections[in_connection])
                            print(value)
                            print("value prior to calculation: " + str(value))
                            node.PrintNodeData()
                            value = value + in_connection.NodeValue * node.InConnections[in_connection]
                            print("value after  calculation: " + str(value))
                        convergence_check_vector[convergence_check_vector_pointer] = abs(value - previous_value)
                        convergence_check_vector_pointer += 1
                node.SetValue(value)
            reiterate = 0 
            #for value in convergence_check_vector: 
             #   print("\n Convergence Check")
             #   print(value)
              #  if value  > 0.01:
              #      reiterate = 1  
              #      break
              #  else:
              #      reiterate = 0
            


    def PrintNetwork(self):
        for node in node_list:
            #print(node.Name)
            node.PrintNodeData()
                  

X = Node("X", 5)
B = Node("B")
Y = Node("Y")
X.AddOutConnection(B, 0.5)
#B.AddInConnection(X,0.5)
B.AddOutConnection(Y, 0.5)
#Y.AddInConnection(B,0.5)



node_list = [X, B, Y]
network = CreateNetworkInstance(node_list)

network.EvaluateNetwork()
network.PrintNetwork()

# Need to demonstrate simple evaluation of network so need to output values of the network at different iterations. 
# write as CSV? using pandas function?  But then do we need to change the data structure in between? 
