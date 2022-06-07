"""
Defines the nodes in a causal network.
"""

# This is protoype code to define nodes in a causal network, and then to
#  generate data.  The aim is to be able to explore different network 
# topologies and node relationships to allow a better understanding of 
# corellational confounding, correcting for confounding by conditioning,
# and the rules of do calculus. This is in response to reading 
# Judea Pearl and Dana Mackenzie's Book of Why,
# on the topic of causal inference.
#
# The evaluate_network_linear() call has initially been written to give a node 
# the value of the sum of all incoming nodes, scaled by their coupling
# factor, and no bias term. 
# This has been effectively replaced by evaluate_network, which allows
# the relationship between the incoming node's value and the value 
# of the node under consideration to be modelled as y = mx + c, or 
# y=mxx +c, the a bias value also to be added.
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


def quadratic(in_value, coupling):
    return(coupling * in_value * in_value)

def linear(in_value, coupling):
    return(coupling * in_value)

class Node:
    """
    Create a node object with a node value, name, dictionary of input
    connections, dictionary of output connections.
    """

    def __init__(self, name, bias=0):
        """ 
        Initialise the node name, value, and connection lists. 
        
        node_previous_value allows comparison with node_value to see 
        if convergence of node value has been achieved when iteratively
        updating the network. 
        """
        self.node_value = bias
        self.node_previous_value = bias
        self.node_bias = bias # value of node with no inputs
        self.name = name
        self.out_connections = {}
        self.in_connections = {}

    def add_out_connection(self, node, coupling_data):
        """ 
        Add entry to the node's out_connections dictionary  
        and update the corresponding in_connections dictionary 
        of the node connecting to self . 

        The dictionary keys are Node objects, so can be iterated over
        to return the Nodes stored in the in_connections and 
        out_connections dictionaries.

        node -- the node to connect to the object node, i.e.  recorded
        in its in_connections dictionary.
        coupling_data -- could be a value for the coupling between the 
        two nodes, for use with evaluate_function(), which assumes a 
        linear coupling between the node values
        (i.e. first order polynomial).  
        Or a tuple with (coupling_value, coupling_function), where 
        coupling_function is a function defining the nature of the 
        coupling between nodes, linear or quadratic, at the time of 
        writing this update (06/06/2022), for use with 
        evaluate_network()   

        coupling_function = node.in_connections[in_connection][1]
        incoming_value = in_connection.node_value 
        coupling_value = node.in_connections[in_connection][0]

        """
        # Add to dictionary of couplings of this node (self).
        self.out_connections[node] = coupling_data
        # Add in connection to receiving node (node)
        node.in_connections[self] = coupling_data

    def add_in_connection(self, node, coupling_data):
        """ 
        Add entry to the node's in_connections dictionary.  
        Also update the corresponding out_connections dictionary 
        of the node connecting to self. 

        Not really needed if add_out_connection is used, since they
        effectively do the same from different perspectives. 

        A longer description is found in add_out_connection(), which 
        uses the same syntax/structures. 
        """
        self.in_connections[node] = coupling_data
        # Adds an out connection to the giving node
        # - it is inefficient to write in and out arrows explicitly,
        # since it duplicates, but should make user experience easier
        node.in_connections[self] = coupling_data

    def set_value(self, value):
        self.node_value = value

    def set_previous_value(self, value):
        self.node_previous_value = value

    def set_bias(self, bias):
        self.node_bias = bias

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
        self.network_node_list = node_list

    def evaluate_network_linear(self):
        """
        Iterate over nodes, once, and calculate a value for each node, 
        assuming a y=mx relationship.

        Only traverses the network once, so may not be self consistent.
        Convergence of the network is achieved by calling
        evaluate_network multiple times and checking for convergence,
        e.g. as in converge_network.
        """
        for node in self.network_node_list:
            value = 0
            #print(node.name, node.node_value)
            if not node.in_connections:# Start node  not dependent on an 
                                       # input does not need updating
                node.node_value = node.node_bias
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


    def evaluate_network(self):
        """
        Iterate over nodes, once, to calculate a value for each node.
        
        Only traverses the network once, so may not be self consistent.
         Convergence of the network is achieved by calling
        evaluate_network multiple times and checking for convergence,
        e.g. as in converge_network.
        
        Requires coupling_data, defined by  add_out_connection() or 
        add_in_connection(), and stored in the in_connections and
        out_connections dictionaries under the node key.  coupling_data
        is a tuple consisting of (coupling_value, coupling_function), 
        but could easily be extended to contain further data in the 
        future. 

        """
        for node in self.network_node_list:#for each node in the network
            value = 0
            #print(node.name, node.node_value)
            if not node.in_connections:# Start node  not dependent on an 
                                       # input; does not need updating
                node.node_value = node.node_bias #Ensure bias and value
                                                 #equal when iterating value
                continue
            else:# needs updating according to incoming connections
                # for each node (current loop), for each input 
                # connection evaluate its
                # contribution to the node value.  
                # node.in_connections[in_connection] stores the 
                # coupling value of the in coming node. I.e. the 
                # multiplier of the incoming node's value. 
                # coupling_function is linear or quadratic or etc. 
                for in_connection in node.in_connections.keys():
                    #print("connection data: ", 
                    #     node.in_connections[in_connection])
                    coupling_function = node.in_connections[in_connection][1]
                    incoming_value = in_connection.node_value 
                    coupling_value = node.in_connections[in_connection][0]
                    value = (
                        value 
                        + coupling_function(incoming_value, coupling_value)
                    )
                    
            value = value + node.node_bias
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
        for node in self.network_node_list:
            node.set_previous_value(node.node_value)
        self.evaluate_network()
        for node in self.network_node_list:
            # If a node is found to differ from it's previous value
            # we need to save the current values as previous
            # and iterate the values of nodes in the network again
            while abs(node.node_previous_value - node.node_value) > 0.01:
                node.set_previous_value(node.node_value)
                print("re-evaluate")
                self.evaluate_network() 



    def converge_network_linear(self):
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
        for node in self.network_node_list:
            node.set_previous_value(node.node_value)
        self.evaluate_network_linear()
        for node in self.network_node_list:
            # If a node is found to differ from it's previous value
            # we need to save the current values as previous
            # and iterate the values of nodes in the network again
            while abs(node.node_previous_value - node.node_value) > 0.01:
                node.set_previous_value(node.node_value)
                print("re-evaluate")
                self.evaluate_network_linear() 

    def print_network(self):
        for node in self.node_list:
            # print(node.Name)
            node.print_node_data()

    def write_network_parameters(self, filename):
        """ Write network parameters to file. I.e. connections, 
        couplings, values at nodes."""
        #with open(filename, 'w') as filepointer:
        filepointer = open(filename, "w")
        data_list = [
            "NodeName",
            "CurrentValue",
            "InComingConnectionFromNodes",
            "InComingValues"]
        filepointer.write(str(data_list) + " \n")
        for node in self.network_node_list:
            #print(node.Name, node.NodeValue)
            data_list = [node.name, node.node_bias, node.node_value]
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

    def make_network_parameters_dataframe(self):
        """ Write network parameters to file. I.e. connections, 
        couplings, values at nodes."""
        data_list = []
        for node in self.network_node_list:
            data_list_row = [node.name, node.node_bias, node.node_value]
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
                1: 'Node Bias Value',
                2: 'CurrentValue',
                3: 'InComingConnectionFromNodes',
                4: 'InComingValues - Coupling and FunctionForm'},
            inplace=True)
        return network_dataframe





# To Do - 
# Take examples out and add to a Jupyter notebook. 
# Allow more complicated functional form. 
# use network definition to generate a data set. 
# 1. Initially just randomise the key inputs and write out dataset. 
# 2. Add noise to the outputs.
