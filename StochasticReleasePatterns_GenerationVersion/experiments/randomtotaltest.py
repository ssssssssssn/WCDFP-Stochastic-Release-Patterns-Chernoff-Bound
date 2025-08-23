import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from experiments.taskScheduling import experiment_all,experiment
from taskGenerate.generate import generate
from plot.plotCNU import plotcut,plotN,plotU
from plot.plotTime import plotTime

'''
    Usum: Total utilization
    Ntask: Number of tasks
    cut: threshold
    GroupNumber: Number of task sets
    thresholdC: Threshold for down-sampling the response time
    iftime: Whether to record computation time
    ifresult: Whether to select the default result set provided
    taskset_bath_path: Task Set Directory
'''
def cutChange():
    Usum = 0.7
    Ntask = 10
    GroupNumber = 50
    thresholdC = 2000
    iftime = False
    ifresult = False
    taskset_bath_path = '../tasksets/taskset1'

    # Generate task set
    generate(Usum,Ntask,2,GroupNumber)
    generate(Usum,Ntask,3,GroupNumber) #default
    generate(Usum,Ntask,5,GroupNumber)
    generate(Usum,Ntask,7,GroupNumber)
    generate(Usum,Ntask,9,GroupNumber)

    # cut experiment
    # BND CV-D CV-L
    experiment_all(Usum, Ntask, 2, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(Usum, Ntask, 3, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(Usum, Ntask, 5, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(Usum, Ntask, 7, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(Usum, Ntask, 9, GroupNumber,thresholdC,iftime,taskset_bath_path)

    # plot
    # CV-D
    plotcut(Usum,Ntask,[2,3,5,7,9],GroupNumber,thresholdC,'110',ifresult)
    # CV-L
    plotcut(Usum,Ntask,[2,3,5,7,9],GroupNumber,thresholdC,'101',ifresult)


def NChange():
    Usum = 0.7
    cut = 3
    GroupNumber = 50
    thresholdC = 2000
    iftime = False
    ifresult = False
    taskset_bath_path = '../tasksets/taskset1'

    # Generate task set
    generate(Usum,5,cut,GroupNumber)
    generate(Usum,10,cut,GroupNumber) #default
    generate(Usum,15,cut,GroupNumber)
    generate(Usum,20,cut,GroupNumber)
    generate(Usum,25,cut,GroupNumber)
    generate(Usum,30,cut,GroupNumber)


    # N experiments
    # BND CV-D CV-L
    experiment_all(Usum, 5, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(Usum, 10, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(Usum, 15, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(Usum, 20, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(Usum, 25, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(Usum, 30, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)

    # plot
    # CV-D
    plotN(Usum,[5,10,15,20,25,30],cut,GroupNumber,thresholdC,'110',ifresult)
    # CV-L
    plotN(Usum,[5,10,15,20,25,30],cut,GroupNumber,thresholdC,'101',ifresult)


def UChange():
    Ntask = 10
    cut = 3
    GroupNumber = 50
    thresholdC = 2000
    iftime = False
    ifresult = False
    taskset_bath_path = '../tasksets/taskset1'

    # Generate task set
    generate(0.5,Ntask,cut,GroupNumber)
    generate(0.55,Ntask,cut,GroupNumber)
    generate(0.6,Ntask,cut,GroupNumber)
    generate(0.65,Ntask,cut,GroupNumber)
    generate(0.7,Ntask,cut,GroupNumber)
    generate(0.75,Ntask,cut,GroupNumber)
    generate(0.8,Ntask,cut,GroupNumber)

    # U experiment
    # BND CV-D CV-L
    experiment_all(0.5, Ntask, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(0.55, Ntask, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(0.6, Ntask, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(0.65, Ntask, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(0.7, Ntask, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(0.75, Ntask, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)
    experiment_all(0.8, Ntask, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)

    # plot
    # CV-D
    plotU([0.5,0.55,0.6,0.65,0.7,0.75,0.8],Ntask,cut,GroupNumber,thresholdC,'110',ifresult)
    # CV-L
    plotU([0.5,0.55,0.6,0.65,0.7,0.75,0.8],Ntask,cut,GroupNumber,thresholdC,'101',ifresult)

def TimeChange():
    Usum = 0.7
    Ntask = 10
    cut = 3
    GroupNumber = 50
    iftime = True
    ifresult = False
    taskset_bath_path = '../tasksets/taskset1'

    # Generate task set
    generate(Usum,Ntask,cut,GroupNumber) #default

    # Time
    # BND
    experiment(Usum, Ntask, cut, GroupNumber,2000,'100',iftime,taskset_bath_path) #default

    # CV-D
    experiment(Usum, Ntask, cut, GroupNumber,1,'010',iftime,taskset_bath_path)
    experiment(Usum, Ntask, cut, GroupNumber,100,'010',iftime,taskset_bath_path)
    experiment(Usum, Ntask, cut, GroupNumber,2000,'010',iftime,taskset_bath_path) #default

    # CV-L
    experiment(Usum, Ntask, cut, GroupNumber,1,'001',iftime,taskset_bath_path)
    experiment(Usum, Ntask, cut, GroupNumber,100,'001',iftime,taskset_bath_path)
    experiment(Usum, Ntask, cut, GroupNumber,2000,'001',iftime,taskset_bath_path) #default

    # plot
    # CV-D
    plotTime(Usum,Ntask,cut,GroupNumber,[1,100,2000],'110',ifresult)
    # CV-L
    plotTime(Usum,Ntask,cut,GroupNumber,[1,100,2000],'101',ifresult)

if __name__ == "__main__":
    UChange()
    NChange()
    cutChange()
    TimeChange()