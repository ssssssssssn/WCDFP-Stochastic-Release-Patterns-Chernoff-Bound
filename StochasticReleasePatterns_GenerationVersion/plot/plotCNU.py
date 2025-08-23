import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import numpy as np
from matplotlib import pyplot as plt, ticker
from matplotlib.ticker import FixedLocator, FixedFormatter
from mpmath import mpf

"""
@method: Draws a box plot and saves it as an SVG file.
@param data: list, containing the data for each interval used to draw the box plot.
@param filename: str, the file name to save the plot results to.
@param interval: list, interval values, representing different categories on the x-axis.
@param method: str, the plotting method name, such as "CV-D" or "CV-L."
@param type: str, the plotting type used to distinguish between different experimental graphs
"""
def drawBox(data, outputfilepath, interval, method,type):
    fig, axes = plt.subplots(figsize=(10, 6), sharey=True)

    for spine in axes.spines.values():
        spine.set_linewidth(1)  

    if type == 'signal':
        labels = [str(interval[0]) + 'u_' + str(interval[1]) + 'n_' + str(interval[2]) + 'cut_' + str(interval[3]) + 'thresholdC']
    else:
        labels = [f'{c}' for c in interval]
    axes.set_yscale("log")

    ylableName = method + '/BND'
    axes.set_ylabel(ylableName, fontsize=20, labelpad=-5)
    axes.tick_params(axis='both', which='major', labelsize=18)

    axes.axhline(y=1e0, color='red', linestyle='-', linewidth=1, alpha=0.7)

    axes.set_ylim(1e-30, 1e100)

    main_exponents = [0, 50, 100]
    minor_exponents = list(range(-30, 101, 10))

    main_ticks = [10.0 ** e for e in main_exponents]
    minor_ticks = [10.0 ** e for e in minor_exponents]

    axes.yaxis.set_major_locator(FixedLocator(main_ticks))
    axes.yaxis.set_minor_locator(FixedLocator(minor_ticks))

    axes.yaxis.set_major_formatter(ticker.FuncFormatter(
        lambda y, _: r'$10^{%d}$' % np.log10(y)
    ))

    axes.yaxis.set_minor_formatter(ticker.FuncFormatter(
        lambda y, _: (r'$10^{%d}$' % np.log10(y)) if np.log10(y) not in main_exponents else ''
    ))

    axes.tick_params(
        axis='y',
        which='major',
        length=8,
        width=2,
        labelsize=20,
        colors='black'
    )
    axes.tick_params(
        axis='y',
        which='minor',
        length=4,
        width=1,
        colors='black',
        labelsize=14
    )

    plt.xlim(0, 8)
    if type == 'signal':
        n = 1
    else:
        n = len(interval)
    s = 4 / n
    positions = [round(s + 2 * s * i, 1) for i in range(n)]

    axes.set_xticks(positions)

    cmap = plt.get_cmap("Blues")
    axes.boxplot(data,
                 widths=0.3,
                 positions=positions,
                 # widths=0.3,
                 # whis=0.4 ,
                 whis=(10, 90),
                 patch_artist=True,
                 boxprops=dict(facecolor="white", edgecolor=cmap(0.9), lw=1.8),  
                 whiskerprops=dict(color=cmap(0.9), linestyle="-"),
                 capprops=dict(color=cmap(0.9), lw=1.8),
                 medianprops=dict(color=cmap(0.6), lw=1.5), 
                 flierprops=dict(marker="o", markersize=6),
                 labels=labels)

    axes.grid(True, which='both', linewidth=1, linestyle='--', alpha=0.5)

    # eg. CV-D/BND-N.SVG
    if type == 'signal':
        filename = outputfilepath + method + '_test.svg'
    else:
        filename = outputfilepath + method + '-' + type + '.svg'
    print(filename)
    plt.savefig(
        filename,
        bbox_inches='tight',
        pad_inches=0.1,
        format='svg'
    )
    plt.show()

"""
@method: Divides two sets of data and returns the combined result.
@param data_cov: list, the first set of data, the result of cov.
@param data_cher: list, the second set of data, the result of chernoff.
@return: list, the combined data containing the division result.
"""
def division_split(data_cov, data_cher):
    divData = []
    if len(data_cher) != len(data_cov):
        print("The two files are of different lengths！！！")
        return

    for i in range(len(data_cov)):
        cher_n_o = data_cher[i]
        cov = data_cov[i]

        for j in range(len(cher_n_o)):
            result = []
            for c, cher in zip(cov[j], cher_n_o[j]):
                if c - mpf('1e-500') < 0 and cher - mpf('1e-500') < 0:
                    continue
                elif c - mpf('1e-500') >= 0 and cher - mpf('1e-500') < 0:
                    ratio = 1e130
                    result.append(ratio)
                    continue
                elif c - mpf('1e-500') < 0 and cher - mpf('1e-500') >= 0:
                    ratio = 1e-40
                    result.append(ratio)
                    continue

                c = min(c, 1)
                cher = min(cher, 1)

                ratio = min(1e130, float(c / cher))
                result.append(ratio)

            divData.append(result)


    return divData


"""
@method: Reads data from a file and parses it into a format suitable for plotting.
@param file_paths: list, a list of multiple file paths.
@return: list, a list of parsed data.
"""
def load_and_parse_data(file_path):
    allData = []
    for i in range(len(file_path)):
        with open(file_path[i], "r") as file:
            lines = [line.strip() for line in file if line.strip()]
        data = []
        for line in lines:
            lineData = line.strip().split(',')

            for i in range(len(lineData)):
                lineData[i] = mpf(lineData[i])
            data.append(lineData)

        column = []
        for i in range(0, len(data[0])):
            column.append([row[i] for row in data])
        allData.append(column)

    return allData

"""
@method: Reads data from the target path and plots the results using cov/chenroff.
@param file_cov_paths: list, list of cov file paths.
@param file_cher_paths: list, list of cher file paths.
@param output_filepath: str, path to save the output files.
@param interval: list, x-axis intervals.
@param plot_type: str, plot type, used to distinguish different experiments.
@param method: str, the plotting method name, such as "CV-D" or "CV-L."
@param type: str, the plotting type used to distinguish between different experimental graphs
"""
def plotBox_split(file_cov_path, file_cher_path, outputfilepath, interval, method,type):
    data_cov = load_and_parse_data(file_cov_path)
    data_cher = load_and_parse_data(file_cher_path)
    data = division_split(data_cov, data_cher)
    drawBox(data, outputfilepath, interval, method,type)


'''
@method: Draws a box plot of N changes
@param Usum: float, total utilization
@param NIntervals: list, intervals for N task sets
@param cut: int, number of slices
@param GroupNumber: int, number of task groups
@param thresholdC: int, execution time threshold
@param option: str, plotting options for selecting different calculation methods
@param ifresult: str,Whether to select the default result set provided
'''
def plotN(Usum,NIntervals,cut,GroupNumber,thresholdC,option,ifresult):
    if ifresult == True:
        base_res_dir = r"../results/result/res/"
    else:
        base_res_dir = r"../results/result1/res/"
    base_output_dir = r"../plot/outputs/"
    cut_t = cut
    cut_c = cut

    file_chernoff_path = []
    file_cov_path = []
    file_linear_cov_path = []
    # Get the chernoff result set file path
    for n in NIntervals:
        templateChernoff = str(Usum)+'u_'+str(n)+'n_'+str(cut_t)+'cut_t_'+str(cut_c)+'cut_c_'+str(GroupNumber)+'turns_CH_BND_res.txt'
        path = base_res_dir + templateChernoff
        file_chernoff_path.append(path)



    if option == '110':
        # Get the cov result set file path
        for n in NIntervals:
            templateCov = str(Usum) + 'u_' + str(n) + 'n_' + str(cut_t) + 'cut_t_' + str(cut_c) + 'cut_c_' + str(
                GroupNumber) + 'turns_' + str(thresholdC) + 'thresholdC_CV_D_res.txt'
            path = base_res_dir + templateCov
            file_cov_path.append(path)
        plotBox_split(file_cov_path, file_chernoff_path,base_output_dir, NIntervals, 'CV-D','N')

    elif option == '101':
        # Get the linear cov result set file path
        for n in NIntervals:
            templateLinearCov = str(Usum) + 'u_' + str(n) + 'n_' + str(cut_t) + 'cut_t_' + str(cut_c) + 'cut_c_' + str(
                GroupNumber) + 'turns_' + str(thresholdC) + 'thresholdC_CV_L_res.txt'
            path = base_res_dir + templateLinearCov
            file_linear_cov_path.append(path)
        plotBox_split(file_linear_cov_path, file_chernoff_path,base_output_dir, NIntervals, 'CV-L','N')
    else:
        print('Please change the option!!!')

'''
@method: Draws a box plot of N changes
@param UIntervals: list, intervals for Usum
@param Ntask: task number
@param cut: int, number of slices
@param GroupNumber: int, number of task groups
@param thresholdC: int, execution time threshold
@param option: str, plotting options for selecting different calculation methods
@param ifresult: str,Whether to select the default result set provided
'''
def plotU(UIntervals,Ntask,cut,GroupNumber,thresholdC,option,ifresult):
    if ifresult == True:
        base_res_dir = r"../results/result/res/"
    else:
        base_res_dir = r"../results/result1/res/"
    base_output_dir = r"../plot/outputs/"

    cut_t = cut
    cut_c = cut

    file_chernoff_path = []
    file_cov_path = []
    file_linear_cov_path = []
    # Get the chernoff result set file path
    for u in UIntervals:
        templateChernoff = str(u)+'u_'+str(Ntask)+'n_'+str(cut_t)+'cut_t_'+str(cut_c)+'cut_c_'+str(GroupNumber)+'turns_CH_BND_res.txt'
        path = base_res_dir + templateChernoff
        file_chernoff_path.append(path)

    if option == '110':
        # Get the cov result set file path
        for u in UIntervals:
            templateCov = str(u) + 'u_' + str(Ntask) + 'n_' + str(cut_t) + 'cut_t_' + str(cut_c) + 'cut_c_' + str(
                GroupNumber) + 'turns_' + str(thresholdC) + 'thresholdC_CV_D_res.txt'
            path = base_res_dir + templateCov
            file_cov_path.append(path)
        plotBox_split(file_cov_path, file_chernoff_path,base_output_dir, UIntervals, 'CV-D','U')

    elif option == '101':
        # Get the linear cov result set file path
        for u in UIntervals:
            templateLinearCov = str(u) + 'u_' + str(Ntask) + 'n_' + str(cut_t) + 'cut_t_' + str(cut_c) + 'cut_c_' + str(
                GroupNumber) + 'turns_' + str(thresholdC) + 'thresholdC_CV_L_res.txt'
            path = base_res_dir + templateLinearCov
            file_linear_cov_path.append(path)
        plotBox_split(file_linear_cov_path, file_chernoff_path,base_output_dir, UIntervals, 'CV-L','U')
    else:
        print('Please change the option!!!')

'''
@method: Draws a box plot of N changes
@param Usum: float, total utilization
@param Ntask: int, task number
@param cut: list, intervals for cut task sets
@param GroupNumber: int, number of task groups
@param thresholdC: int, execution time threshold
@param option: str, plotting options for selecting different calculation methods
@param ifresult: str,Whether to select the default result set provided
'''
def plotcut(Usum,Ntask,cutIntervals,GroupNumber,thresholdC,option,ifresult):
    if ifresult == True:
        base_res_dir = r"../results/result/res/"
    else:
        base_res_dir = r"../results/result1/res/"
    base_output_dir = r"../plot/outputs/"


    file_chernoff_path = []
    file_cov_path = []
    file_linear_cov_path = []
    # Get the chernoff result set file path
    for cut in cutIntervals:
        templateChernoff = str(Usum)+'u_'+str(Ntask)+'n_'+str(cut)+'cut_t_'+str(cut)+'cut_c_'+str(GroupNumber)+'turns_CH_BND_res.txt'
        path = base_res_dir + templateChernoff
        file_chernoff_path.append(path)

    if option == '110':
        # Get the cov result set file path
        for cut in cutIntervals:
            templateCov = str(Usum) + 'u_' + str(Ntask) + 'n_' + str(cut) + 'cut_t_' + str(cut) + 'cut_c_' + str(
                GroupNumber) + 'turns_' + str(thresholdC) + 'thresholdC_CV_D_res.txt'
            path = base_res_dir + templateCov
            file_cov_path.append(path)
        plotBox_split(file_cov_path, file_chernoff_path,base_output_dir, cutIntervals, 'CV-D','cut')

    elif option == '101':
        # Get the linear cov result set file path
        for cut in cutIntervals:
            templateLinearCov = str(Usum) + 'u_' + str(Ntask) + 'n_' + str(cut) + 'cut_t_' + str(cut) + 'cut_c_' + str(
                GroupNumber) + 'turns_' + str(thresholdC) + 'thresholdC_CV_L_res.txt'
            path = base_res_dir + templateLinearCov
            file_linear_cov_path.append(path)
        plotBox_split(file_linear_cov_path, file_chernoff_path,base_output_dir, cutIntervals, 'CV-L','cut')
    else:
        print('Please change the option!!!')


'''
@method: Draws a box plot of signal parameter
@param Usum: float, total utilization
@param Ntask: int, number of tasks per set 
@param cut: list, intervals for cut task sets
@param GroupNumber: int, number of task groups
@param thresholdC: int, execution time threshold
@param option: str, plotting options for selecting different calculation methods
'''
def plot(Usum,Ntask,cut,GroupNumber,thresholdC,option):
    base_res_dir = r"../results/result1/res/"
    base_output_dir = r"../plot/outputs/"


    file_chernoff_path = []
    file_cov_path = []
    file_linear_cov_path = []
    # Get the chernoff result set file path
    templateChernoff = str(Usum)+'u_'+str(Ntask)+'n_'+str(cut)+'cut_t_'+str(cut)+'cut_c_'+str(GroupNumber)+'turns_CH_BND_res.txt'
    path = base_res_dir + templateChernoff
    file_chernoff_path.append(path)

    if option == '110':
        # Get the cov result set file path
        templateCov = str(Usum) + 'u_' + str(Ntask) + 'n_' + str(cut) + 'cut_t_' + str(cut) + 'cut_c_' + str(
            GroupNumber) + 'turns_' + str(thresholdC) + 'thresholdC_CV_D_res.txt'
        path = base_res_dir + templateCov
        file_cov_path.append(path)
        plotBox_split(file_cov_path, file_chernoff_path,base_output_dir, [Usum,Ntask,cut,thresholdC], 'CV-D','signal')

    elif option == '101':
        # Get the linear cov result set file path
        templateLinearCov = str(Usum) + 'u_' + str(Ntask) + 'n_' + str(cut) + 'cut_t_' + str(cut) + 'cut_c_' + str(
            GroupNumber) + 'turns_' + str(thresholdC) + 'thresholdC_CV_L_res.txt'
        path = base_res_dir + templateLinearCov
        file_linear_cov_path.append(path)
        plotBox_split(file_linear_cov_path, file_chernoff_path,base_output_dir, [Usum,Ntask,cut,thresholdC], 'CV-L','signal')
    else:
        print('Please change the option!!!')

if __name__ == "__main__":
    plotN(0.7,[5,10,15,20,25,30],3,50,2000,'110',True)
    plotN(0.7,[5,10,15,20,25,30],3,50,2000,'101',True)

    plotU([0.5,0.55,0.6,0.65,0.7,0.75,0.8],10,3,50,2000,'110',True)
    plotU([0.5,0.55,0.6,0.65,0.7,0.75,0.8],10,3,50,2000,'101',True)

    plotcut(0.7,10,[2,3,5,7,9],50,2000,'110',True)
    plotcut(0.7,10,[2,3,5,7,9],50,2000,'101',True)
