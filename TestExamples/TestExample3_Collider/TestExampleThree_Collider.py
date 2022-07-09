
import pandas as pd
import sys, os
sys.path.append('..\\..\\') # to pick up network_generator.py
from network_generator import *
from scan_1D_of_network_add_noise import *
filestem = "ExampleThree_Collider"

## 1.  Define network and converge.
## 1.1 Define nodes and network.
## 1.2 Evaluate and converge network values.
## 1.3 Write network values.
## 2.  Scan multiple values of X and then add noise.
## 2.1 Scan values.
## 2.2 Write noise free values to file.
## 2.3 Add noise multiple times.
## 2.4 Write noisy values to file.

## 1.1a.  Define the nodes, their names and any initial values. Default value is 0
X = Node("X", 1)
B = Node("B", 5)
Y = Node("Y")

## 1.1b. Define the connections that a node makes. 
# add_out_connection automatically also creats an add_in_connection 
# call on the recieving node.
# The below defines a simple network such that X->B->Y 
# such that initially defining the value of X propagates through 
# to define the values of B and y.
X.add_out_connection(B, 0.5)
Y.add_out_connection(B, 0.3)
variable_to_scan = X
scan_range_lower = 1
scan_range_upper = 16

## 1.1c. defining the node list in the order of influence, X->B->Y means that the
# network values will be consistent after one evaluation of the network.
node_list = [X, B, Y]

## 1.3 to 2.4 - scanning and writing of the data. 
scan_1D_of_network_add_noise(node_list, variable_to_scan, scan_range_lower,
        scan_range_upper, filestem)
