# -*- coding: utf-8 -*-

import numpy as np
from GaussJordan import *
from utils import canonica, isOptimal, findPivotVariable

# Parametros
# minimizacion siempre
# funcion objetivo
obj = "-2x-3y-3z"
# arreglo de restricciones (asumimos que todas las variables son mayores a 0)
rest = [
    "3x + 2y + z <= 10",
    "2x + 5y + 3z <= 15"
    ]
#obj = "-8x - 10y -7"

#%%
# declaracion de la funcion (posterior)
def simplex(obj, rest):
    tbl = canonica(obj, rest)
    tbl = np.array(tbl, dtype = float)
    print(tbl)
    count=0
    while not isOptimal(tbl):
        pv, row, column = findPivotVariable(tbl)
        if pv == "unbounded":
            return "unbounded"
        tbl = pivoteo(tbl, row, column)
        if count == 5:
            break
        count+=1
    return tbl
        
# solucionamos
print(sol := simplex(obj, rest))
