
import pandas as pd
import sys, os
sys.path.append('..\\..\\')

from network_generator import *

# Define the nodes, their names and any initial values. Default value is 0
X = Node("X", 5)
B = Node("B", 1)
Y = Node("Y")

# Define the connections that a node makes. 
# add_out_connection automatically also creats an add_in_connection 
# call on the recieving node.
# The below defines a simple network such that X->B->Y 
# such that initially defining the value of X propagates through 
# to define the values of B and y.
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
network1 = NetworkInstance(node_list)
network1.evaluate_network_linear()
network1.converge_network_linear()
network1_dataframe = network1.make_network_parameters_dataframe()
print(network1_dataframe)

# block to iterate through values of X 
node_and_range = (X, range(1,16)) 

# defined as a tuple with the idea that a list of tuples could be passed
# to scan_parameters, to scan multiple parameters at once.
data_from_scanningX = network1.scan_parameters_linear(node_and_range)

# write scanned data to file
column_names = network1.list_of_node_names()  
network1_values_dataframe = pd.DataFrame(data_from_scanningX, columns=column_names)
network1_values_dataframe.to_csv(
                                "Example1_linear_NetworkValues.csv",
                                index=False,
                                na_rep='None')

# Write network parameters to file, including last converged values. 
network1.write_network_parameters("Example1_linear_NetworkParameters.txt")  
network1_parameters_frame=network1.make_network_parameters_dataframe()
network1_parameters_frame.to_csv(
                                "Example1_linear_NetworkParameters.csv",
                                index=False,
                                na_rep='None')

print("Data for node B")
B.print_node_data()
