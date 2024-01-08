import csp
import sys
import time

from csp import *

class rlfa(csp.CSP):
        
    def __init__(self,variables, domains, neighbors,constraints, cons):
        
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.cons = cons #dict { var: [conditions] ex. [['>','2],[etc]] }
                         #                             neighbor1 , neighbor2 ...
       
        self.weight = {}   
        self.confSet = {key: set() for key in self.variables}
        self.pastFc = {key: set() for key in self.variables}
        self.ngSet = set()
       
        self.start_time = None
        self.end_time = None
        self.checks = 0
        
        for var in self.variables:
            for n in self.neighbors[var]:
                self.weight[(var, n)] = 1
    
        csp.CSP.__init__(self, variables, domains, neighbors, constraints)
    
   
    def choices(csp, var):
        """Return all values for var that aren't currently ruled out."""
        return (csp.curr_domains or csp.domains)[var]
    
    
    #heuristic domain weighted degree
    def dom_wdeg(assignment, csp):
        
        min = sys.maxsize
        minv = 0 #min var
        
        for var in csp.variables:
            
            #sum of weights
            wdeg = 0          
            
            #for each unassighned var, sum the weights of each constraint including her and another unassighned neighbor
            if var not in assignment:
                for n in csp.neighbors[var]:
                    if n not in assignment:
                        wdeg += csp.weight[(var, n)]
            
                if wdeg == 0 :
                    wdeg = 1
            
                # evaluation value = size of current domain / weight degree
                domSize = len(rlfa.choices(csp, var))  
                eval = domSize/wdeg
                
                #find var with min evaluation value
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
                    #weight : dict{(x,y): counter } (x,y):constraint (two way assosiation)
                    csp.weight[(Xi, Xj)] += 1
                    csp.weight[(Xj, Xi)] += 1
                    return False # CSP is inconsistent
                
                for Xk in csp.neighbors[Xi]:
                    if Xk != Xj:
                        queue.add((Xk, Xi))
        return True  # CSP is satisfiable
       
    

    def mac(csp, var, value, assignment, removals, constraint_propagation=AC3): #<-- AC3 instead of AC3b
        """Maintain arc consistency."""
        return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)
      
      
    def revise(csp, Xi, Xj, removals, checks=0):
        """Return true if we remove a value."""
        revised = False
        for x in csp.curr_domains[Xi][:]:
            # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
            # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            conflict = True
            for y in csp.curr_domains[Xj]:    
                #counter of constraint checks
                csp.checks += 1       #<--- the only change
                
                if csp.constraints(Xi, x, Xj, y, csp.neighbors, csp.cons):
                    conflict = False
                checks += 1
                if not conflict:
                    break
           
            if conflict:
                csp.prune(Xi, x, removals)
                revised = True
        return revised, checks
    
    
    def forward_checking(csp, var, value, assignment, removals):
        """Prune neighbor values inconsistent with var=value.""" 
        csp.support_pruning()
        for B in csp.neighbors[var]:
            if B not in assignment:
                for b in csp.curr_domains[B][:]:
                    csp.checks += 1
                    if not csp.constraints(var, value, B, b, csp.neighbors, csp.cons):                 
                        # add inconcistent var in neighbor's past_fc set(set of vars that prunned one or more values from var)
                        csp.pastFc[B].add(var) 
                        
                        csp.prune(B, b, removals)
                
                if not csp.curr_domains[B]:  
                    # update Conflict Set of current variable var maintaining the vars affected(prunnded values) by B
                    csp.confSet[var] = csp.confSet[var].union(csp.pastFc[B])

                    # weight : dict{(x,y): counter } (x,y):constraint (two way assosiation)
                    csp.weight[(var, B)] += 1
                    csp.weight[(B, var)] += 1 
                    
                    return False
                
        return True
                
    # source paper: 
    def cbj_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):

        csp.start_time = time.perf_counter()
        def backtrack(assignment):

            if len(assignment) == len(csp.variables):
                return assignment
           
            var = select_unassigned_variable(assignment, csp)
            for value in order_domain_values(var, assignment, csp): 
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    
                    # found result
                    if result is not None:                    
                        return result
                    
                    # if var not in no - good set --> havent found the deepest var of the no good set --> backtrack more
                    if var not in csp.ngSet:
                        csp.unassign(var, assignment)
                        csp.restore(removals)
                        return None
                   
                    # if in no good set --> found the deepest(that we must backtrack) var in no good set                      
                    deepVar = var
                    
                    # update confSet of deep var by adding the vars in ng set (vars that caused dom wipe out in curr var) in it
                    csp.confSet[deepVar] = csp.confSet[deepVar].union(csp.ngSet) - {deepVar}
                    
                    #restore conflict sets of vars in past_fc of the deepVar to remove association with vars that it affected 
                    for v in csp.pastFc[deepVar]: 
                        csp.confSet[v] = set()

                csp.restore(removals)
                csp.unassign(var, assignment)
                
            #domain of var wiped out --> update ng set by merging (confset,pastFc) <-- the reason of dom wipe out is in there
            csp.ngSet = csp.confSet[var].union(csp.pastFc[var])
            return None

        result = backtrack({})
        csp.end_time = time.perf_counter()
        assert result is None or csp.goal_test(result)
        return result
    
    
    def backtracking_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):
        
        csp.start_time = time.perf_counter()    #<---- the only change

        def backtrack(assignment):
            if len(assignment) == len(csp.variables):
                return assignment
            var = select_unassigned_variable(assignment, csp)
            for value in order_domain_values(var, assignment, csp):
                if 0 == csp.nconflicts(var, value, assignment):
                    csp.assign(var, value, assignment)
                    removals = csp.suppose(var, value)
                    if inference(csp, var, value, assignment, removals):
                        result = backtrack(assignment)
                        if result is not None:
                            return result
                    csp.restore(removals)
            csp.unassign(var, assignment)
            return None

        result = backtrack({})
        csp.end_time = time.perf_counter()  #<---- the only change
        assert result is None or csp.goal_test(result)
        return result



