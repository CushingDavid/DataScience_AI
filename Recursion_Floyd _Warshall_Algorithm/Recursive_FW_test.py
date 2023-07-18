# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 21:12:42 2022

@author: David
"""
import numpy as np

# Number of vertices in the graph
# Define infinity as the large enough value. 
# This value will be used for vertices not connected to each other
INF = 99999
# User input for the number of nodes in the test. 
V = int(input('Enter the number of nodes to test (4-7): '))
if V==4:
    # 4 noded graph - all paths are 1-way. Different weights
    graph= np.array([[0, 5, INF, 10], [INF, 0, 3, INF], [INF, INF, 0, 1], 
                     [INF, INF, INF, 0]])
elif V==5:
    # 5 noded graph - all paths are 1-way except one. 
    graph= np.array([[0, 2, INF, INF, INF], [INF, 0, 6, INF, INF], 
                     [INF, 7, 0, INF, INF], [INF, INF, 1, 0, 3],
                     [1, 4, INF, INF, 0]])
elif V==6:
    # 6 noded graph - all paths are 2-way but different weights in each direction
    graph= np.array([[0, INF, 9, INF, 7, INF], [INF, 0, 6, 5, INF, INF],
                    [10, 5, 0, INF, INF, INF], [0, 6, INF, 0, 4, 0],
                    [8, INF, INF, 2, 0, 4], [INF, INF, INF, 6, 5, 0]])
elif V==7:
    # 7 noded graph - all paths are 2-way and equally weighted in each direction
    graph= np.array([[0, 3, 10, INF, INF, 1, INF], [3, 0, 6, 1, INF, INF, INF],
                     [10, 6, 0, 1, INF, INF, INF], [INF, 1, 1, 0, 1, INF, 4],
                     [INF, INF, INF, 1, 0, INF, INF], [1, INF, INF, INF, INF, 0, 1],
                     [INF, INF, INF, 4, INF, 1, 0]])
# Additional test arrays may be added here ...
else:
    print('Please choose option 4,5,6 or 7')

#i and j are mapped onto the different vertices from 0 to V-1
dist = list(map(lambda i: list(map(lambda j: j, i)), graph))
#print(dist)

#recursive function will return the minimum distance  
def fw_recur(i, j, k):
    ''' Recursive function returns the original value from the 
    distance 2D-array if k is less than zero, or it returns 
    the minimum value of the distance between two nodes. 
    The distance in the 2D-array is compaired to the distance via
    a secondary node. 
    '''
    if k<0 :
        #print(dist[i][j])
        return dist[i][j]
    else:
        #print(min(fw_recur(i, j, k-1), 
                        #fw_recur(i, k, k-1) + fw_recur(k, j, k-1)))
        return min(fw_recur(i, j, k-1), 
                        fw_recur(i, k, k-1) + fw_recur(k, j, k-1))
    
def matrix_fill(dist):     
    ''' This function loops through all the values between 0 -> V
    for each of i, j and k. It updates the dist array using the 
    recursive function fw_recur. 
    '''
    for k in range(V):
        #print(k)
        #print(np.array(dist))
        for i in range(V):
            for j in range(V):
                dist[i][j] = fw_recur(i, j, k)
    return dist

# Apply the function on the chosen 2D-array  
matrix_fill(dist)
# Ouput the end result as a numpy array 
graph_end= np.array(dist)
# Screen output of the original and final matrices for comparison: 
print("")
print('The original weighted graph matrix was:')
print(graph)
print("")
print('The final minimum-path weighted graph matrix was:')
print(graph_end)
    
#End

      
                  
