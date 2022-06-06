
from network_generator_2 import *

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
network = NetworkInstance(node_list)

network.evaluate_network_2()
network.converge_network_2()
network_dataframe = network.make_network_dataframe()
print(network_dataframe)
#network_dataframe.to_csv("NetworkParameters.csv", index=False, na_rep='None')



#def quadratic(in_value, coupling):
#    return(coupling * in_value * in_value)

#def linear(in_value, coupling):
#    return(coupling * in_value)

# Define the connections that a node makes. 
# AddOutConnection automatically also creats an AddInConnection 
# call on the recieving node
# The below defines a simple network such that X->B->Y 
# such that initially defining the value of X propagates through 
# to define the values
# of B and y.
X.add_out_connection(B, (0.5, quadratic))
# B .AddInConnection(X,0.5)
B.add_out_connection(Y, (0.5, linear))
# Y.AddInConnection(B,0.5)

# X.PrintNodeData()
# B.PrintNodeData()
# Y.PrintNodeData()
# X.PrintNodeData()

# defining the node list in the order of influence, X->B->Y means that the
# network values with be consistent after one evaluation of the network.
node_list = [X, B, Y]
network = NetworkInstance(node_list)
print("network instance defined: X B Y , quadratic, linear")


network.evaluate_network()
network.converge_network()
network_dataframe = network.make_network_dataframe()
print(network_dataframe)
#network_dataframe.to_csv("NetworkParameters.csv", index=False, na_rep='None')


'''
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

# node_list = [A, C, B, X, Y]:  giving nodes in this order leads to
# convergence in the first iteration, since a node is only visited
# once the nodes on which it is dependent has been visited. 
# Any other order is a suboptimal order but network converges for this
# topology on second pass.
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
'''
