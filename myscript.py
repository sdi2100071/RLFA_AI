import csp
import rlfa
import functions
import sys
import time

if __name__ == "__main__":
        
    variables, neighbors, domains,cons = functions.handle_files()

    #create rlfa prob    
    rlfap = rlfa.rlfa(variables, domains, neighbors,functions.constraints, cons)
    
    method = {"fc_bt" : [rlfa.rlfa.backtracking_search, rlfa.rlfa.forward_checking],
              "mac_bt" : [rlfa.rlfa.backtracking_search, rlfa.rlfa.mac ], 
              "fc_cbj" : [rlfa.rlfa.cbj_search,rlfa.rlfa.forward_checking ]}
    
    search = method[sys.argv[1]][0]
    inf = method[sys.argv[1]][1]
    
    
    "FC"
    # fc = csp.backtracking_search(rlfap, select_unassigned_variable=rlfa.rlfa.dom_wdeg, inference=rlfa.rlfa.forward_checking)
    # print(fc)
    # print(rlfap.nassigns)
    "MAC"
    # mac = csp.backtracking_search(rlfap, select_unassigned_variable=rlfa.rlfa.dom_wdeg, inference=rlfa.rlfa.mac)
    # print(mac)

    "FC - CBJ"
    solution = search(rlfap, select_unassigned_variable=rlfa.rlfa.dom_wdeg, inference = inf)
   
    print("SOLUTION FOR " , sys.argv[1] ,"=" )
    print(solution)
   
    print("-------------------------------------")
   
    print("NUMBER OF ASSIGHNS:")
    print(rlfap.nassigns ,"\n")
    
    print("TIME ELLAPSED:")
    print(rlfap.end_time - rlfap.start_time , "sec")
    