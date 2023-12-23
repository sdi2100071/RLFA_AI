import csp
import csv

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
    for i in range(1, len(temp)):
        key = temp[i].split(" ")[0]
        neighbors[key].append(temp[i].split(" ")[1])
        neighbors[temp[i].split(" ")[1]].append(key)
        
    variables  = list(map(int, variables)) 
    neighbors = {int(key):[int(i) for i in val]
       for key, val in neighbors.items()}
    print(neighbors)
    
    
            
        
    