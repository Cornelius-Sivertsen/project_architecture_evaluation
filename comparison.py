from constants import n, S

K = len(S)

nbr_extreme_nodes = K**n


nbr_nodes = 0


for i in range(n):
    nbr_nodes += K**(i+1)

