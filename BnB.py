from constants import n, S, D, U_rm
from Node import SolutionNode
from Cij import C_ij
import time

start_time = time.perf_counter()
# Stores the cost of the best complete solution (terminal node) found so far. Initialized with the worst case solution
best_cost = n*S[-1]

# Stores the terminal node corresponding to the best solution found so far
best_solution = SolutionNode(0,0,0,0,None)

# Root node of the tree used for branch and bound
root = SolutionNode(0,0,0,0,None)

# stack/LIFO queue used to store nodes of interest before branching from them
stack = [root]

# Two variables used for performance testing
terminal_nodes_visited = 0
nodes_visited = 0

# Loop until no more nodes are placed on the stack
while (not(len(stack) == 0)):

    current_node = stack.pop(0)
    nodes_visited += 1

    # Check if the popped node is a terminal node
    if (current_node.solution()):

        terminal_nodes_visited += 1

        # Update best found so far only if the current node has a better cost than the best found so far
        if (current_node.cost < best_cost):
            best_cost = current_node.cost
            best_solution = current_node

    else:

        # Branch, then place only nodes satisfying bound and constraint condition on the stack
        for node in current_node.branch():
            if node.bound() <= best_cost:
                cons = node.constraint()
                if (cons <= U_rm):
                    node.cons = cons
                    stack.insert(0,node) # Stack push operation
            else:
                # Because the cache partition sizes are sorted, we know that if a cache size fails the the bound test,
                # all succeeding partition sizes will also fail, so we can break out of the foor loop and save some cycles here.
                break


    if (nodes_visited >= 7.4 * 10**20):
        print("timed out")
        break


end_time = time.perf_counter()
total_time = end_time - start_time
print(f"Best solution node: i: {best_solution.i}, j: {best_solution.j}, cost: {best_solution.cost}, cons: {best_solution.cons}")
print(f"number of calls to cij: {C_ij.nbr_calls:.3E}, number of calls to valgrind: {C_ij.nbr_valgrind_calls}")
print(f"end nodes visited: {terminal_nodes_visited:.3E}")
print(f"nodes visited: {nodes_visited:.3E}")
print(f"execution time: {total_time}")

print("Every node moving up from the bottom is:")
aux = best_solution
while (not(aux == None)):
    print(f"i: {aux.i}, j: {aux.j}")
    aux = aux.parent

import comparison

print(f"total number of end nodes: {comparison.nbr_extreme_nodes:.3E}")
print(f"total number of nodes: {comparison.nbr_nodes:.3E}")
