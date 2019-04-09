import numpy as np
import time
 
 
def gauss_jordan(a, b):
    matrix = np.hstack([a, b.reshape(-1, 1)])
    rows = len(matrix)
    for i in range(rows):
        max_value = matrix[i, i]
        max_ind = i
        for j in range(i + 1, rows):
            if max_value < matrix[i, j]:
                max_value = abs(matrix[i, j])
                max_ind = j
        matrix[[i, max_ind]] = matrix[[max_ind, i]]
        for j in range(i + 1, rows):
            matrix[j] = matrix[j] - (matrix[j, i] / matrix[i, i]) * matrix[i]
            matrix[j, i] = 0
        for j in range(0, i):
            matrix[j] = matrix[j] - (matrix[j, i] / matrix[i, i]) * matrix[i]
            matrix[j, i] = 0
        matrix[i] = matrix[i] / matrix[i, i]
    return matrix[:, rows]
 
 
# preparing matrices
m = np.array(np.random.rand(300, 300))
bm = np.array(np.random.rand(300))
 
start = time.time()
my_result = gauss_jordan(m, bm)
end = time.time()
print("my implementation: ")
print(end - start)
 
start = time.time()
lib_result = np.linalg.solve(m, bm)
end = time.time()
print("lib: ")
print(end - start)
 
print("*****************************************************************************")
print(my_result)
print("*****************************************************************************")
print(lib_result)