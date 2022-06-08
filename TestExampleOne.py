
from network_generator import *

# Define the nodes, their names and any initial values. Default value is 0
X = Node("X", 5)
B = Node("B", 1)
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
network1 = NetworkInstance(node_list)

network1.evaluate_network_linear()
network1.converge_network_linear()
network1_dataframe = network1.make_network_parameters_dataframe()
print(network1_dataframe)
#network_dataframe.to_csv("NetworkParameters.csv", index=False, na_rep='None')
