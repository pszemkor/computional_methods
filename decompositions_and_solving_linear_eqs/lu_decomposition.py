import scipy
import numpy as np
import scipy.linalg
import time

def LU_decomposition(matrix):
    rows = len(matrix)
    L = np.zeros((rows, rows))
    for i in range(rows):
        for j in range(i + 1, rows):
            L[j, i] = (matrix[j, i] / matrix[i, i])
            matrix[j] = matrix[j] - (matrix[j, i] / matrix[i, i]) * matrix[i]
            matrix[j, i] = 0
    for i in range(rows):
        L[i, i] = 1
    return L, matrix  # matrix is U now


# A = scipy.array([[7, 3, -1, 2], [3, 8, 1, -4], [-1, 1, 4, -1], [2, -4, -1, 6]])

A = np.random.rand(500, 500)
start = time.time()
L1, U1 = LU_decomposition(A)
end = time.time()
print("moja implementacja LU: ",end-start)
start1= time.time()
P, L, U = scipy.linalg.lu(A)
end1 = time.time()
print("implementacja scipy: ", end1 - start1)
print(np.matmul(P,L))

