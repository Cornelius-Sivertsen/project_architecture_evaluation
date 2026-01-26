# Global variables used throughout the program

S = [] # List of cache partition sizes, set in parse.py

processes = ['root', 'pca', 'sphinx', 'disparity']
n = len(processes)-1


D = [0,
    431308233500.5,
    1766791655780.5,
    391161470400.5,]


U_rm = n*(2**(1/n)-1)
