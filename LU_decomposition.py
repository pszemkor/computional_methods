import numpy as np
 
 
def LU_decomposition(matrix):
    rows = len(matrix)
    L = np.zeros((rows, rows))
    for i in range(rows):
        for j in range(i + 1, rows):
            L[j,i] = (matrix[j, i] / matrix[i, i])
            matrix[j] = matrix[j] - (matrix[j, i] / matrix[i, i]) * matrix[i]
            matrix[j, i] = 0
    for i in range(rows):
        L[i,i] = 1
    return L, matrix #matrix is U now
 
 
A = np.array([[1.0, -3.0, 2.0], [1.0, 1.0, -2.0], [2.0, -1.0, 1.0]])
print(A)
b = np.array([3.0, 1.0, -1.0])
Ab = np.hstack([A, b.reshape(-1, 1)])
L, U = LU_decomposition(A)
print(np.matmul(L, U))