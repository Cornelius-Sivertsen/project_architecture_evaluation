from constants import n, S, D
from Cij import C_ij

class SolutionNode:
    def __init__(self, i,j, cost, cons, parent):
        self.i = i
        self.j = j
        self.cost = cost
        self.cons = cons
        self.parent = parent

    def bound(self):
        return self.cost + (n-self.i)*S[0]

    def solution(self):
        return (self.i == n)

    def branch(self):
        nodes = list(range(len(S)))

        for l in range(len(S)):
            nodes[l] = SolutionNode(self.i + 1, l, self.cost + S[l], 0, self)

        return nodes

    def constraint(self):
        return self.parent.cons + C_ij.get_Cij(self.i,self.j) / D[self.i]

    
