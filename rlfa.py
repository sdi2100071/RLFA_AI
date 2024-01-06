import csp
import sys
from csp import *
# from utils import argmin_random_tie, count, first, extend

class rlfa(csp.CSP):
        
    def __init__(self,variables, domains, neighbors,constraints, cons):
        
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.cons = cons
        self.weight = {}   
        self.confSet = {key: set() for key in self.variables}
        self.pastFc = {key: set() for key in self.variables}
        self.ngSet = set()
        
        for var in self.variables:
            for n in self.neighbors[var]:
                self.weight[(var, n)] = 1
        
    
        csp.CSP.__init__(self, variables, domains, neighbors, constraints)
    
    # def restore_sets(csp):
    #     """Undo a supposition and all inferences from it."""
    #     csp.confSet = { key : set() for key in csp.variables }
    def choices(csp, var):
        """Return all values for var that aren't currently ruled out."""
        return (csp.curr_domains or csp.domains)[var]
    
    def dom_wdeg(assignment, csp):
        
        # wdeg = {key : 1 for key in csp.variables } 
        min = sys.maxsize
        minv = 0
        
        for var in csp.variables:
            
            wdeg = 0          
            domSize = len(rlfa.choices(csp, var))  
            if var not in assignment:
                for n in csp.neighbors[var]:
                    if n not in assignment:
                        wdeg += csp.weight[(var, n)]
            
                # print (wdeg)
                if wdeg == 0:
                    wdeg = 1

                eval = domSize/wdeg
                if eval < min:
                    min = eval
                    minv = var
                
        return minv
     
    
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
      
    
    def forward_checking(csp, var, value, assignment, removals):
        """Prune neighbor values inconsistent with var=value.""" 
        csp.support_pruning()
        for B in csp.neighbors[var]:
            if B not in assignment:
                for b in csp.curr_domains[B][:]:
                    if not csp.constraints(var, value, B, b, csp.neighbors, csp.cons):                 
                        #add inconcistent var in neighbors PAST FC SET
                        csp.pastFc[B].add(var) 
                        csp.prune(B, b, removals)
                
                if not csp.curr_domains[B]:  
                    #update Conflict Set of current variable var
                    csp.confSet[var] = csp.confSet[var].union(csp.pastFc[B])
                  
                    csp.weight[(var, B)] += 1 #allagh
                    csp.weight[(B, var)] += 1 #allagh
                    
                    return False
                
        return True
                
            
  

    def cbj_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):

        def backtrack(assignment):
            print(csp.nassigns)
            if len(assignment) == len(csp.variables):
                return assignment
            var = select_unassigned_variable(assignment, csp)
            for value in order_domain_values(var, assignment, csp): 
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    
                    if result is not None:                    
                        return result
                    
                    if var not in csp.ngSet:
                        csp.unassign(var, assignment)
                        csp.restore(removals)
                        return None
                                            
                    deepVar = var
                    csp.confSet[deepVar] = csp.confSet[deepVar].union(csp.ngSet) - {deepVar}
                    for v in csp.pastFc[deepVar]: 
                        csp.confSet[v] = set()
            

                csp.restore(removals)
                csp.unassign(var, assignment)
            
            csp.ngSet = csp.confSet[var].union(csp.pastFc[var])
            return None

        result = backtrack({})
        assert result is None or csp.goal_test(result)
        return result



