# -*- coding: utf-8 -*-

import re
import numpy as np

def canonica(obj, rest):
    # construimos forma canonica (estandar)
    # coeficientes
    coef = re.split("[A-Za-z]", obj)[:-1]
    print(coef)
    coef = [float(i) for i in coef]
    # vector b
    b = []
    for i in rest:
        b.append(re.sub( "[^0-9]" , "" , re.split("[A-Za-z]", i)[-1]))
    # matriz A
    A = []
    for i in rest:
        a = []
        for j in re.split("[A-Za-z]", i)[:-1]:
            a.append(re.sub( "[^0-9]" , "" , j))  
        A.append(a)

    for i in range(len(A)):
        #print(i)
        for j in range(len(A[0])):
            if A[i][j] == '':
                A[i][j] = 1
            else:
                A[i][j]= int(A[i][j])
    # tabla en forma 
    A = np.array(A)
    A = np.hstack((A, np.identity(len(A))))
    tbl = np.hstack((A, np.array(b)[:,np.newaxis]))
    z = coef + list(np.zeros(len(A))) + [0]
    tbl = np.vstack((tbl, z))
    return tbl.astype(float)

def isOptimal(tbl):
    if np.all(tbl[-1][:-1] >=0):
        return True
    else:
        return False
    
def findPivotVariable(tbl):
    coefs = tbl[-1][:-1]
    minNegCoef =  min(coefs[:-1])
    index = np.where(coefs == minNegCoef)
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
    