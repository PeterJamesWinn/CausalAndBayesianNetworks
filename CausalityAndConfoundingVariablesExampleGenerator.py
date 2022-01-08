# Style conventions used
# Class and Method names use CamelNotation
# Instances/Variable names use underscore_notation


class Node:
    def __init__(self,value=0):
        self.NodeValue = [value]
        self.OutConnections = {}
        self.InConnections = {}

    def AddOutConnection(self,node,coupling):
        self.OutConnections[node]=coupling 
        # Needs to add an in connection to the receiving node
        node.InConnections[self]=coupling

    def AddInConnection(self,node,coupling):
        self.InConnectionns[node]=coupling
        # Needs to add an out connection to the giving node 
        # - it is inefficient to write in and out arrows explicitly, since it duplicates, but should make user experience easier
        node.OutConnections[self]=coupling

    def PrintNodeData(self):
        #print(self)
        print("value ")
        print(self.NodeValue)
        print("Out connections ")
        print(self.OutConnections.keys())
        print("Out connections ")
        print(self.InConnections.keys())



class CreateNetworkInstance:
    def __init__(self, node_list):
        self.node_list = node_list
    
    def EvaluateNetwork(self):
        for node in node_list:
            node.PrintNodeData()

X = Node(5)
B = Node()
Y = Node()
X.AddOutConnection(B, 0.5)
B.AddOutConnection(Y, 0.5)



node_list = [X, B, Y]
B.PrintNodeData()

network = CreateNetworkInstance(node_list)
network.EvaluateNetwork()