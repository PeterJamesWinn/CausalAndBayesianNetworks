# Style conventions used
# Class, Method names and object attributes use CamelNotation
# Simple Instances/Variable names use underscore_notation


class Node:
    def __init__(self, name, value=0):
        self.NodeValue = [value]
        self.Name = name
        self.OutConnections = {}
        self.InConnections = {}

    def AddOutConnection(self,node,coupling):
        self.OutConnections[node]=coupling 
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
        print("name")
        print(self.Name)
        print("value ")
        print(self.NodeValue)
        print("Out connections ")
        for connection in self.OutConnections.keys():
            print(connection.Name)
            print(self.OutConnections[connection])
        
        print("In connections ")
        for connection in self.InConnections.keys():
            print(connection.Name)
            print(self.InConnections[connection])



class CreateNetworkInstance:
    def __init__(self, node_list):
        self.node_list = node_list
    
    def EvaluateNetwork(self):
        for node in node_list:
            value = 0
            for in_connection in node.InConnections.keys():
                #print("in connection data")
                #print(in_connection.NodeValue)
                #print(node.InConnections[in_connection])
                value = value + in_connection.NodeValue * node.InConnections[in_connection] 

            
            node.SetValue(value)

    def PrintNetwork(self):
        for node in node_list:
            print(node.Name)
            node.PrintNodeData()
                  

X = Node("X", 5)
B = Node("B")
Y = Node("Y")
X.AddOutConnection(B, 0.5)
B.AddOutConnection(Y, 0.5)



node_list = [X, B, Y]
print("   ")
print(" Data for B")
B.PrintNodeData()
print("   ")

network = CreateNetworkInstance(node_list)
network.EvaluateNetwork()
network.PrintNetwork()