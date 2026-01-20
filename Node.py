# Implements the nodes of the B&B tree
from constants import n, S, D
from Cij import C_ij

class SolutionNode:
    def __init__(self, i,j, cost, cons, parent):
        self.i = i
        self.j = j
        self.cost = cost
        self.cons = cons
        self.parent = parent

    # Classic B&B bound() function
    def bound(self):
        return self.cost + (n-self.i)*S[0]

    # Returns true if node is a terminal node
    def solution(self):
        return (self.i == n)

    # Classic B&B branch() function
    def branch(self):
        nodes = list(range(len(S)))

        for l in range(len(S)):
            nodes[l] = SolutionNode(self.i + 1, l, self.cost + S[l], 0, self)
            # Note: cons is set to 0 here because we want to calculate the true cons as
            # rarely as possible. It is therefore conditionally calculated and set later
            # using the .constraint() member function

        return nodes

    # Calculates the cons field of a node.
    def constraint(self):
        return self.parent.cons + C_ij.get_Cij(self.i,self.j) / D[self.i]

    
