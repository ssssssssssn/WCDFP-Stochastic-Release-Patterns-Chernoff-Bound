import ast
import os
import time
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms import cher_n_o
from algorithms.cov import method_cov, method_cov_linear

'''
@method Reads a task file and parses the task collection
@param file_path: File path for reading task data
'''
def getAllTask(file_path):
    # Read the file
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    T_all = []  # Used to store all T
    C_all = []  # Used to store all C

    # Traverse every two lines
    for i in range(0, len(lines), 2):
        first_line = lines[i].strip() if i < len(lines) else None
        second_line = lines[i + 1].strip() if i + 1 < len(lines) else None

        # Parse T and C and store them separately
        if first_line.startswith('T='):
            T_all.append(ast.literal_eval(first_line[len('T='):]))

        if second_line.startswith('C='):
            C_all.append(ast.literal_eval(second_line[len('C='):]))

    return T_all, C_all


'''
@method Calculates the results for different analyse methods and saves them to a file.
@param Usum: Total utilization
@param Ntask: Number of tasks per set
@param cut: number of possible values in PMIT or PWCET
@param GroupNumber: Number of task sets
@param thresholdC: threshold for response time distribution
@param option: Selected algorithm  ('100': Run  throrem 3 in our paper, '010': Run  Maxim et al. (RTSS 2013), '001': Run  Maxim et al. (RTSS 2013) with down-sample in F. Markovi´c et al. (ECRTS 2021))
@param iftime: Whether to record computation time
@param taskset_bath_path: Task Set Directory
'''
def experiment(Usum, Ntask, cut,  GroupNumber, thresholdC, option, iftime,taskset_bath_path):
    print(f"Usum {Usum}\nNtask {Ntask}\ncut {cut}\nGroupNumber {GroupNumber}\nthresholdC {thresholdC}")
    cut_t = cut
    cut_c=  cut
    results_base_path = './results/result1'
    thresholdC = thresholdC
    thresholdT = 5
    # Read all tasks of the target file according to different parameter types
    filename = f'{Usum}u_{Ntask}n_{cut_t}cut_t_{cut_c}cut_c_{GroupNumber}turns'

    # Build the full file path
    input_filename = f'{taskset_bath_path}/{filename}_input.txt'
    if option == '100':
        method = 'CH_BND'
    elif option == '010':
        method = 'CV_D'
    elif option == '001':
        method = 'CV_L'

    res_filename = f'{results_base_path}/res/{filename}_{thresholdC}thresholdC_{method}_res.txt'
    time_filename = f'{results_base_path}/time/{filename}_{thresholdC}thresholdC_{method}_time.txt'

    if option == '100':
        res_filename = f'{results_base_path}/res/{filename}_{method}_res.txt'
        time_filename = f'{results_base_path}/time/{filename}_{method}_time.txt'

    # Make sure the target directory exists, create it if it doesn't
    res_dir = os.path.dirname(res_filename)
    time_dir = os.path.dirname(time_filename)

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)  # Create a res directory

    if not os.path.exists(time_dir):
        os.makedirs(time_dir)  # Create a time directory

    # Get all task data
    AllT, AllC = getAllTask(input_filename)

    # Check if the number of groups is correct
    if len(AllT) != GroupNumber:
        print('The number of groups is incorrect.')
        return

    # Traverse all task sets
    allTime = 0
    result = []
    t1 = time.time()
    for num in range(GroupNumber):
        T = AllT[num]
        C = AllC[num]
        chernoff_result_golden = 100
        # Set the traversal range based on the maximum task minimum Period
        arr = [i for i in range(1, int(T[Ntask - 1][0][0]) + 1)]
        if option == '100':
            # BHD
            for t in arr:
                cher_result = cher_n_o.chernoff_N_O_golden(T, C, Ntask, t)
                chernoff_result_golden = min(chernoff_result_golden, cher_result)

            print('BND WCDFP:',chernoff_result_golden)
            result.append(chernoff_result_golden)

        elif option == '010':

            # CV-D
            convolution_cov = method_cov(Ntask, T, C, thresholdC, thresholdT)

            print('CV-D WCDFP:',convolution_cov)
            result.append(convolution_cov)

        elif option == '001':
            # linear cov
            convolution_linear_cov = method_cov_linear(Ntask, T, C, thresholdC, thresholdT)

            print('CV-L WCDFP:',convolution_linear_cov)
            result.append(convolution_linear_cov)


    t2 = time.time()
    allTime = (t2 - t1) / GroupNumber
    # print('time:', allTime)

    # Save all results to a file
    first_iteration = True

    for i in range(len(result)):

        # The first write is overwritten, and subsequent writes are appended
        mode = 'w' if first_iteration else 'a'
        with open(res_filename, mode) as f:
            f.write(f'{result[i]}\n\n')
        first_iteration = False

    if iftime:
        print('time:', allTime)
        with open(time_filename, 'w') as f:
            f.write(f'{allTime}\n\n')


'''
@method Calculates the results for all analyse methods and saves them to a file.
@param Usum: Total utilization
@param Ntask: Number of tasks per set
@param cut: number of possible values in PMIT or PWCET
@param GroupNumber: Number of task sets
@param thresholdC: threshold for response time distribution
@param iftime: Whether to record computation time
'''
def experiment_all(Usum, Ntask, cut,  GroupNumber, thresholdC, iftime,taskset_bath_path):
    # BND
    experiment(Usum, Ntask, cut, GroupNumber, thresholdC, '100', iftime, taskset_bath_path)
    # CV-D
    experiment(Usum, Ntask, cut, GroupNumber, thresholdC, '010', iftime, taskset_bath_path)
    # CV-L
    experiment(Usum, Ntask, cut, GroupNumber, thresholdC, '001', iftime, taskset_bath_path)
