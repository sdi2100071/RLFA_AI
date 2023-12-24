import operator
import csp

from utils import argmin_random_tie, count, first, extend

class rlfa(csp.CSP):
    
    def __init__(self,variables, domains, neighbors,constraints, cons):
        
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.cons = cons
    
        csp.CSP.__init__(self, variables, domains, neighbors, constraints)
              
    def dom_dweg():
        
        
        
        return 