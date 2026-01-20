from constants import n, S, D
import numpy as np

CPI = 1/2
clock_frequency = 1 # Unknown
L1H_cost = 1
L1M_cost = 13
L2H_cost = 1 # Unknown
L2M_cost = 123


def call_valgrind_WIP(I_refs, D_refs, LL_refs, I1_miss, D1_miss, LL_miss):
    L1_total = I_refs + D_refs - LL_refs
    L1_miss = I1_miss + D1_miss
    L1_hit = L1_total - L1_miss
    L2_hit = LL_refs - LL_miss
    L2_miss = LL_miss

    execution_cycles = CPI*I_refs

    cycles = (L1H_cost*L1_hit +
              L1M_cost*L1_miss +
              L2H_cost*L2_hit +
              L2M_cost*L2_miss +
              execution_cycles)

    return cycles * 1/clock_frequency


class C_ij:
    stored_Cij = np.zeros([n+1,len(S)])
    nbr_valgrind_calls = 0
    nbr_calls = 0

    def get_Cij(i,j):
        if (C_ij.stored_Cij[i, j] == 0):
            C_ij.stored_Cij[i, j] = call_valgrind(i,j)
            C_ij.nbr_valgrind_calls += 1
        C_ij.nbr_calls += 1
        return call_valgrind(i,j)
        #return C_ij.stored_Cij[i,j]

    def get_nums():
        return (C_ij.nbr_calls, C_ij.nbr_valgrind_calls)

def call_valgrind(i,j):
    return 0.3 * i * 1/(3*j+0.1)
