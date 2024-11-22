import numpy as np


def preliminary_matrix(mat):
    r = {}

    for i, row in enumerate(mat):
        if isinstance(row, list):
            for elem in row:
                r[elem] = i
        else:
            r[row] = i
    
    Y_a = []
    for i in range(1, len(r) + 1):
        row = []
        for key, _ in r.items():
            if r[key] >= r[i]:
                row.append(1)
            else:
                row.append(0)
        Y_a.append(row)

    return Y_a

def calculate_stat(A, B):
    A, B = np.array(A), np.array(B)
    AB = A * B
    AB_t = A.transpose() * B.transpose()
    K = np.logical_or(AB, AB_t)

    return K

def main(A, B):
    print(calculate_stat(preliminary_matrix(A), preliminary_matrix(B)))

if __name__ == '__main__':
    A = [1,
         [2,3],
         4,
         [5,6,7],
         8,
         9,
         10]
    B = [[1,2],
         [3,4,5,],
         6,
         7,
         9,
         [8,10]]
    main(A, B)
    