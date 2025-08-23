import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math

'''
 @method Resampling of response time 
 @param x: Given distribution
 @param cut: threshold
'''
def resample_C(X, cut):
    p = 0
    result = []
    q = math.ceil(len(X) / cut)
    for i in range(0, len(X)):
        p = p + X[i][1]
        if ((i + 1) % q == 0) or (i == (len(X) - 1)):
            result.append([X[i][0], p])
            p = 0

    return result

'''
 @method Resampling of accumulated PMIT
 @param x: Given distribution
 @param cut: threshold
'''
def resample_T(X, cut):
    p = 0
    result = []
    q = math.ceil(len(X) / cut)
    for i in range(0, len(X)):
        tmp = len(X) - i - 1
        p = p + X[tmp][1]
        if ((i + 1) % q == 0) or (i == len(X) - 1):
            result.append([X[tmp][0], p])
            p = 0
    result.sort(reverse=False)
    return result


'''
 @method Algorithm 2 Linear down-sampling of a discrete random variable F. Markovi´c et al. (ECRTS 2021)
 @param X: Given distribution
 @param cut: threshold
'''
def linear_downsample(X, cut):
    n = len(X)
    P_un = 1.0
    p_delta = P_un / cut
    p = 0.0
    sum_prob = 0.0
    X_prim = []

    for l in range(n):
        p += X[l][1]
        sum_prob += X[l][1]
        P_un -= X[l][1]

        if l == n - 1 or p >= p_delta:
            X_prim.append([X[l][0], sum_prob])
            sum_prob = 0.0
            cut -= 1
            p_delta = P_un / cut if cut > 0 else 0
            p = 0.0

    return X_prim