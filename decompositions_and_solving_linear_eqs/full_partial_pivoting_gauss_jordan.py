import numpy as np
import time


# partial pivoting
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


# full pivoting
def get_full_pivot(A):
    max_row = 0
    max_col = 0
    n = len(A)
    for i in range(n):
        for j in range(n):
            if abs(A[i, j]) > abs(A[max_row, max_col]):
                max_row, max_col = i, j
    return max_row, max_col


def gauss_jordan_v2_fp(A, B):
    matrix = np.hstack([A, B.reshape(-1, 1)])
    rows = len(matrix)
    P = [i for i in range(rows + 1)]

    max_row, max_col = get_full_pivot(matrix)
    max_val = abs(matrix[max_row, max_col])

    for i in range(rows):
        for j in range(rows + 1):
            matrix[i, j] = matrix[i, j] / max_val  # skalowanie

    for k in range(rows):
        # pivoting + zamiana kolumn
        max_row, max_col = get_full_pivot(matrix[k:rows, k:rows + 1])
        matrix[[k, max_row + k]] = matrix[[max_row + k, k]]
        matrix[:, [k, max_col + k]] = matrix[:, [max_col + k, k]]
        P[k], P[max_col + k] = P[max_col + k], P[k]

        for i in range(k + 1, rows):
            factor = matrix[i][k] / matrix[k][k]
            for j in range(k, rows + 1):
                matrix[i][j] = 0 if j == k else (matrix[i][j] - factor * matrix[k][j])
        for i in range(k):
            factor = matrix[i][k] / matrix[k][k]
            for j in range(k, rows + 1):
                matrix[i][j] = 0 if j == k else (matrix[i][j] - factor * matrix[k][j])

    for i in range(rows):
        factor = 1.0 / matrix[i][i]
        matrix[i][i] = 1.0
        matrix[i][rows] *= factor

    # uwzględnienie zamian w kolumnach
    for i in range(rows + 1):
        if P[i] != i:
            ind = P.index(i)
            matrix[i, rows], matrix[ind, rows] = matrix[ind, rows], matrix[i, rows]
            P[i], P[ind] = P[ind], P[i]

    return matrix[:, rows]

# preparing matrices
m = np.array(np.random.rand(500, 500))
bm = np.array(np.random.rand(500))

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

start = time.time()
res = gauss_jordan(m, bm)
end = time.time()
print("my implementation (full pivoting): ")
print(end - start)

# print("*****************************************************************************")
# print(my_result)
# print("*****************************************************************************")
# print(lib_result)

if np.allclose(lib_result, my_result) and np.allclose(lib_result, res):
    print("macierze są równe")
else:
    print("macierze nie są równe")