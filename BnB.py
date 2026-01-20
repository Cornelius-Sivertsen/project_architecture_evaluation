from constants import n, S, D, U_rm
from Node import SolutionNode
from Cij import C_ij
import time

"""
Implements the branch and bound algorithm to minimize total cache size, with constraint of stability of the given scheduling policy
"""

# Used for performance testing
start_time = time.perf_counter()

# Stores the cost of the best complete solution (terminal node) found so far. Initialized with the worst case solution
best_cost = n*S[-1]

# Stores the terminal node corresponding to the best solution found so far
best_solution = SolutionNode(0,0,0,0,None)

# Root node of the tree used for branch and bound
root = SolutionNode(0,0,0,0,None)

# stack/LIFO queue used to store nodes of interest before branching from them
stack = [root]

# Three variables used for performance testing
terminal_nodes_visited = 0
nodes_visited = 0
max_stack_size = 0

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

    if (nodes_visited % 1000000 == 0):
        print(f"Visited {nodes_visited:.3E} nodes")


    if (len(stack) > max_stack_size):
        max_stack_size = len(stack)
    
    
    if (nodes_visited >= 10**10):
        print(f"Timed out after visiting {nodes_visited} nodes")
        break

# Get execution time information
end_time = time.perf_counter()
total_time = end_time - start_time

# Print found final node
print(f"Best solution node: i: {best_solution.i}, j: {best_solution.j}, cost: {best_solution.cost}, cons: {best_solution.cons}")

# Print perfomance information
print(f"n = {n}")
print(f"k = {len(S)}")
print(f"number of calls to cij: {C_ij.nbr_calls:.3E}, number of calls to valgrind: {C_ij.nbr_valgrind_calls}")
print(f"end nodes visited: {terminal_nodes_visited:.3E}")
print(f"nodes visited: {nodes_visited:.3E}")
print(f"Maximum stack size obtained: {max_stack_size:.3E}")
print(f"execution time: {total_time}")

# Print out the entire path corresponding to the ideal solution
print("Every node moving up from the bottom is:")
aux = best_solution
while (not(aux == None)):
    print(f"i: {aux.i}, j: {aux.j}")
    aux = aux.parent



import comparison

print(f"Total number of terminal nodes in graph: {comparison.nbr_extreme_nodes:.3E}")
print(f"Total mumber of nodes in graph: {comparison.nbr_nodes:.3E}")
