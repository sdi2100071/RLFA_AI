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
    # print(domains)
    # print(variables)
        
        
    