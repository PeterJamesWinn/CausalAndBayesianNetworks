

import numpy as np

test_array = np.array([[1.,2.,30.],[4.,5.,60.],[7.,8.,90.],[10.,11.,120.]])

print(test_array, np.square(test_array))

'''
print(array[:,2])
print(np.amax(array[:,1]))
print(np.amax(array[:,0]))
print(np.amax(array[:,2]))

print(len(array[:,0:]))

for column in array.T:
    print(column)
    #print(array[:,counter])
    print(column.T)
    print(np.amax(column))
'''

'''
print(test_array)
print(test_array.shape[1])
counter = 0 
while counter != test_array.shape[1]:
    temp = test_array[:,counter]
    #print(array[:,counter])
    print(temp)
    print(np.amax(temp))
    counter += 1

for counter in range(test_array.shape[1]):
    print(test_array[:,counter])
    print(np.amax(test_array[:,counter]))
'''

standard_deviation_scale = 0.1
data_array = test_array
print(data_array)
column_means = np.mean(data_array, axis=0)
print("means ", column_means)
standard_deviation = column_means * standard_deviation_scale
print("sd ", standard_deviation)
noise = np.random.normal(loc=0, 
        scale=standard_deviation, size= data_array.shape)
print("noise ", noise)
temp = data_array.copy() +  noise
print(temp)
data_array = data_array + noise.copy()
print(data_array)
'''
standard_deviation_base = 0.1
#data_array = np.array(data)
data_array = test_array
for column in range(data_array.shape[1]):
    print(data_array[:,column:column+1])
    print(np.amax(data_array[:,column:column+1]))
    column_max_value = np.amax(data_array[:,column:column+1])
    column_mean =np.mean(data_array[:,column:column+1])
    standard_deviation = standard_deviation_base * column_mean
    noise = np.random.normal(loc=0,scale=standard_deviation, size=(data_array.shape[0],1))
    print(noise)
    temp = data_array[:,column:column+1].copy() + noise
    print("temp ", temp)
    data_array[:,column:column+1] = temp.copy()
    print(data_array[:,column:column+1])
print(data_array)
'''