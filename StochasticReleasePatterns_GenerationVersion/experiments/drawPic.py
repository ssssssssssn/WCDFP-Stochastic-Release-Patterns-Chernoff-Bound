import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from plot.plotCNU import plotcut, plotU, plotN
from plot.plotTime import plotTime


if __name__ == "__main__":
    # # U experiment
    # # CV-D
    plotU([0.5,0.55,0.6,0.65,0.7,0.75,0.8],10,3,50,2000,'110',True)
    # # CV-L
    plotU([0.5,0.55,0.6,0.65,0.7,0.75,0.8],10,3,50,2000,'101',True)

    # N experiments
    # CV-D
    plotN(0.7,[5,10,15,20,25,30],3,50,2000,'110',True)
    # # CV-L
    plotN(0.7,[5,10,15,20,25,30],3,50,2000,'101',True)

    # cut experiment
    # CV-D
    plotcut(0.7,10,[2,3,5,7,9],50,2000,'110',True)
    # # CV-L
    plotcut(0.7,10,[2,3,5,7,9],50,2000,'101',True)

    # time experiment
    # CV-D
    plotTime(0.7,10,3,50,[1,10,100,500,1000,2000,4000,8000,16000],'110',True)
    # CV-L
    plotTime(0.7,10,3,50,[1,10,100,500,1000,2000,4000,8000,16000],'101',True)

