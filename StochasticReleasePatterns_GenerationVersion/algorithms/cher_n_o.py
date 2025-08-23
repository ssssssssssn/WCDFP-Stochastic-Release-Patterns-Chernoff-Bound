import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mpmath import mp
from scipy.optimize import minimize_scalar

'''
 @function of Theorem 3
 @param x: lambda in Theorem 3 to be optimized
 @param T: PMIT distribution
 @param C: PWECT distribution
 @param Ntask: Number of tasks per taskset
 @param t: t belongs to [0,T[Ntask - 1][0][0])
'''
def f2(x, Ntask, T, C, t):
    expr1 = 0
    for i in range(0, Ntask - 1):
        temp = 0
        e_c = 0
        #
        for j in range(0, len(C[i])):
            e_c += mp.exp(C[i][j][0] * x) * C[i][j][1]
        for l in range(0, len(T[i])):
            if t <= T[i][l][0]:
                temp += (e_c ** 2) * T[i][l][1]
            else:
                temp += (e_c ** (t / T[i][l][0] + 2)) * T[i][l][1]
        expr1 += mp.log(temp)
    # k
    temp = 0
    e_c = 0
    for j in range(0, len(C[-1])):
        e_c += mp.exp(C[-1][j][0] * x) * C[-1][j][1]
    temp += e_c
    expr1 += mp.log(temp)

    expr2 = x * t

    return expr1 - expr2


'''
 @Apply negative-value penalties to prevent the optimizer from assigning negative values to param x (i.e. lambda in Theorem 3)
'''
def g_for_optimization_2(x, Ntask, T, C, t):
    if x < 0:
        return float('inf')  # negative-value penalties
    return float(f2(x, Ntask, T, C, t))

'''
 @method theorem 3 in our paper
 @param T: PMIT distribution
 @param C: PWECT distribution
 @param Ntask: Number of tasks per taskset
 @param t: t belongs to [0,T[Ntask - 1][0][0])
'''
def chernoff_N_O_golden(T, C, Ntask, t):

    # bounded method
    # bounds = (0, 50)
    # result = minimize_scalar(g_for_optimization_2, args=(Ntask, T, C, t), bounds=bounds, method='bounded',
    #                          options={'xatol': 1e-2, 'maxiter': 50})

    # Golden-section search to find the optimized value of lambda in Theorem 3.
    result = minimize_scalar(g_for_optimization_2, args=(Ntask, T, C, t),
                             method='Golden',options={'xtol': 1e-2, 'maxiter': 50})
    x_optimal = result.x # the optimized lambda
    E_e_ax_n = 1

    # hp tasks

    for i in range(0, Ntask - 1):

        e_c = 0
        temp = 0

        for j in range(0, len(C[i])):
            e_c += mp.exp(C[i][j][0] * x_optimal) * C[i][j][1]
        for l in range(0, len(T[i])):
            if (t <= T[i][l][0]):
                temp += (e_c ** 2) * T[i][l][1]
            else:
                temp += (e_c ** (t / T[i][l][0] + 2)) * T[i][l][1]

        E_e_ax_n *= temp

    # task k
    e_c = 0
    temp = 0
    for j in range(0, len(C[-1])):
        e_c += mp.exp(C[-1][j][0] * x_optimal) * C[-1][j][1]

    temp += e_c

    E_e_ax_n *= temp

    P_chernoff = E_e_ax_n / mp.exp(x_optimal * t)

    return P_chernoff


