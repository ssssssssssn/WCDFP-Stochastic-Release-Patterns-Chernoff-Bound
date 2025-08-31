# WCDFP Analysis for Real-Time Tasks with Stochastic Release Patterns using Chernoff Bound

This repository is used to reproduce the evaluation from paper:

***WCDFP Analysis for Real-Time Tasks with Stochastic Release Patterns using Chernoff Bound***

for RTSS 2025 submission. This document is explaining how to use the artifact to repeat the experiments presented in the paper, i.e., Fig. 2(a)-(h) in Section V. 

The rest of the document is organized as follows:

1. [Code download and environmental set up](#Code-download-and-environmental-set-up)
2. [Directory structure](#directory-structure)
3. [The random task sets and results for all the Figs in the paper](#The-random-task-sets-and-results-for-all-the-Figs-in-the-paper)
4. [How to run the random experiments](#how-to-run-the-random-experiments)
5. [Our paper](#our-paper)

## Code download and Environmental set up

Experiments are executed on a desktop computer with Windows 10 OS, equipped with an Intel(R) Core(TM) i7-10700 processor and 8GB of RAM.


### Code download

**If you use VirtualBox,Please find the link([Image download link](https://github.com/ssssssssssn/WCDFP-Stochastic-Release-Patterns-Chernoff-Bound)) and download the image file with the `.ova` extension. There is no need to download (StochasticReleasePatterns_VSCodeVersion and StochasticReleasePatterns_GenerationVersion).Please use vscode to run our code.Our code and vscode are both provided on the deskop**

*We have already set up the environment in the virtual machine, please note that we are not conducting the experiments with the virtual machine; instead, we are doing the experiments on our physical computer.*



**If you are using VSCode (we will provide instructions on how to install and use it), please download the code([StochasticReleasePatterns_VSCodeVersion](https://github.com/ssssssssssn/WCDFP-Stochastic-Release-Patterns-Chernoff-Bound/tree/main/StochasticReleasePatterns_VSCodeVersion)).**

**If you are using other Python IDEs, such as PyCharm, please download the code([StochasticReleasePatterns_GenerationVersion](https://github.com/ssssssssssn/WCDFP-Stochastic-Release-Patterns-Chernoff-Bound/tree/main/StochasticReleasePatterns_GenerationVersion)) instead.**


### Environmental set up

***This section is intended for those who are not using the provided virtual machine.***


We use Python 3.8 in our experiments. If you are familiar with Python, you may configure the environment on your own and make sure to install the required packages.

    mpmath scipy numpy matplotlib adjustText

Otherwise, we provide step-by-step instructions on how to deploy Python 3.8 and install the required libraries on a Windows system.

For more details, please refer to [EnvironmentalDependence](https://github.com/ssssssssssn/WCDFP-Stochastic-Release-Patterns-Chernoff-Bound/blob/main/StochasticReleasePatterns_VSCodeVersion/EnvironmentalDependence.md).



## Directory structure

The following shows all the file directories, where for each function in every file, we have provided detailed annotations of its parameters and key procedures.
    

    .
    ├── algorithms                  # algorithms
    │   ├── cher_n_o.py             # Theorem 3 in our paper
    │   ├── convolution.py          # convolution operation of two random variables
    │   ├── cov_cucu.py             # Convolution method from Maxim et al. (RTSS 2013)
    │   ├── resample.py             # downsampling techniques
    ├── experiments                 # Evaluation scripts
    │── plot                        # Plotter and plots 
    │── results                     # Results of evaluations
    │── taskGenerate                # Tasksets generateor
    │── tasksets                    # Generated tasksets
    └── README.md  

## The random task sets and results for all the Figs in the paper



The random task sets 
and the corresponding results presented in Fig. 2(a)-(h) are provided. 
Specifically, all  task sets   are stored in the directory `.\tasksets\taskset`, 
and the results of each algorithm are stored in `.\results\result`.


For example, the file
`.\tasksets\taskset\0.5u_10n_3cut_t_3cut_c_50turns_input.txt` (which contains 50 task sets) corresponds to the following results:

* **CH-BND**:
  `.\results\result\res\0.5u_10n_3cut_t_3cut_c_50turns_CH_BND_res.txt`

* **CV-D** (with downsample threshold for response time set to **2000**):
  `.\results\result\res\0.5u_10n_3cut_t_3cut_c_50turns_2000thresholdC_CV_D_res.txt`

* **CV-L** (with downsample threshold for response time set to **2000**):
  `.\results\result\res\0.5u_10n_3cut_t_3cut_c_50turns_2000thresholdC_CV_L_res.txt`

---

## How to run the random experiments

We will present the experimental reproduction of Fig. 2(a)–(h). 
To facilitate this, we provide ready-to-use code files that can be executed directly, without the need to write additional testing code.
In total, we provide four testing scripts:

* One script allows you to reproduce the plots using the supplied results. (Only takes ***a few seconds***)

* One script enables the full reproduction of our random experiments, i.e. Fig. 2(a)–(h) (note that this may take more than ***3 weeks***).

* For convenience, we also provide two ***lightweight*** tests, which can be completed within a few hours.




### Script 1 reproduce the plots

(This test takes ***a few seconds***)

Running python file: `./experiments/drawPic.py` allows you to reproduce the plots using the supplied results. (please refer to [EnvironmentalDependence](EnvironmentalDependence.md) for instructions on how to run a Python file in VSCode.)

The resulting plots are saved in: `./plot/outputs\`. The correspondence between the output figures and those in the paper is as follows::

| Paper Figure | Output Figure |
| ------------ | ------------- |
| Fig. 2(a)    | CV-D-Time.svg |
| Fig. 2(b)    | CV-L-Time.svg |
| Fig. 2(c)    | CV-D-N.svg    |
| Fig. 2(d)    | CV-D-U.svg    |
| Fig. 2(e)    | CV-D-cut.svg  |
| Fig. 2(f)    | CV-L-N.svg    |
| Fig. 2(g)    | CV-L-U.svg    |
| Fig. 2(h)    | CV-L-cut.svg  |

### Script 2 full reproduction of our random experiments

(This test takes more than ***3 weeks***)

Running python file: `./experiments/randomtotaltest.py` enables the full reproduction of our random experiments, i.e. Fig. 2(a)–(h) (note that this may take more than ***3 weeks***).


* The randomly generated task sets are stored in `./tasksets/taskset1/`.
* The experimental results are saved in `./results/result1/res/`.
* The runtime files are stored in `./results/result1/time/`.
* The resulting plots are available in `./plot/outputs/`.

### Script 3 lightweight test1: reproduce the random experiment on one parameter.

(This test takes about ***10 hours***)


Running the python file `./experiments/randomUTest.py` reproduces the random experiment on one parameter:
total utilization = 0.8, number of possible values of PMIT and PWCET = 3, 10 tasks per task set, and a re-sampling threshold of 2000.



The data and results are saved as follows:

* The randomly generated task sets are stored in `./tasksets/taskset1/`.
* The experimental results are saved in `./results/result1/res/`.
* The resulting plots are available in `./plot/outputs/`.


The two resulting plots correspond to the same parameter settings as the rightmost box in Fig. 2(d) and Fig. 2(g).
**However, please note that this test generates 30 task sets, whereas the experiments reported in our paper use 50 task sets. A smaller number of task sets may lead to higher variability in the results. Therefore, we recommend increasing the number of task sets whenever time permits.**


### Script 4 lightweight test2: reproduce the outcome with our provided random task set.

(This test takes about ***17 hours***)


Running the python file `./experiments/UTest.py` reproduces the outcome using our provided random task set.
The parameters of this task set are: total utilization = 0.8, number of possible values of PMIT and PWCET = 3, 10 tasks per task set, and a re-sampling threshold of 2000.

The results are saved as follows:

* The experimental results are saved in `./results/result1/res/`.
* The resulting plots are available in `./plot/outputs/`.

You may cross-check these results with the corresponding ones we provide for the same task set.
For details on how to locate our provided results, please refer to [The random task sets and results for all the Figs in the paper](#The-random-task-sets-and-results-for-all-the-Figs-in-the-paper).


Also, the two resulting plots are identical to the rightmost box in Fig. 2(d) and Fig. 2(g).

