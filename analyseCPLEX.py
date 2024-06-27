import json

"""
analyseCPLEX.py
Program to get important data from a CPLEX stdout file

Note - getData function is based off another repository, didn't use in my project
    as I found it AFTER MANUALLY CALCULATING ALL THE VALUES however it does work
    as I checked with this program and it matched what I had found.
"""

def getData(filename):
    """Returns important data from CPLEX file"""
    with open(filename, 'rb') as f:
        data = f.read()
    result = data.decode("utf-8").split()
    
    start = result.index("Incumbent")
    load = {}
    links = []
    link_count = 0
    capacities = {}
    capacities = {'max':[0,[]]}
    max_capacity = 0.0
    for i in range(1,8):
        load[i] = float(0)
    for n in result[start:]:
        if n.startswith('x'):
            transit_node = int(n[2])
            x_index = result.index(n)
            load[transit_node] += float(result[x_index+1])
        if (n.startswith('c') or n.startswith('d')) and len(n) == 3:
            cap_index = result.index(n)
            capacity = float(result[cap_index+1])
            if capacity > 0:
                link_count += 1
                links.append(n)
            if capacity == max_capacity:
                capacities['max'][1].append(n)            
            if capacity > max_capacity:
                max_capacity = capacity
                capacities['max'][0] = max_capacity
                capacities['max'][1]= [n]
                                                    
    data = 'Load on transit nodes: '+json.dumps(load)+'\n'+'Maximum capacity: '+json.dumps(capacities)+'\nNon-zero capacity link count: '+str(link_count)+'\nNon-zero capacity links: '+' '.join(links)                                  
    return data


def main():
    """Run"""
    result = getData("737CPLEX.txt")
    f = open("737CPLEXdata.txt",'w')
    f.write(result)
    f.close()
    
    result = getData("747CPLEX.txt")
    f = open("747CPLEXdata.txt",'w')
    f.write(result)
    f.close()
    
    result = getData("757CPLEX.txt")
    f = open("757CPLEXdata.txt",'w')
    f.write(result)
    f.close()
    
    result = getData("767CPLEX.txt")
    f = open("767CPLEXdata.txt",'w')
    f.write(result)
    f.close()
    
    result = getData("777CPLEX.txt")
    f = open("777CPLEXdata.txt",'w')
    f.write(result)
    f.close()
    return

if (__name__ == "__main__"):
    main()
    