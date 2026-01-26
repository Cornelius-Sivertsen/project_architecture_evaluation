# Functions used to calculate Cij. 
from global_vars import n, S, D, processes
import numpy as np
import parse

CPI = 1/2

L1H_cost = 1
L1M_cost = 13

L2M_cost = 123


# The function that reads Cij from vallgrind output
def calculate_cycles(I_refs, D_refs, LL_refs, I1_miss, D1_miss, LL_miss):
    L1_total = I_refs + D_refs - LL_refs
    L1_miss = I1_miss + D1_miss
    L1_hit = L1_total - L1_miss
    L2_hit = LL_refs - LL_miss
    L2_miss = LL_miss

    execution_cycles = CPI*I_refs

    cycles = (L1H_cost*L1_hit +
              L1M_cost*L1_miss +
              L2M_cost*L2_miss +
              execution_cycles)

    return cycles


# Use of class to get static functionallity
class C_ij:
    stored_Cij = np.zeros([n+1,len(S)])
    nbr_valgrind_calls = 0
    nbr_calls = 0

    # If C_ij has already been obtained from valgrind, use the stored result instead of re-running valgrind. If not, call valgrind
    def get_Cij(i,j):
        if (C_ij.stored_Cij[i, j] == 0):
            C_ij.stored_Cij[i, j] = call_valgrind(i,j)
            C_ij.nbr_valgrind_calls += 1
        C_ij.nbr_calls += 1
        
        return C_ij.stored_Cij[i,j]

    def get_nums():
        return (C_ij.nbr_calls, C_ij.nbr_valgrind_calls)

# Call valgrind function
def call_valgrind(i,j):

    if i == 0:
        return 0

    valgrind_result = parse.get_valgrind_result(i,j)
    return calculate_cycles(*valgrind_result)

