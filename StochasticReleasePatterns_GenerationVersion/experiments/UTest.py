import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plot.plotCNU import  plot
from experiments.taskScheduling import experiment_all


def UTest():
    Usum = 0.8
    Ntask = 10
    cut = 3
    GroupNumber = 50
    thresholdC = 2000
    iftime = False
    taskset_bath_path = '../tasksets/taskset'

    # N experiments
    # BND CV-D CV-L
    experiment_all(Usum, Ntask, cut, GroupNumber,thresholdC,iftime,taskset_bath_path)

    # plot
    # CV-D
    plot(Usum,Ntask,cut,GroupNumber,thresholdC,'110')
    # CV-L
    plot(Usum,Ntask,cut,GroupNumber,thresholdC,'101')

if __name__ == "__main__":
    UTest()