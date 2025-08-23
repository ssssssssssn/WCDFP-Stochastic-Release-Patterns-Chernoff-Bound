import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import math
import random
from decimal import Decimal


'''
 @method Generate a task set
 @param T_samples: Range of possible minimum values of PMIT
 @param Usum: Total utilization
 @param Ntask: Number of tasks per taskset
 @param cut_t: number of possible values in PMIT distribution
 @param cut_c: number of possible values in PWCET distribution
'''
def generate_simp_norestrictofTmaxandTmin_ceil(T_samples, Usum, Ntask, cut_t, cut_c):
    T = []
    U = []
    C = []

    # generate P_t
    p_t = round(1 / cut_t, 5)

    # generate T
    P = []
    for i in range(1, cut_t):
        P.append(1.5 ** (cut_t - i - 1) / 100)
    P = [1 - sum(P)] + P

    for i in range(0, Ntask):
        tmin = random.choice(T_samples)  # μ-3σ
        Tall = []
        for j in range(0, cut_t - 1):
            tpiece = tmin + round(1 / (cut_t - 1), 5) * j * tmin
            Tall.append([math.ceil(tpiece), P[cut_t - 1 - j]])
        p = round(1 - (cut_t - 1) * p_t, 5)
        Tall.append([math.ceil(tmin * 2), P[0]])
        Tall = deWeight(Tall)
        Tall.sort()
        T.append(Tall)

    T.sort()
    # generate P_c
    p_c = round(1 / cut_c, 5)

    # generate U
    Uc = Usum
    Utemp = []
    for i in range(1, Ntask):
        Unc = Uc * random.uniform(0, 1) ** (1 / (Ntask - i))
        Utemp.append(Uc - Unc)
        Uc = Unc

    Utemp.append(Uc)

    for uuu in Utemp:
        umin = uuu
        Uall = []
        for j in range(0, cut_c - 1):
            upiece = umin + j * round(1 / (cut_c - 1), 5) * umin
            Uall.append([upiece, P[j]])
        Uall.append([uuu + umin, P[j + 1]])  # 2 uuu
        Uall.sort()
        U.append(Uall)

    # generate C
    for i in range(0, Ntask):
        Call = []
        for j in range(0, cut_c - 1):
            Call.append([round(T[i][0][0] * U[i][j][0], 5), P[j]])
        Call.append([round(T[i][0][0] * U[i][cut_c - 1][0], 5), P[j + 1]])
        C.append(Call)

    return T, C, U

'''
@method: merge the same values in PMIT distribution
@param data: List of PMIT, PWCET, and utilization
@return result_dec: merged PMIT, PWCET, and utilization
'''
def deWeight(data):
    merged_dec = {}
    for number, prob in data:
        dec_prob = Decimal(str(prob))
        merged_dec[number] = merged_dec.get(number, Decimal('0')) + dec_prob

    result_dec = [[k, float(v.normalize())] for k, v in merged_dec.items()]

    return result_dec

'''
@method Generates a task set and saves it to a file
@param Usum: Total utilization
@param Ntask: Number of tasks per task set
@param cut_t: number of possible values in PWCET or PMIT distribution
@param GroupNumber: Number of task sets
'''
def generate(Usum, Ntask, cut, GroupNumber):
    T_samples = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    taskset_bath_path = '../tasksets/taskset1'
    cut_t = cut
    cut_c = cut

    filename = f'{Usum}u_{Ntask}n_{cut_t}cut_t_{cut_c}cut_c_{GroupNumber}turns'
    input_filename = f'{taskset_bath_path}/{filename}_input.txt'

    first_iteration = True
    for i in range(GroupNumber):
        T, C, U = generate_simp_norestrictofTmaxandTmin_ceil(T_samples, Usum, Ntask, cut_t, cut_c)

        mode = 'w' if first_iteration else 'a'
        with open(input_filename,mode) as file:
            file.write(f'T={T}\nC={C}\n\n')
        first_iteration = False

if __name__ == '__main__':

    # N experiment
    generate(0.7, 5, 3, 50)
    generate(0.7, 10, 3, 50)
    generate(0.7, 15, 3, 50)
    generate(0.7, 20, 3, 50)
    generate(0.7, 25, 3, 50)
    generate(0.7, 30, 3, 50)

    # U experiment
    generate(0.5, 10, 3, 50)
    generate(0.6, 10, 3, 50)
    # generate(0.7, 10, 3, 50) # default
    generate(0.8, 10, 3, 50)
    generate(0.9, 10, 3, 50)

    # cut experiment
    generate(0.7, 10, 2, 50)
    # generate(0.7, 10, 3, 50) #default
    generate(0.7, 10, 5, 50)
    generate(0.7, 10, 7, 50)
    generate(0.7, 10, 9, 50)

