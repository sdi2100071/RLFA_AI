import csp
import sys
from csp import *
# from utils import argmin_random_tie, count, first, extend

class rlfa(csp.CSP):
        
    def __init__(self,variables, domains, neighbors,constraints, cons, weight, confSet):
        
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.cons = cons
        self.weight = weight
        self.confSet = confSet
    
        csp.CSP.__init__(self, variables, domains, neighbors, constraints)
    
    def dom_wdeg(assignment, csp):
        
        # wdeg = {key : 1 for key in csp.variables } 
        min = sys.maxsize
        minv = 0
        if csp.curr_domains is None:
            return first_unassigned_variable(assignment, csp)
        
        for var in csp.variables:
            wdeg = 1          
            domSize = len(csp.curr_domains[var])  
            if var not in assignment:
                for n in csp.neighbors[var]:
                    if n not in assignment:
                        wdeg += csp.weight[(var, n)]
            
                # print (wdeg)
                eval = domSize/wdeg
                if eval <= min:
                    min = eval
                    minv = var
                
        return minv
    
    def forward_checking(csp, var, value, assignment, removals):
        """Prune neighbor values inconsistent with var=value.""" 
        csp.support_pruning()
        for B in csp.neighbors[var]:
            if B not in assignment:
                for b in csp.curr_domains[B][:]:
                    if not csp.constraints(var, value, B, b, csp.neighbors, csp.cons):
                        #add B in conf set of var
                        csp.confSet[var].add(B)
                        csp.prune(B, b, removals)
                
                if not csp.curr_domains[B]:
                    csp.weight[(var, B)] += 1 #allagh
                    csp.weight[(B, var)] += 1 #allagh
                    return False
                
                if( len(csp.curr_domains[B]) == 0 ):
                    csp.weight[(var, B)] += 1 #allagh
                    csp.weight[(B, var)] += 1 #allagh
                    
        return True
    
    def AC3(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
        """[Figure 6.3]"""
        if queue is None:
            queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
        csp.support_pruning()
        queue = arc_heuristic(csp, queue)
        checks = 0
        while queue:
            (Xi, Xj) = queue.pop()
            revised, checks = revise(csp, Xi, Xj, removals, checks)
            if revised:
                if not csp.curr_domains[Xi]:
                    csp.weight[(Xi, Xj)] += 1 #allagh
                    csp.weight[(Xj, Xi)] += 1 #allagh
                    return False # CSP is inconsistent
                for Xk in csp.neighbors[Xi]:
                    if Xk != Xj:
                        queue.add((Xk, Xi))
        return True  # CSP is satisfiable
    
    def mac(csp, var, value, assignment, removals, constraint_propagation=AC3):
        """Maintain arc consistency."""
        return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)
                
            
def cbj_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):
    
    def Cbj(assignment):
        
        if len(assignment) == len(csp.variables):
            return assignment
        
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)          
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = Cbj(assignment)
                    if result is not None:
                        return result
                
                for i in range(1, len(assignment)):
                    if list(assignment)[-i] in csp.confSet[var]:
                        recent = list(assignment)[-i]
                        # csp.confSet[recent].add(csp.confSet[var])
                        csp.confSet[recent] = csp.confSet[recent] - {var}
                        
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = Cbj({})
    assert result is None or csp.goal_test(result)
    return result




