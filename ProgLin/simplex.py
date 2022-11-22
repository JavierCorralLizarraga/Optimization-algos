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
 
def pivoteo(M, row, column):
    M = np.array(M, dtype = float)
    if M[row, column] != 1:
        M = multRow(M, row, 1/M[row, column])
    a = list(enumerate(M))
    a.pop(row)
    for ind, i in a:
        #print(ind, i)
        M = addRow(M, row, ind, -i[column])
    return M

def isOptimal(tbl):
    if np.all(tbl[-1][:-1] >=0):
        return True
    else:
        return False
    
def findPivotVariable(tbl):
    coefs = tbl[-1][:-1]
    minNegCoef =  min(coefs[:-1])
    index = np.where(coefs == minNegCoef)
    print(index)
    index = np.array(index).flat[0]
    a = tbl[:,index][:-1] # columna 
    b = tbl[:,-1][:-1]
    ratios = []
    for i,j in zip(a,b):
        ratios.append(j/i)
    ratios = np.array(ratios)
    if np.any(ratios > 0):
        m = min(ratios)
        index2 = np.where(ratios == m)
        #print(np.array(index2).flat[0])
        return tbl[index, index2].flat[0], np.array(index2).flat[0], index
    else:
        return "unbounded", 0,0 

def simplex(tbl):
    #tbl = canonica(obj, rest)
    tbl = np.array(tbl, dtype = float)
    print(tbl)
    count=0
    while not isOptimal(tbl):
        pv, row, column = findPivotVariable(tbl)
        if pv == "unbounded":
            return "unbounded"
        tbl = pivoteo(tbl, row, column)
        if count == 0:
            break
        count+=1
    return tbl
        
def canonica(A, b, c):
    A = np.array(A)
    A = np.hstack((A, np.identity(len(A))))
    tbl = np.hstack((A, np.array(b)[:,np.newaxis]))
    z = coef + list(np.zeros(len(A))) + [0]
    tbl = np.vstack((tbl, z))
    return tbl.astype(float)

def matrixForm(preA, preb, prec):
    pass

def main():
    #probs = ['problema_A', 'problema_B', 'problema_C']
    #for i in probs:
    #    with open(i, 'r') as file:
    #        print(file.read())
    with open('problema_A', 'r') as file:
       prob = file.read().split("\n")
       sa = prob.index('sa') ; var = prob.index('vars')
       print(sa, var)
       prec = prob[2]
       preA = prob[3]
       preb = ''
     
    print(preA, preb, prec)
       
    #PPL1 = [A, b, c]
    #tbl = canonica(*PPL1)
    
    #print(sol := simplex(tbl))
    #print('a')
if __name__=="__main__":
    main()