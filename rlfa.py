import csp

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
                    return False
        # print(weight)
        return True
              
    def dom_wdeg(assignment, csp):
        wdeg = {key : 1 for key in csp.variables }
        for var in csp.variables:
            if var not in assignment:
                for n in csp.neighbors[var]:
                    if n not in assignment:
                        wdeg[var] += csp.weight[(var, n)]
        
        return min(wdeg.values())
                
                
        
        
        
    #     return 