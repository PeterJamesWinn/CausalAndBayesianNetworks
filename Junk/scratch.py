
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


filename="DataSetOverValues"
filepointer = open(filename, "w")



#network_dataframe = pd.DataFrame(columns=node_list)
# break code block as a procdure/method to set column names?
column_names = []
for node_entry in network.network_node_list:
    column_names.append(node_entry.name)
    print(column_names)

# block to iterate through values of X and write converged network 
# values to file. 
# can this be generalised as a method of the network?
data_list = []
for value_of_X in [1, 2, 3]:
    X.set_bias(value_of_X)
    network.evaluate_network()
    network.converge_network()
    # write converged network to data_list 
    data_list_row = []
    for node in network.network_node_list:
        data_list_row.append(node.node_value)
        #print(data_list_row)
    data_list.append(data_list_row)
    #print(data_list)
    data_list_row = []
    
network_dataframe = pd.DataFrame(data_list, columns=column_names)
print(network_dataframe)   

#def add_gaussian_noise(value, standard_deviation):
#    import random
#    random.gauss(value, standard_deviation)


