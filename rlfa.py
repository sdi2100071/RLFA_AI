import operator
import csp

from utils import argmin_random_tie, count, first, extend

class rlfa(csp.CSP):
            
        def constraints(A, a, B, b, neighbors, cons):

            ops = { "=": operator.eq, ">": operator.gt } 
            
            ind = neighbors[A].index(B)
            cond = cons[A][ind]    
            sub = abs(a - b)
            res = int(cond[1])

            if ops[cond[0]](sub, res):
                return True
            else:
                return False  
        def __init__(self,variables, domains, neighbors, cons):
            
            self.variables = variables
            self.domains = domains
            self.neighbors = neighbors
            self.cons = cons
            csp.CSP.__init__(self, variables, domains, neighbors, self.constraints)