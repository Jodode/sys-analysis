import numpy as np
from math import log2

def calculate_enthropy(probs):
    enthropy = 0

    for prob in np.nditer(probs):
        enthropy -= prob * log2(prob)

    return enthropy

def direct_entropy(mat):
    return calculate_enthropy(mat)

def sum_entropy(mat):
    h_y = calculate_enthropy(mat.sum(axis=1))
    h_x = calculate_enthropy(mat.sum(axis=0))

    mat_copy = np.copy(mat)
    overall_conditional_H = 0

    for row_index in range(len(mat)):
        mat_copy[row_index] /= mat.sum(axis=1)[row_index]
        conditional_H = calculate_enthropy(mat_copy[row_index])    
        overall_conditional_H += conditional_H * mat.sum(axis=1)[row_index]

    return h_x - overall_conditional_H, h_y + overall_conditional_H

def main(in_mat):
    initial_matrix = np.array(in_mat)

    amount_of_purchases = initial_matrix.sum()

    compatible_event_prob_matrix = initial_matrix / amount_of_purchases
    
    H_XY = direct_entropy(compatible_event_prob_matrix)

    I, H_XY_through_sum = sum_entropy(compatible_event_prob_matrix)

    print(f"Количество информации I(X,Y): {round(I, 2)}")
    print(f"Энтропия совместного события H(XY): {round(H_XY, 2)} (прямой расчет)")
    print(f"Энтропия совместного события H(XY): {round(H_XY_through_sum, 2)} (через сумму)")


if __name__ == '__main__':
    test = [[20, 15, 10, 5],
            [30, 20, 15, 10],
            [25, 25, 20, 15],
            [20, 20, 25, 20],
            [15, 15, 30, 25]]

    main(test)