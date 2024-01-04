import csp
import rlfa
import csv
import operator

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

if __name__ == "__main__":
    
#file import 

    path = "rlfap\\dom2-f24.txt"
    with open(path, 'r') as dom:
        lines = dom.readlines()
    
    doms = []
    for line in lines:
        asList = line.split(", ")
        doms.append(asList[0].replace("\n",""))
    
    domains = {}
    for i in range(1, len(doms)):
        vars = []
        key = doms[i].split(" ")[0]
        for j in range(1, len(doms[i].split(" "))):
            vars.append(doms[i].split(" ")[j])
        domains[key] = vars
 
    domains = {int(key):[int(i) for i in val]
       for key, val in domains.items()}
    
    domvars = domains
    
    path = "rlfap\\var2-f24.txt"
    with open(path, 'r') as var:
        lines = var.readlines()
    
    temp = []
    variables = []
    for line in lines:
        asList = line.split(", ")
        temp.append(asList[0].replace("\n",""))

    
    domains = {}    
    for i in range(1, len(temp)):
        variables.append(temp[i].split(" ")[0])
        key = int(temp[i].split(" ")[0])
        domains[key] = domvars[int(temp[i].split(" ")[1])]

    variables  = list(map(int, variables)) 
        
    path = "rlfap\\ctr2-f24.txt"
    with open(path, 'r') as cons:
        lines = cons.readlines()
        
    temp= []
    for line in lines:
        asList = line.split(", ")
        temp.append(asList[0])
    
    neighbors = {key: [] for key in variables} 
    cons = {key: [] for key in variables}   
    for i in range(1, len(temp)):
        key = int(temp[i].split(" ")[0])
        neighbors[key].append(temp[i].split(" ")[1])
        cons[key].append([temp[i].split(" ")[2], temp[i].split(" ")[3].replace("\n","")])
        neighbors[int(temp[i].split(" ")[1])].append(key)
        cons[int(temp[i].split(" ")[1])].append([temp[i].split(" ")[2], temp[i].split(" ")[3].replace("\n","")])
         
    
    neighbors = {int(key):[int(i) for i in val]
       for key, val in neighbors.items()}
    
    #counter  dictionary
    weight = {}
    confSet = {key: set() for key in variables}
    
    for var in variables:
        for n in neighbors[var]:
            weight[(var, n)] = 1
    
    #----------------------------------------------------------------------------------
    
    
    
    
    
    
    
    rlfap = rlfa.rlfa(variables, domains, neighbors,constraints, cons, weight, confSet)
    
    "FC"
    fc = csp.backtracking_search(rlfap, select_unassigned_variable=rlfa.rlfa.dom_wdeg, inference=rlfa.rlfa.forward_checking)
    
    "MAC"
    mac = csp.backtracking_search(rlfap, select_unassigned_variable=rlfa.rlfa.dom_wdeg, inference=rlfa.rlfa.mac)

    "FC - CBJ"
    # result1 = rlfa.rlfa.cbj_search(x, select_unassigned_variable=rlfa.rlfa.dom_wdeg, inference=rlfa.rlfa.forward_checking)

    print(fc)
    # print(mac)
    
    
    # print(list(set1)[-1])
    # print (csp.ass)
    