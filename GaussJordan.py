# -*- coding: utf-8 -*-

import numpy as np

def swapRow(M, row1, row2):
    M[[row1, row2]] = M[[row2, row1]]
    return M
    
def multRow(M, row, factor):
    M[row,:] = M[row,:] * factor
    return M
    
def addRow(M, row1, row2, factor):
     M[row2,:] = M[row2,:] + multRow(M.copy(), row1, factor)[row1, :]
     return M

def GaussJordanElimination(M):
    for ind, i in enumerate(np.transpose(M)):
        if ind < len(M):
            if 1 in i or -1 in i:
                if 1 in i: 
                    index = np.where( i == 1 )[0][0]
                    if not  index == ind:
                        M = swapRow(M, ind, index)
                elif -1 in i:
                    index = np.where(i == -1)[0][0]
                    M = multRow(M, index, -1)    
                    if not index == ind:
                        M = swapRow(M, ind, index)
                p = i[ind+1:]
                for jnd, j in enumerate(p):
                    M = addRow(M, ind, jnd+ind+1, -j)
            else:
                M = multRow(M, ind, 1/i[ind])
                p = i[ind+1:]
                for jnd, j in enumerate(p):
                    M = addRow(M, ind, jnd+ind+1, -j)
    return M
        
    
m = np.array([[5, 4, 5, 12], 
              [-1, 8, 9, 0],
              [1, 7, 11, 19]], dtype = float)
   
a=GaussJordanElimination(m)
print(a)

         