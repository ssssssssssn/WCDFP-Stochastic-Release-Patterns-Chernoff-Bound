import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import copy
import numpy as np
from mpmath import mpf
from algorithms import resample
from algorithms.convolution import convolutionC, convolutionT


'''
 @Algorithm 1 in Maxim et al. (RTSS 2013) combining with down-sampling techniques in its matlab code.
 @param Ntask: Number of tasks
 @param T: PMIT 
 @param C: PWECT
 @param cov_len_C: Threshold for down-sampling the response time 
 @param cov_len_T: Threshold for down-sampling the PMIT
'''
def method_cov(Ntask, T, C, cov_len_C, cov_len_T):


    R = C[Ntask - 1]

    for i in range(0, Ntask - 1):
        R = convolutionC(R, C[i])
        if len(R) >= (cov_len_C * 2): #same as Sergey Bozhko et al. (RTSS 2021) Down-sampling is triggered when the number of values in the distribution reaches twice the threshold.
            R = resample.resample_C(R, cov_len_C)

    for i in range(0, Ntask - 1):  #As shown by Chen et al. (RTSS 2022), the original bound is not safe. To address this issue, we add a carry-in job for each higher-priority task, as discussed in our paper.
        R = convolutionC(R, C[i])
        if len(R) >= (cov_len_C * 2):
            R = resample.resample_C(R, cov_len_C)

    A = copy.deepcopy(T)

    stop_value = int(T[Ntask - 1][0][0])

    for i in np.arange(1, stop_value, 1):
        for j in range(0, Ntask - 1):
            if A[j][0][0] == int(i):
                R.sort()
                R = preempt(R, A[j], C[j])
                if len(R) >= (cov_len_C * 2):
                    R = resample.resample_C(R, cov_len_C)

                A[j] = convolutionT(A[j], T[j])
                if len(A[j]) >= (cov_len_T * 2):
                    A[j] = resample.resample_T(A[j], cov_len_T)


    R.sort()
    WCDFP = 0

    for i in range(0, len(R)):
        if R[len(R) - i - 1][0] > T[Ntask - 1][0][0]:
            WCDFP += R[len(R) - i - 1][1]
        else:
            break
    return WCDFP


'''
 @Algorithm 1 in Maxim et al. (RTSS 2013) combining with down-sampling techniques of Algorithm 2 in F. Markovi´c et al. (ECRTS 2021)
 @param Ntask: Number of tasks
 @param T: PMIT 
 @param C: PWECT
 @param cov_len_C: Threshold for down-sampling the response time 
 @param cov_len_T: Threshold for down-sampling the PMIT
'''
def method_cov_linear(Ntask, T, C, cov_len_C, cov_len_T):

    R = C[Ntask - 1]

    for i in range(0, Ntask - 1):
        R = convolutionC(R, C[i])
        if len(R) >= (cov_len_C * 2):#same as Sergey Bozhko et al. (RTSS 2021) Down-sampling is triggered when the number of values in the distribution reaches twice the threshold.
            R = resample.linear_downsample(R, cov_len_C)

    for i in range(0, Ntask - 1):  #As shown by Chen et al. (RTSS 2022), the original bound is not safe. To address this issue, we add a carry-in job for each higher-priority task, as discussed in our paper.
        R = convolutionC(R, C[i])
        if len(R) >= (cov_len_C * 2):
            R = resample.linear_downsample(R, cov_len_C)

    A = copy.deepcopy(T)

    stop_value = int(T[Ntask - 1][0][0])

    for i in np.arange(1, stop_value, 1):
        for j in range(0, Ntask - 1):
            if A[j][0][0] == int(i):
                R.sort()
                R = preempt(R, A[j], C[j])
                if len(R) >= (cov_len_C * 2):
                    R = resample.linear_downsample(R, cov_len_C)

                A[j] = convolutionT(A[j], T[j])
                if len(A[j]) >= (cov_len_T * 2):
                    A[j] = resample.resample_T(A[j], cov_len_T)


    R.sort()
    WCDFP = 0

    for i in range(0, len(R)):
        if R[len(R) - i - 1][0] > T[Ntask - 1][0][0]:
            WCDFP += R[len(R) - i - 1][1]
        else:
            break
    return WCDFP


'''
 @Algorithm 2 in Maxim et al. (RTSS 2013)
 @param R: Response time distribution
 @param A: accumulated PMIT (defined in Maxim et al. (RTSS 2013))
 @param C: PWCET
'''
def preempt(R, A, C):
    Rintermediary = []
    head = []
    tail = []
    for i in range(0, len(A)):
        Afake = [[0, A[i][1]]]
        for j in range(0, len(R)):
            if R[j][0] > A[i][0]:
                break
            elif j == len(R) - 1:
                j = len(R)

        head = copy.deepcopy(R[:j])
        tail = copy.deepcopy(R[j:])
        if len(tail) != 0:
            tail = convolutionC(tail, C)
        temp = head + tail

        for l in range(0, len(temp)):
            temp[l][1] *= (
                mpf(A[i][1]))

        Rintermediary += temp

    result_dict = {}
    for [a, b] in Rintermediary:
        if a in result_dict:
            result_dict[a] += b
        else:
            result_dict[a] = b

    result_list = [[x, v] for x, v in result_dict.items()]

    result_list.sort(reverse=False)
    return result_list

