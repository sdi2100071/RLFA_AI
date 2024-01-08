import sys
        
def handle_files():
    
    prefix = sys.argv[2]
     
    path = "../rlfap/dom" + prefix + ".txt"
    with open(path, 'r') as domFile:
        lines = domFile.readlines()
    
    #list of lines of the file
    doms = []
    for line in lines:
        asList = line.split(", ")
        doms.append(asList[0].replace("\n",""))
        
    domains = {}
    for i in range(1, len(doms)):
        vars = []
           
        #key = domain number
        key = doms[i].split(" ")[0]
        
        #len(doms[i].split(" ") =  number of var associated with this domain
        for j in range(1, len(doms[i].split(" "))):
            vars.append(doms[i].split(" ")[j])
        domains[key] = vars
    #str --> int
    domains = {int(key):[int(i) for i in val]
       for key, val in domains.items()}  
    
    #dictionary {dom number : values }
    domvars = domains   
    domFile.close()
    
    
    path = "../rlfap/var" + prefix + ".txt"
    with open(path, 'r') as varFile:
        lines = varFile.readlines()
    
    temp = []
    for line in lines:
        asList = line.split(", ")
        temp.append(asList[0].replace("\n",""))

    domains = {}    
    variables = []
    for i in range(1, len(temp)):
        variables.append(temp[i].split(" ")[0])
        key = int(temp[i].split(" ")[0])
        #dictionary {variable : values}
        domains[key] = domvars[int(temp[i].split(" ")[1])]
    
    #str ->int
    variables  = list(map(int, variables)) 
    varFile.close()

    path = "../rlfap/ctr" + prefix + ".txt"
    with open(path, 'r') as consFile:
        lines = consFile.readlines()
        
    temp= []
    for line in lines:
        asList = line.split(", ")
        temp.append(asList[0])
        
    neighbors = {key: [] for key in variables} 
    #cons: dictionary { var: [conditions] ex. [['>','2],[etc]] }
    cons = {key: [] for key in variables}   
    for i in range(1, len(temp)):
        key = int(temp[i].split(" ")[0])
        
        neighbors[key].append(temp[i].split(" ")[1])
        cons[key].append([temp[i].split(" ")[2], temp[i].split(" ")[3].replace("\n","")])
       
        #keep two - way association
        neighbors[int(temp[i].split(" ")[1])].append(key)
        cons[int(temp[i].split(" ")[1])].append([temp[i].split(" ")[2], temp[i].split(" ")[3].replace("\n","")])
         
    neighbors = {int(key):[int(i) for i in val]
       for key, val in neighbors.items()}
    
    consFile.close()
    
    return variables, neighbors, domains, cons
    
    
