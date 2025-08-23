import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mpmath import mpf
'''
 @Convolution operation in Maxim et al. (RTSS 2013)
'''
def convolutionC(a, b):
    lena = len(a)
    lenb = len(b)
    result = []

    for i in range(0, lena):
        for j in range(0, lenb):
            result.append((round(a[i][0] + b[j][0], 6), mpf(a[i][1]) * mpf(b[j][1])))

    result.sort(key=lambda k: k[0], reverse=False)#convolution result
    result_dict = {}# state merge
    for a, b in result:
        if a in result_dict:
            result_dict[a] = result_dict[a] + b
        else:
            result_dict[a] = b
    result_list = [[x, v] for x, v in result_dict.items()]

    result_list.sort(reverse=False)
    return result_list

'''
 @Convolution operation in Maxim et al. (RTSS 2013)
'''
def convolutionT(a, b):
    lena = len(a)
    lenb = len(b)
    result = []
    for i in range(0, lena):
        for j in range(0, lenb):
            result.append((round(a[i][0] + b[j][0], 6), mpf(a[i][1]) * mpf(b[j][1])))

    result.sort(key=lambda k: k[0], reverse=False)#convolution result
    result_dict = {}# state merge
    for a, b in result:
        if a in result_dict:
            result_dict[a] = result_dict[a] + b
        else:
            result_dict[a] = b

    result_list = [[x, v] for x, v in result_dict.items()]

    result_list.sort(reverse=False)
    return result_list
