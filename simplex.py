# -*- coding: utf-8 -*-
import re
import numpy as np

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
    tbl = np.hstack((np.array(A), np.array(b)[:,np.newaxis]))
    z = coef + [0]
    tbl = np.vstack((tbl, z))
    return tbl
#%% declaracion de la funcion (posterior)
def simplex(obj, rest):
    return canonica(obj, rest)
        
#%% solucionamos
print(simplex(obj, rest))
