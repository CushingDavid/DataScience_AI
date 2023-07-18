# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 21:12:42 2022

@author: David
"""
import numpy as np
import guppy
from guppy import hpy

heap = hpy()

print("Heap Status At Starting : ")
heap_status1 = heap.heap()
print("Heap Size : ", heap_status1.size, " bytes\n")
print(heap_status1)

heap.setref()

print("\nHeap Status After Setting Reference Point : ")
heap_status2 = heap.heap()
print("Heap Size : ", heap_status2.size, " bytes\n")
print(heap_status2)

#Stripped down code for benchmarking
V = 4

INF = 99999
# Test martix with 4 vertices:
graph= np.array([[0, 5, INF, 10], [INF, 0, 3, INF], [INF, INF, 0, 1], [INF, INF, INF, 0]])

dist = list(map(lambda i: list(map(lambda j: j, i)), graph))

def fw_recur(i, j, k):
    if k<0 :
        #print(dist[i][j])
        return dist[i][j]
    else:
        return min(fw_recur(i, j, k-1), 
                        fw_recur(i, k, k-1) + fw_recur(k, j, k-1))
    
def matrix_fill(dist):     
    V=4
    for k in range(V):
        for i in range(V):
            for j in range(V):
                dist[i][j] = fw_recur(i, j, k)
    return dist


matrix_fill(dist)
graph_end= np.array(dist)

#print(graph)
print("")
print(graph_end)

print("\nHeap Status After Module : ")
heap_status3 = heap.heap()
print("Heap Size : ", heap_status3.size, " bytes\n")
print(heap_status3)

print("\nMemory Usage After Creation Of Objects : ",
       heap_status3.size - heap_status2.size, " bytes")
    


      
                  
