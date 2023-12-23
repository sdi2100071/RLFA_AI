import csp
import csv
import operator

def constraints(A, a, B, b, neighbors, cons):

    ind = neighbors[A].index(B)
    cond = cons[A][ind]    
    print(ind)   
    ops = { "=": operator.eq, ">": operator.gt } 
    sub = abs(a - b)
    res = int(cond[1])
    if ops[cond[0]](sub, res):
        return True
    else:
        return False   
    

if __name__ == "__main__":
    
#file import 
 
    path = "C:\\Users\\mikae\\OneDrive\\Υπολογιστής\\5th_semmester\\AI\\RLFA_AI\\rlfap\\var2-f24.txt"
    with open(path, 'r') as var:
        lines = var.readlines()
    
    temp = []
    variables = []
    for line in lines:
        asList = line.split(", ")
        temp.append(asList[0].replace("\n",""))
    
    for i in range(1, len(temp)):
        variables.append(temp[i].split(" ")[0])
    
   
    path = "C:\\Users\\mikae\\OneDrive\\Υπολογιστής\\5th_semmester\\AI\\RLFA_AI\\rlfap\\dom2-f24.txt"
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
    
    path = "C:\\Users\\mikae\\OneDrive\\Υπολογιστής\\5th_semmester\\AI\\RLFA_AI\\rlfap\\ctr2-f24.txt"
    with open(path, 'r') as cons:
        lines = cons.readlines()
        
    # print(lines)
    temp= []
    for line in lines:
        asList = line.split(", ")
        temp.append(asList[0])
    
    neighbors = {key: [] for key in variables} 
    cons = {key: [] for key in variables}   
    for i in range(1, len(temp)):
        key = temp[i].split(" ")[0]
        neighbors[key].append(temp[i].split(" ")[1])
        cons[key].append([temp[i].split(" ")[2], temp[i].split(" ")[3].replace("\n","")])
        neighbors[temp[i].split(" ")[1]].append(key)
        cons[temp[i].split(" ")[1]].append([temp[i].split(" ")[2], temp[i].split(" ")[3].replace("\n","")])
        
    
    b = constraints('2', 1, '1' , 86, neighbors, cons)
    print(b)
    
    variables  = list(map(int, variables)) 
    neighbors = {int(key):[int(i) for i in val]
       for key, val in neighbors.items()}
    
    # print(temp[1].split(" ")[3])
    
    
            
        
    