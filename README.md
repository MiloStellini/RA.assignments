# RA.assignments
GALTON
Galton.py is the code of the assignment.
Python libraries: numpy, matplotlib, scipy.
At the bottom of the code there are all the variables that can be modified to show different plots and simulations.
N and n are respectively the number of balls and the number of bins used for the distribution plot.
N_values and n_values are different numbers of balls and bins used for the error plot between empirical and theoretical distributions.
Once run, the program will show three differents plots, one after the other.
At line 92 it is possible to uncomment to print the MSEs between empirical and theoretical distributions on the terminal.

BALANCED ALLOCATION
Balanced_Allocation.py is the code for the first methods with full information.
Balanced_Allocation2.py is the code for the b-batching setting.
Balanced_Allocation3.py is the code for the partial information setting.
All 3 codes have assignments to the variables n,m,beta,d and k at the beginning of the code, and can be modified.
The program run in Python will show the plots displayed in the PDF.

CARDINALITY ESTIMATION
Cardinality_Estimation.py is the code of the assignment.
Python libraries: randomhash, math, heapq, numpy, matplotlib.
It is possible to tune the parameters of the synthetic data at line 116.
Shifting to the real datasets is possible using "data" at lines 133 and 147 instead of "syn_data". The file paths are at lines 107 and 108. It is also necessary to uncomment line 124 and comment 125.
It is possible to tune the parameters of the two algorithms at lines 128 and 142.
