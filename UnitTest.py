
import unittest
from network_generator import *
import sys


verbosity_level=2

class SetUp(unittest.TestCase):
    def setUp(self):
        self.X = Node("X", 5)
        self.B = Node("B")
        self.Y = Node("Y")
        self.X.add_out_connection(self.B, 0.5)
        self.B.add_out_connection(self.Y, 0.5)
        self.node_list = [self.X, self.B, self.Y]
        self.network = NetworkInstance(self.node_list)


class TestNetworkCreation(SetUp):
    def test_node_assignment(self):
        self.assertEqual(self.X.node_value, 5)
        self.assertEqual(self.X.name, "X")
        self.assertEqual(self.X.node_bias, 5)
        
        self.assertEqual(self.B.node_value, 0)
        self.assertEqual(self.B.name, "B")
        self.assertEqual(self.B.node_bias, 0)
        
    def test_network_connections(self):
        self.assertEqual(self.B.out_connections[self.Y],0.5)
        self.assertEqual(self.Y.in_connections[self.B],0.5)
    
    def test_network_instance(self):
        self.assertEqual(self.network.network_node_list[0],self.X)
        self.assertEqual(self.network.network_node_list[1],self.B)
        self.assertEqual(self.network.network_node_list[2],self.Y)
        
        self.assertEqual(self.network.network_node_list[0].node_value,5)
        self.assertEqual(self.network.network_node_list[1].node_value,0)


class TestSettingNodeValues(SetUp):
    def setUp(self): # takes initialisation of network from class SetUp  
        super().setUp()
        self.X.set_value(15)  # should change value but not bias
        self.B.set_previous_value(5)
        self.Y.set_bias(25)   # should change bias but not value
       
    def test_set_value(self):
        self.assertEqual(self.X.node_value,15)
        self.assertEqual(self.X.node_bias,5)
     
    def test_set_previous_value(self):
        self.assertEqual(self.X.node_previous_value,5)
        self.assertEqual(self.B.node_previous_value,5)
        self.assertEqual(self.Y.node_previous_value,0)

    def test_set_bias(self):
        self.assertEqual(self.Y.node_bias,25)
        self.assertEqual(self.X.node_previous_value,5)

    def test_print_node_data(self):
        # print data to file and compare to reference.
        file_pointer = open('temp.txt','w')
        sys.stdout = file_pointer
        self.B.print_node_data() # this just checks the code runs 
                                 # without error. 
        file_pointer.close()
        # compare data with a standard file.
        file_pointer = open('check_print_node_data.txt','r')
        lines = file_pointer.readlines()
        file_pointer2 = open('temp.txt','r')
        lines2 = file_pointer2.readlines()
        self.assertEqual(lines, lines2)



for test_case in [TestNetworkCreation, TestSettingNodeValues]:
    suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
    unittest.TextTestRunner(verbosity=verbosity_level).run(suite)




'''
class TestNetworkConvergence(unittest.TestCase):
    def setUp(self):
        self.X = Node("X", 5)
        self.B = Node("B")
        self.Y = Node("Y")
        self.X.add_out_connection(self.B, 0.5)
        self.B.add_out_connection(self.Y, 0.5)
        self.node_list = [self.X, self.B, self.Y]
        self.network = NetworkInstance(self.node_list)
        network.evaluate_network()
        network.converge_network()
        network_dataframe = network.make_network_dataframe()


        X 5
B 0
Y 0
X 5
B 2.5
Y 1.25
  NodeName  CurrentValue InComingConnectionFromNodes  InComingValues
0        X          5.00                        None             NaN
1        B          2.50                           X             0.5
2        Y          1.25                           B             0.5 
'''       





