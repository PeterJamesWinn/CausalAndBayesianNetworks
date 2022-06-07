# This is protoype code to define nodes in a causal network, and then to
#  generate data.  The aim is to be able to explore different network 
# topologies and node relationships to allow a better understanding of 
# corellational confounding, correcting for confounding by conditioning,
# and the rules of do calculus. This is in response to reading 
# Judea Pearl and Dana Mackenzie's Book of Why,
# on the topic of causal inference.
#
# The EvaluateNetwork() call has initially been written to give a node 
# the value of the sum of all incoming nodes, but future
# iterations of the code would allow for more complex relationships.
#
# The code below defines functions, classes and methods to generate 
# networks, and has two simple networks as example networks
# to test the code and exemplify its usage.
#
# Style conventions used:
# Class names use CamelNotation
# Method names and instance variables use lower case underscore_notation.
# Simple Instances, functions and variable names use underscore_notation.
# i.e. aiming to follow the Python pep8 style guide.

import numpy as np
import pandas as pd


class Node:
    """
    Create a node object with a node value, name, dictionary of input
    connections, dictionary of output connections.
    """

    def __init__(self, name, value=0):
        """ 
        Initialise the node name, value, and connection lists. 
        
        node_previous_value allows comparison with node_value to see 
        if convergence of node value has been achieved when iteratively
        updating the network. 
        """
        self.node_value = value
        self.node_previous_value = value
        self.name = name
        self.out_connections = {}
        self.in_connections = {}

    def add_out_connection(self, node, coupling):
        """ 
        Add entry to the node's out_connections dictionary  
        and update the corresponding in_connections dictionary 
        of the node connecting to self. 

        The dictionary keys are node objects, so can be iterated over
        to return the nodes stored in the in_connections and 
        out_connections dictionaries.

        """
        # Add to dictionary of couplings of this node (self).
        self.out_connections[node] = coupling
        # Add in connection to receiving node (node)
        node.in_connections[self] = coupling

    def add_in_connection(self, node, coupling):
        """ 
        Add entry to the node's in_connections dictionary.  
        Also update the corresponding out_connections dictionary 
        of the node connecting to self. 

        Not really needed if add_out_connection is used, since they
        effectively do the same from different perspectives. 
        """
        self.in_connections[node] = coupling
        # Adds an out connection to the giving node
        # - it is inefficient to write in and out arrows explicitly,
        # since it duplicates, but should make user experience easier
        node.in_connections[self] = coupling

    def set_value(self, value):
        self.node_value = value

    def set_previous_value(self, value):
        self.node_previous_value = value

    def print_node_data(self):
        """
        Print the name, value, out connections, in connections of
        a node.
        """
        print("\n Start node data \n")
        print("name")
        print(self.name)
        print("value ")
        print(self.node_value)
        print("-----------------------\n")
        print("Out connections \n")
        for connection in self.out_connections.keys():
            print(connection.Name)
            print(self.out_connections[connection])

        print("-----------------------\n")
        print("In connections \n")
        for connection in self.in_connections.keys():
            print(connection.Name)
            print(self.in_connections[connection])
        print("Done node data \n")


class NetworkInstance:
    """
    Create a network object from a list of nodes defined by the
    Node class.
    """

    def __init__(self, node_list):
        self.node_list = node_list

    def evaluate_network(self):
        """
        Iterate over nodes, once, to calculate a value for each node.

        Only traverses the network once, so may not be self consistent.
        Convergence of the network is achieved by calling
        evaluate_network multiple times and checking for convergence,
        e.g. as in converge_network.
        """
        for node in node_list:
            value = node.node_value
            if not node.in_connections:# Start node  not dependent on an 
                                       # input does not need updating
                continue
            else: # needs updating according to incoming connections
                # for each node, for each input connection evaluate its
                # contribution to the node value.  
                # node.in_connections[in_connection] stores the 
                # coupling value of the in coming node. I.e. the 
                # multiplier of the incoming node's value. 
                for in_connection in node.in_connections.keys():
                    value = value + in_connection.node_value * \
                        node.in_connections[in_connection] 
            node.set_value(value)

    def converge_network(self):
        """
        Use the evalute_network method to calculate the value
        at every node and then repeat until a consistent value is
        obtained.

        The value at each node depends on the value at the nodes
        connected to it, so the network may need to be traversed
        several times before it is self consistent.
        """
        # Check value at all nodes.
        # Re-evaluate.
        # Check if different from previous evaluation. If so repeat, else
        # Return.
        for node in node_list:
            node.set_previous_value(node.node_value)
        network.evaluate_network()
        
        for node in node_list:
            while abs(node.node_previous_value - node.node_value) > 0.01:
                node.set_previous_value(node.node_value)
                # print("re-evaluate")
                network.evaluate_network()

    def print_network(self):
        for node in node_list:
            # print(node.Name)
            node.print_node_data()

    def write_network(self, filename):
        #with open(filename, 'w') as filepointer:
        filepointer = open(filename, "w")
        network_dataframe = pd.DataFrame(columns=['Name', 'Value'])
        data_list = [
            "NodeName",
            "CurrentValue",
            "InComingConnectionFromNodes",
            "InComingValues"]
        filepointer.write(str(data_list) + " \n")
        for node in node_list:
            #print(node.Name, node.NodeValue)
            data_list = [node.name, node.node_value]
            #network_dataframe.append(pd.Series(DataList, index=network_dataframe.columns), ignore_index=True)
            for in_connection in node.in_connections:
                # in_connection is a dictionary key but that key is a 
                # node object.
                data_list.append(in_connection.name)
                data_list.append(node.in_connections[in_connection])
            # print(network_dataframe)
            filepointer.write(str(data_list) + " \n")
        # print(network_dataframe)
        filepointer.close()

    def make_network_dataframe(self):
        data_list = []
        for node in node_list:
            data_list_row = [node.name, node.node_value]
            for in_connection in node.in_connections:
                if in_connection.name:
                    # in_connection is a dictionary key but that key is 
                    # a node object.
                    data_list_row.append(in_connection.name)
                    data_list_row.append(node.in_connections[in_connection])
            data_list.append(data_list_row)
        # This section to sort out column names. Could be tidied up by 
        # considering the dimension of the rows and adjusting the 
        # headings dynamically.
        # column_names = 
        #  ["NodeName", "CurrentValue", 
        #   "InComingConnectionFromNodes", "InComingValues"]
        network_dataframe = pd.DataFrame(data_list)
        network_dataframe.rename(
            columns={
                0: 'NodeName',
                1: 'CurrentValue',
                2: 'InComingConnectionFromNodes',
                3: 'InComingValues'},
            inplace=True)
        return network_dataframe


# Define the nodes, their names and any initial values. Default value is 0
X = Node("X", 5)
B = Node("B")
Y = Node("Y")

# Define the connections that a node makes. 
# AddOutConnection automatically also creats an AddInConnection 
# call on the recieving node
# The below defines a simple network such that X->B->Y 
# such that initially defining the value of X propagates through 
# to define the values
# of B and y.
X.add_out_connection(B, 0.5)
# B.AddInConnection(X,0.5)
B.add_out_connection(Y, 0.5)
# Y.AddInConnection(B,0.5)

# X.PrintNodeData()
# B.PrintNodeData()
# Y.PrintNodeData()
# X.PrintNodeData()

# defining the node list in the order of influence, X->B->Y means that the
# network values with be consistent after one evaluation of the network.
node_list = [X, B, Y]
network = NetworkInstance(node_list)
network.evaluate_network()
network.converge_network()
network_dataframe = network.make_network_dataframe()
print(network_dataframe)
network_dataframe.to_csv("NetworkParameters.csv", index=False, na_rep='None')


# Game 5 from Chapter 4 (Confounding and Deconfounding ...) 
# of The Book of Why.  

A = Node("A", 5)
B = Node("B")
C = Node("C", 1)
Y = Node("Y")
X = Node("X")

A.add_out_connection(B, 0.5)
A.add_out_connection(X, 0.5)
B.add_out_connection(X, 0.5)
C.add_out_connection(B, 0.5)
C.add_out_connection(Y, 0.5)
X.add_out_connection(Y, 0.5)

# node_list = [A, C, B, X, Y] # giving nodes in this order leads to
# convergence after one iteration
# this is a suboptimal order but network converges on second pass, which
# should be true of any order except the optimal
node_list = [A, C, B, Y, X]
node_list = [A, B, Y, X, C]
network = NetworkInstance(node_list)
network.evaluate_network()
network_dataframe_game5 = network.make_network_dataframe()
print(network_dataframe_game5)
network.converge_network()
network_dataframe_game5 = network.make_network_dataframe()
print(network_dataframe_game5)
network_dataframe_game5.to_csv(
    "NetworkParameters_game5.csv",
    index=False,
    na_rep='None')

# To Do - 
# Take examples out and add to a Jupyter notebook. 
# Allow more complicated functional form. 
# use network definition to generate a data set. 
# 1. Initially just randomise the key inputs and write out dataset. 
# 2. Add noise to the outputs.

print("\n Node docstring:", Node.__doc__)