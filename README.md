# CausalAndBayesianNetworks

This code is the start of a project to generate causally linked nodes. I.e. nodes where the value of one node affects the value of another node, with the nodes creating a network. 
Different data values for the nodes can then be generated to produce a data set for investigating statistical confounding effects, the effects of conditioning on specific variables to mitigate confounding effects, and to better understand do calculus for causal inference (see e.g. Dana Mackenzie and Judea Pearl's Book of Why for an introduction to the field). 


The EvaluateNetwork() call has initially been written to give a node the value of the sum of all incoming nodes, but future 
iterations of the code would allow for more complex relationships. 

The code currently defines functions, classes and methods to generate networks, and has two simple networks as example networks
to test the code and exemplify its usage. 

The .csv files are the output from running the code. 
