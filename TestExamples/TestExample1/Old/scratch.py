
import sys, os
sys.path.append(os.getcwd())
sys.path.append('..\\')
sys.path.append('..\\..\\')
#sys.path.append('..\\..')
#sys.path.append('..\/..\/')
#print(sys.path)
print("CWD ...  ", os.getcwd())
os.chdir('..\\..\\')
print("CWD ...  ", os.getcwd())
#sys.path.append('..\\..\\..\\')
#sys.path.append("C:\\Users\\customer\\Documents\\GitHub\\CausalAndBayesianNetworks\\")
from network_generator import *