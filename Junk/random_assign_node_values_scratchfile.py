
import random as random

def set_node_parameters_random_real(self, list_of_node_range_tuples, seed):
    '''
    reassigns the nodes defined in list_of_node_range_tuples with random
    values. 

    uses python random module of the standard python package
    list_of_node_range_tuples is of the form 
    (node object, min value of node, max value)
    '''
        # 1. change node values
        for node_tuple in list_of_nodes:
            node_to_change = node_tuple[0] # node name is first of tuple
            random.seed(seed)
            value = random
            min = node[1]
            max = node[2]
            value = min + value*(max - min)
            node_to_change.set_bias(value)

def set_node_parameters_random_real(self, list_of_node_range_tuples, seed):
    '''
    reassigns the nodes defined in list_of_node_range_tuples with random
    real number value. 

    uses python random module of the standard python package
    list_of_node_range_tuples is of the form 
    (node object, min value of node, max value)
    '''
    for node_tuple in list_of_nodes:
        node_to_change = node_tuple[0] # node name is first of tuple
        random.seed(seed)
        value = random
        min = node[1]
        max = node[2]
        value = min + value*(max - min)
        node_to_change.set_bias(value)
        
def set_node_parameters_random_int(self, list_of_node_range_tuples, seed):
    '''
    reassigns the nodes defined in list_of_node_range_tuples with random
    integer number values. 

    uses python random module of the standard python package
    list_of_node_range_tuples is of the form 
    (node object, min value of node, max value)
    '''
    for node_tuple in list_of_nodes:
        node_to_change = node_tuple[0] # node name is first of tuple
        random.seed(seed)
        value = randint(node[1],node[2])
        min = node[1]
        max = node[2]
        node_to_change.set_bias(value)