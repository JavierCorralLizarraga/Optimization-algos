# -*- coding: utf-8 -*-
import numpy as np
np.set_printoptions(suppress=True)

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
    return np.hstack((A, np.vstack((np.identity(numRestr), np.ones(numRestr)*M)))), numRestr

def isOptimal(tbl): # checa si es optima la solucion basica factible
    # print("checa si es óptima:")
    return True if np.all(tbl[-1][:-1] >=0) else False # si todos los coeficientes son no negativos
    
def canonica(A, b, c): # tomamos nuestras matrices y arreglos creamos un tableo
    A = np.array(A)
    tbl = np.hstack((A, np.array(b)[:,np.newaxis]))
    z = c + [0]
    tbl = np.vstack((tbl, z))
    return tbl.astype(float)

def solIsEmpty(tbl, auxVars):
    # print(tbl[-1][-auxVars:], "shi")
    a = np.any(tbl[-1][-auxVars:] >= 0) # si alguna de los coeficientes de las vars auxiliares es positivo
    # print(a, 'asdasdasdsfasdfasdfa')
    return a

def findPivotVariable(tbl): # encuentra la variable que sera pivoteada a continuacion
    coefs = tbl[-1][:-1]
    # print(coefs)
    minNegCoef =  min(coefs) # encuentra el coeficiente mas negativo por regla de Bland
    # print(coefs[:-1])
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
        m = min([i for i in ratios if i > 0]) # tomamos el minimo POSITIVO
        index2 = np.where(ratios == m) # encontramos en que renglon esta
        row = index
        column = np.array(index2).flat[0]
        value = tbl[column, row].flat[0]
        return value, row, column # regresamos el valor de la variable pivote, su renglon y su columna
    else:
        return "unbounded", 0,0 

def basica(column): # determina si una columna es basica
    return sum(column) == 1 and len([c for c in column if c == 0]) == len(column) - 1

def sbfInterpret(tbl): # saca la sbf de la tabla optima
    columns = np.array(tbl).T
    sols = []
    for column in columns[:-1]:
        sol = 0
        if basica(column):
            one_index = column.tolist().index(1)
            sol = columns[-1][one_index]
        sols.append(sol)
    return sols

def getZ(tbl): # obtiene el valor optimo de la tabla optima
    return tbl.flat[-1]

def multSols(tbl): # determinar si hay multiples soluciones
    for column in tbl.T:
        if basica(column) and column[-1]==0: 
            return True
    return False
     
def simplex(A, b, c, M):
    x = len(A[0])
    tbl = canonica(A, b, c)
    print('La matriz original se ve así:')
    print(tbl)
    A = np.transpose(np.transpose(tbl)[:-1])
    A, auxVars = convertGranM(A, M) # agrega las vars auxiliares para aplicar el metodo de la gran M
    # print(auxVars, 'aaaa')
    b = np.transpose(tbl)[-1].reshape(-1, 1)
    tbl = np.hstack((A,b))
    # print('la matriz con las variables auxiliares para aplicar el metodo de la gran M se ve asi:')
    # print(tbl)
    y = len(tbl[0]) - 1
    for z in range(x,y):
        row2 = len(tbl) - 1
        row1 = z - x
        factor = -1 * M
        tbl[row2,:] = tbl[row2,:] + multRow(tbl.copy(), row1, factor )[row1, :]
    print('la matriz simplex inicial es:')
    print(tbl)
    count = 0
    while True: # iteramos un rato
        if isOptimal(tbl): break # rompemos si es optimo
        # print('la matriz no es optima, asi que pivotearemos')
        pv, column, row = findPivotVariable(tbl) # encontramos la variable pivote
        # print('el valor del pivote es: ' + str(pv) + ' con columna: ' + str(column+1) + ' y renglon: ' + str(row+1))
        if pv == "unbounded": return tbl, "unbounded" # rompemos si es un problema no acotado
        tbl = pivoteo(tbl, row, column) # pivoteamos sobre la variable pivote
        print('nuestra matriz pivoteada se ve asi: ')
        print(tbl)
    if not solIsEmpty(tbl, auxVars): return tbl, "the solution space is empty"
    if multSols(tbl):
        print("\n La matriz óptima es:")
        print(tbl)
        return tbl, "there are multiple solutions and one of them is the last one: "
    return tbl, 'esta es nuestra tabla optima'
        
def main():
    np.set_printoptions(linewidth=np.inf)
    A = [
        [1,0,0,0,1,0,0,0],
        [20,1,0,0,0,1,0,0],
        [200,20,1,0,0,0,1,0],
        [2000,200,20,1,0,0,0,1]
        ]
    b = [1,100,10000,1000000]
    c = [1000,100,10,1,0,0,0,0]
    print(np.array(c))
    tbl, comment = simplex(A, b, c, 100)
    print(comment)
    if comment == 'esta es nuestra tabla optima' or comment == "there are multiple solutions and one of them is the last one: ":
        print('\n y nuestra sbf se ve así: ')
        print(sbfInterpret(tbl))
        print('\n con valor de la función objetivo: ')
        print(-getZ(tbl))
        
if __name__=="__main__": main() # lo que se corre