# -*- coding: utf-8 -*-
import numpy as np

def swapRow(M, row1, row2): # operacion elemental de intercambiar renglones
    M[[row1, row2]] = M[[row2, row1]]
    return M
    
def multRow(M, row, factor): # operacion elemental de multiplicar renglones por una constante
    M[row,:] = M[row,:] * factor
    return M
    
def addRow(M, row1, row2, factor): # operacion elemental de sumar un multiplo de un renglon a otro
     M[row2,:] = M[row2,:] + multRow(M.copy(), row1, factor)[row1, :]
     return M
 
def pivoteo(M, row, column): # se pivotea un renglon y una columna de la matriz 
    M = np.array(M, dtype = float)
    if M[row, column] != 1:
        M = multRow(M, row, 1/M[row, column])
    _ = list(enumerate(M)); _.pop(row)
    for ind, i in _:
        M = addRow(M, row, ind, -i[column])
    return M

def convertGranM(A, M): # le agrega a nuestro tableo una identidad con coeficientes asociados de M
    numRestr = A.shape[0]-1
    return np.hstack((A, np.vstack((np.identity(numRestr), np.ones(numRestr)*M))))

def isOptimal(tbl): # checa si es optima la solucion basica factible
    return True if np.all(tbl[-1][:-1] >=0) else False # si todos los coeficientes son no negativos
    
def canonica(A, b, c): # tomamos nuestras matrices y arreglos creamos un tableo
    A = np.array(A)
    tbl = np.hstack((A, np.array(b)[:,np.newaxis]))
    z = c + [0]
    tbl = np.vstack((tbl, z))
    return tbl.astype(float)

def solIsEmpty(tbl, auxVars):
    return np.any(tbl[-1][-auxVars:] >= 0) # si alguna de los coeficientes de las vars auxiliares es positivo

def findPivotVariable(tbl): # encuentra la variable que sera pivoteada a continuacion
    coefs = tbl[-1][:-1]
    minNegCoef =  min(coefs[:-1]) # encuentra el coeficiente mas negativo por regla de Bland
    index = np.where(coefs == minNegCoef)
    index = np.array(index).flat[0]
    a = tbl[:,index][:-1]
    b = tbl[:,-1][:-1]
    ratios = [] # arreglo para acumular los ratios
    for i,j in zip(a,b):
        if i != 0:
            ratios.append(j/i) # calculamos los ratios
        else:
            ratios.append(0)
    ratios = np.array(ratios)
    if np.any(ratios > 0): # si encontramos ratios positivos
        m = min([i for i in ratios if i > 0]) # tomamos el minimo
        index2 = np.where(ratios == m) # encontramos en que renglon esta
        row = index
        column = np.array(index2).flat[0]
        value = tbl[column, row].flat[0]
        return value, row, column # regresamos el valor de la variable pivote, su renglon y su columna
    else:
        return "unbounded", 0,0 
 
def simplex(A, b, c, M):
    tbl = canonica(A, b, c)
    print('la matriz original se ve asi:')
    print(tbl)
    # A = np.transpose(np.transpose(tbl)[:-1])
    # A = convertGranM(A, M) # agrega las vars auxiliares para aplicar el metodo de la gran M
    # b = np.transpose(tbl)[-1].reshape(-1, 1)
    # tbl = np.hstack((A,b))
    # print(tbl)
    # print('la matriz con las variables auxiliares para aplicar el metodo de la gran M se ve asi:')
    # print(tbl)
    #print(tbl)
    count = 0
    while True: # iteramos un rato
        if isOptimal(tbl): break # rompemos si es optimo
        print('la matriz no es optima, asi que pivotearemos')
        pv, column, row = findPivotVariable(tbl) # encontramos la variable pivote
        print('el valor del pivote es: ' + str(pv) + ' con columna: ' + str(column+1) + ' y renglon: ' + str(row+1))
        if pv == "unbounded": return "unbounded" # rompemos si es un problema no acotado
        tbl = pivoteo(tbl, row, column) # pivoteamos sobre la variable pivote
        print(tbl)
        count = count+1
        #if count == 2:
        #    break
    return 'a'
    #return tbl if solIsEmpty(tbl, auxVars) else "the solution space is empty"
        
def main():
    A = [
        [0,5,50,1,1,0],
        [1,-15,2,0,0,0],
        [0,1,1,0,1,1]
        ]
    b = [10,2,6]
    c = [0,-9,-1,0,2,1]
    #out = ''
    simplex(A, b, c, 100)
    #print(tbl)

if __name__=="__main__": main() # lo que se corre