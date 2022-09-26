# -*- coding: utf-8 -*-
import re
import numpy as np
from GaussJordan import GaussJordanElimination
#%% parametros
# funcion objetivo
obj = "-2x-3y-3z"
# arreglo de restricciones (asumimos que todas las variables son mayores a 0)
rest = [
    "3x + 2y + z <= 10",
    "2x + 5y + 3z <= 15"
    ]
#%%
def canonica(obj, rest):
    # construimos forma canonica (estandar)
    # coeficientes
    coef = re.split("[A-Za-z]", obj)[:-1]
    coef = [int(i) for i in coef]
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

#%% checa si es solucion optima
def isOptimal(tbl):
    if np.all(tbl[-1][:-1] >=0):
        return True
    else:
        return False
#%%
def isUnbounded():
    pass
#%% 
def findPivotVariable(tbl):
    coefs = tbl[-1][:-1]
    minNegCoef =  min(coefs)
    index = np.where(coefs == minNegCoef)
    index = np.array(index).flat[0]
    a = tbl[:,index][:-1] # columna 
    b = tbl[:,-1][:-1]
    c = []
    for i,j in zip(a,b):
        c.append(j/i)
    c = np.array(c)
    #if np.any(c >= 0)):
    m = min(c)
    index2 = np.where(c == m)
    return tbl[index, index2].flat[0]
    
#%% 

# declaracion de la funcion (posterior)
def simplex(obj, rest):
    tbl = canonica(obj, rest)
    print(tbl)
    #while not isOptimal(tbl):
        #pass
    #Unbounded():
        #return "unbounded"
    pv = findPivotVariable(tbl)
    return tbl[-1][-1]
        
    #a = GaussJordanElimination(tbl)
    #return a
    #if not is_sbfo():
      #  return no acotado
    #if is_sbfo():
     #   return "no acotado "
        
# solucionamos
print(simplex(obj, rest))
