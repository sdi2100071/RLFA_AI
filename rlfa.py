import csp
import sys
from csp import *
from utils import argmin_random_tie, count, first, extend

class rlfa(csp.CSP):
        
    def __init__(self,variables, domains, neighbors,constraints, cons, weight):
        
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.cons = cons
        self.weight = weight
    
        csp.CSP.__init__(self, variables, domains, neighbors, constraints)
    
    
    def forward_checking(csp, var, value, assignment, removals):
        """Prune neighbor values inconsistent with var=value."""
        csp.support_pruning()
        for B in csp.neighbors[var]:
            if B not in assignment:
                for b in csp.curr_domains[B][:]:
                    if not csp.constraints(var, value, B, b, csp.neighbors, csp.cons):
                        csp.prune(B, b, removals)
                if not csp.curr_domains[B]:
                    csp.weight[(var, B)] += 1 #allagh
                    csp.weight[(B, var)] += 1 #allagh
                    return False
        # print(weight)
        return True
              
    def dom_wdeg(assignment, csp):
        
        wdeg = {key : 1 for key in csp.variables }
        min = sys.maxsize
        minv = 0
        
        if csp.curr_domains is None:
            return first_unassigned_variable(assignment, csp)
        
        for var in csp.variables:
            
            domSize = len(csp.curr_domains[var])  
            # print domSize
            if var not in assignment:
                for n in csp.neighbors[var]:
                    if n not in assignment:
                        wdeg[var] += csp.weight[(var, n)]
                        
            eval = domSize/wdeg[var]
            # print(eval)
            if eval <= min:
                min = eval
                minv = var
            
        # print(wdeg)
        # print(minv) 
        return minv
         
