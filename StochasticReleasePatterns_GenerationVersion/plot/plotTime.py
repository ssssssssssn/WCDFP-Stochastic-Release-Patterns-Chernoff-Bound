import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from adjustText import adjust_text
import numpy as np
from matplotlib import pyplot as plt, gridspec
from mpmath import mpf

'''
@method: Get task data from a file
@param file_path: str, path to the task data file
@return: list, list of task data
'''
def getTask(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]
    data = []
    for line in lines:

        if mpf(line) > 1:
            line = 1
        line = mpf(line)
        data.append(line)
    return data

'''
@method: Get time data from a file
@param file_path: str, path to the time data file
@return: float, average value of the time data
'''
def getTime(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    averageTime = mpf(lines[0])

    return averageTime

'''
@method: Draws a box plot of the task set evaluation results and execution time.
@param resData: list of lists, result data for each task set
@param timeData: list of floats, average time data for each task set
@param filename: str, output file path
@param interval: list of ints, intervals
@param method: str, calculation method name (e.g., 'CV-D' or 'CV-L')
'''
def drawBoxChangecovC(resData, timeData, filename, interval, method):
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 6)
    plt.subplots_adjust(left=0.13, right=0.9, top=0.97, bottom=0.22)  

    # Main Y axis settings
    ax.set_yscale("log")
    ax.set_ylim(1e-100, 1e0)
    ax.set_yticks([10.0 ** exp for exp in np.arange(0, -101, -10)])
    ax.set_ylabel('WCDFP', fontsize=20, labelpad=10)
    ax.tick_params(axis='both', which='major', labelsize=18)
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)

    # Secondary Y axis settings
    ax2 = ax.twinx()
    ax2.set_ylabel('Average time (s)', fontsize=20, labelpad=15)
    ax2.tick_params(axis='y', labelsize=18)
    for spine in ax2.spines.values():
        spine.set_linewidth(1.5)
    ax2.set_ylim(0, 6000)
    num_ticks = 10
    yticks = np.linspace(0, 6000, num_ticks + 1)
    ax2.set_yticks(yticks)
    # Label setting 2
    label = ['CH-BND'] + [f'{method}({i})' for i in interval]

    # Color Configuration
    cmap_blue = plt.get_cmap("Blues")(0.9)
    cmap_red = plt.get_cmap("Reds")(0.9)
    line_colors = [cmap_blue if i < 1 else cmap_red for i in range(len(timeData))]


    positions = list(range(len(resData)))
    for idx, data in enumerate(resData):
        ax.boxplot(
            [data],
            positions=[positions[idx]],
            # whis=(10, 90),
            widths=0.3,
            boxprops=dict(color=line_colors[idx], linewidth=2.5),
            whiskerprops=dict(color=line_colors[idx], linestyle="-", linewidth=2.5),
            capprops=dict(color=line_colors[idx], linewidth=2.5),
            medianprops=dict(color=line_colors[idx], linewidth=3),
            flierprops=dict(marker="o", markersize=3, markeredgecolor="black")
        )


    ax.set_xticks(positions)
    ax.set_xticklabels(label, rotation=45, ha='center', fontsize=18)

    # Draw a line chart
    ax2.plot(
        positions,
        timeData,
        color=cmap_red,
        linestyle='-',
        linewidth=2,
        marker='o',
        markersize=5,
        markerfacecolor='white',
        markeredgewidth=2
    )

    
    for idx in range(len(timeData)):
        ax2.plot(positions[idx], timeData[idx], 'o', color=line_colors[idx], markersize=5)

   
    texts = []
    for idx, (x, y) in enumerate(zip(positions, timeData)):
        text = ax2.text(
            x - 0.02,
            y * 0.96,
            f'{float(y):.2f}',
            # rotation=30,
            ha='right',
            va='bottom',
            fontsize=14,
            color=line_colors[idx]
        )
        texts.append(text)

    adjust_text(texts)

    ax.grid(True, which='both', linewidth=1, linestyle='--', alpha=0.7)
    # Draw a line chart
    output_filename = filename + '/'+ method +'-Time.svg'
    print(output_filename)
    plt.savefig(
        output_filename,
        bbox_inches='tight',
        pad_inches=0.1,
        format='svg'
    )
    plt.show()


'''
@method: Draws a box plot and time plot based on file paths.
@param filePaths: list of str, containing the paths to multiple task result files.
@param timeFilePaths: list of str, containing the paths to multiple time data files.
@param interval: list of int, intervals.
@param outputFilePath: str, output file path.
@param method: str, calculation method name.
'''
def plotBoxChangecovC(filePaths, timeFilePaths, interval, outputFilePath,method):
    resData = []
    timeData = []
    print()
    for path in filePaths:
        data = getTask(path)
        resData.append(data)
    for path in timeFilePaths:
        data = getTime(path)
        timeData.append(data)
    drawBoxChangecovC(resData, timeData, outputFilePath, interval,method)

'''
@method: Plots the time and results of the specified set of tasks
@param Usum: float, total utilization
@param Ntask: int, number of tasks
@param cut: int, cut
@param GroupNumber: int, number of task groups
@param thresholdCIntervals: list of ints, execution time thresholds
@param option: str, plotting options, specifying the calculation method ('110' for CV-D, '101' for CV-L)
@param ifresult: str,Whether to select the default result set provided
'''
def plotTime(Usum,Ntask,cut,GroupNumber,thresholdCIntervals,option,ifresult):
    if ifresult == True:
        base_res_dir = r"../results/result/res/"
        base_time_dir = r"../results/result/time/"
    else:
        base_res_dir = r"../results/result1/res/"
        base_time_dir = r"../results/result1/time/"
    base_output_dir = r"../plot/outputs/"
    thresholdT = 5

    ResPaths = []
    TimePaths = []

    # BND
    chernoff_res_path = base_res_dir + str(Usum)+'u_'+str(Ntask)+'n_'+str(cut)+'cut_t_'+str(cut)+'cut_c_'+str(GroupNumber)+'turns_CH_BND_res.txt'
    chernoff_time_path = base_time_dir + str(Usum)+'u_'+str(Ntask)+'n_'+str(cut)+'cut_t_'+str(cut)+'cut_c_'+str(GroupNumber)+'turns_CH_BND_time.txt'
    ResPaths.append(chernoff_res_path)
    TimePaths.append(chernoff_time_path)

    if option == '110':
        for covC in thresholdCIntervals:
            cov_res_path = base_res_dir + str(Usum)+'u_'+str(Ntask)+'n_'+str(cut)+'cut_t_'+str(cut)+'cut_c_'+str(GroupNumber)+'turns_'+str(covC)+'thresholdC_CV_D_res.txt'
            cov_time_path = base_time_dir + str(Usum)+'u_'+str(Ntask)+'n_'+str(cut)+'cut_t_'+str(cut)+'cut_c_'+str(GroupNumber)+'turns_'+str(covC)+'thresholdC_CV_D_time.txt'
            ResPaths.append(cov_res_path)
            TimePaths.append(cov_time_path)

        plotBoxChangecovC(ResPaths, TimePaths, thresholdCIntervals, base_output_dir,'CV-D')
    elif option == '101':
        for covC in thresholdCIntervals:
            linear_res_path = base_res_dir + str(Usum)+'u_'+str(Ntask)+'n_'+str(cut)+'cut_t_'+str(cut)+'cut_c_'+str(GroupNumber)+'turns_'+str(covC)+'thresholdC_CV_L_res.txt'
            linear_time_path = base_time_dir + str(Usum)+'u_'+str(Ntask)+'n_'+str(cut)+'cut_t_'+str(cut)+'cut_c_'+str(GroupNumber)+'turns_'+str(covC)+'thresholdC_CV_L_time.txt'

            ResPaths.append(linear_res_path)
            TimePaths.append(linear_time_path)

        plotBoxChangecovC(ResPaths, TimePaths, thresholdCIntervals, base_output_dir,'CV-L')


if __name__ == "__main__":
    # CV-D
    plotTime(0.7,10,3,50,[1,10,100,500,1000,2000,4000,8000,16000],'110',True)
    # CV-L
    plotTime(0.7,10,3,50,[1,10,100,500,1000,2000,4000,8000,16000],'101',True)
