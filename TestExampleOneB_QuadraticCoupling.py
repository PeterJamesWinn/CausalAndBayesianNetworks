
from network_generator import *


# Define the connections that a node makes. 
# add_out_connection automatically also creats an add_in_connection 
# call on the recieving node.
#
# The below defines a simple network such that X->B->Y 
# such that initially defining the value of X propagates through 
# to define the values
# of B and y.
X = Node("X", 5)
B = Node("B", 1)
Y = Node("Y")
X.add_out_connection(B, (0.5, quadratic))
B.add_out_connection(Y, (0.5, linear))

# X.PrintNodeData()
# B.PrintNodeData()
# Y.PrintNodeData()

# defining the node list in the order of influence, X->B->Y means that the
# network values with be consistent after one evaluation of the network.
node_list = [X, B, Y]
network2 = NetworkInstance(node_list)
print("network instance defined: X B Y , quadratic, linear")
network2.evaluate_network()
network2.converge_network()
network2_dataframe = network2.make_network_parameters_dataframe()
print(network2_dataframe)

# block to iterate through values of X 
node_and_range = (X, range(1,16)) 
# defined as a tuple with the idea that a list of tuples could be passed
# to scan_parameters
data_from_scanningX = network2.scan_parameters(node_and_range)

# write scanned data to file
column_names = network2.list_of_node_names()  
network2_values_dataframe = pd.DataFrame(data_from_scanningX, columns=column_names)
network2_values_dataframe.to_csv(
                                "Example1B_Quadratic_NetworkValues.csv",
                                index=False,
                                na_rep='None')

# Write network parameters to file, including last converged values. 
network2.write_network_parameters("Example1B_NetworkParameters.txt")  
network2_parameters_frame=network2.make_network_parameters_dataframe()
network2_parameters_frame.to_csv(
                                "Example1B_NetworkParameters.csv",
                                index=False,
                                na_rep='None')

#def add_gaussian_noise(value, standard_deviation):
#    import random
#    random.gauss(value, standard_deviation)


