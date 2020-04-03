import pandas as pd
import numpy as np

iterations = 1000
ants = 13

graph = []
ph = []
num_node = 0
nodes = []

alpha=0.5
beta=0.5
dens=0.25

def read_data():
	global graph
	global ph
	global num_node
	global nodes

	# print("Ant colony opt for VRP")
	dt = pd.read_csv('ip2.csv')
	graph = dt.to_numpy()
	num_node = len(graph)
	temp = []

	for i in range(num_node):
		ph.append([1 for i in range(num_node)])
	nodes = [ i for i in range(num_node) ]

def start_ant(nvis,dpot):
	global graph
	global ph
	global num_node
	global nodes
	# print("Ant started...")
	cp=dpot
	path = []
	path.append(cp)
	weight = 0
	while len(nvis)!=0:
		probabilities = list(map(lambda x: ( ( ( (ph[cp][x])**alpha)*((1/graph[cp][x])**beta))  ) , nvis))
		probabilities = probabilities/np.sum(probabilities)  
		cp = np.random.choice(nvis, p=probabilities)
		# cp=nvis[0]
		# mm=probabilities[0]
		# for i in len(probabilities):
		# 	if probabilities[i] >mm:
		# 		mm=probabilities[i]
		# 		cp=nvis[i]
		path.append(cp)
		nvis.remove(cp)
	return path

def update_feromone(dpot,best_solution):
	for i in range(num_node):
		for j in range(num_node):
			ph[i][j] -= (1-dens)*ph[i][j]
			if ph[i][j]<=0:
				ph[i][j]=(10**(-10))

	cp = dpot
	best_solution[1].append(dpot)
	for x in best_solution[1]:
		if cp != x:
			ph[cp][x] += 1/graph[cp][x]
			ph[x][cp] = ph[cp][x]
			cp=x

def getWeight(path,dpot):
	x=dpot
	weight = 0
	for y in path:
		weight+=graph[x][y]
		x=y
	weight+=graph[x][dpot]
	return weight

def get_best_solution(solution):
	ma=solution[0]
	for soln in solution:
		if ma[0]>soln[0]:
			ma=soln
	return ma

def start_spreading_ants(nvis,shortest_dist):
	global graph
	global ph
	global num_node
	global nodes

	
	solution = []
	for i in range(ants):
		nnvis = nvis.copy()
		dpot = np.random.choice(nnvis)
		nnvis.remove(dpot)
		path = start_ant(nnvis,dpot)
		solution.append( (getWeight(path,0),path) )
	best_solution = get_best_solution(solution)
	# print(best_solution)
	if shortest_dist[0] > best_solution[0]:
		shortest_dist=best_solution
	update_feromone(0,best_solution)
	return shortest_dist

def main():
	global alpha
	global beta
	global dens
	global iterations
	# read_data()
	# for _ in range(iterations):
	# 	start_spreading_ants([i for i in range(num_node)])
	# 	pass

	print("------------------------------------------------------------------")
	veh1 = input("Vehical 1's nodes :").split(' ')
	veh2 = input("Vehical 2's nodes :").split(' ')
	veh3 = input("Vehical 3's nodes :").split(' ')

	veh1 = [ int(i) for i in veh1 ]
	veh2 = [ int(i) for i in veh2 ]
	veh3 = [ int(i) for i in veh3 ]

	

	print("alpha:",alpha, " | beta:", beta, " | density",dens, " | Iterations: ",iterations, " | ants:",ants)
	
	# shortest_dist = (10*200,[])
	# for _ in range(iterations):
	# 	shortest_dist = start_spreading_ants(veh1,shortest_dist)
	# sd1=shortest_dist
	# print("Vehical 1 : ",shortest_dist)

	# shortest_dist = (10*200,[])
	# for _ in range(iterations):
	# 	shortest_dist = start_spreading_ants(veh2,shortest_dist)
	# sd2=shortest_dist
	# print("Vehical 2 : ",shortest_dist)

	# shortest_dist = (10*200,[])
	# for _ in range(iterations):
	# 	shortest_dist = start_spreading_ants(veh3,shortest_dist)
	# sd3=shortest_dist
	# print("Vehical 3 : ",shortest_dist)
	# print(",sd1[0],",",sd2[0],",",sd3[0])



	# for q in [0.5]:
	# 	for i in [0.1,0.2,0.3,0.5,0.6,0.8,1]:
	# 		for j in [0.2,0.3,0.5,0.6,0.8,0.9,1]:
	# 			alpha=i
	# 			beta=j
	# 			dens=q
	# 			shortest_dist = (10*200,[])
	# 			for _ in range(iterations):
	# 				shortest_dist = start_spreading_ants(veh1,shortest_dist)
	# 			sd1=shortest_dist
	# 			#print("Vehical 1 : ",shortest_dist)

	# 			shortest_dist = (10*200,[])
	# 			for _ in range(iterations):
	# 				shortest_dist = start_spreading_ants(veh2,shortest_dist)
	# 			sd2=shortest_dist
	# 			#print("Vehical 2 : ",shortest_dist)

	# 			shortest_dist = (10*200,[])
	# 			for _ in range(iterations):
	# 				shortest_dist = start_spreading_ants(veh3,shortest_dist)
	# 			sd3=shortest_dist
	# 			#print("Vehical 3 : ",shortest_dist)
				# print(q,",",i,",",j,",",sd1[0],",",sd2[0],",",sd3[0])

	for itr in range(500):
		read_data()
		iterations=itr
		shortest_dist = (10*200,[])
		for _ in range(iterations):
			shortest_dist = start_spreading_ants(veh1,shortest_dist)
		sd1=shortest_dist
		# print("Vehical 1 : ",shortest_dist)

		shortest_dist = (10*200,[])
		for _ in range(iterations):
			shortest_dist = start_spreading_ants(veh2,shortest_dist)
		sd2=shortest_dist
		# print("Vehical 2 : ",shortest_dist)

		shortest_dist = (10*200,[])
		for _ in range(iterations):
			shortest_dist = start_spreading_ants(veh3,shortest_dist)
		sd3=shortest_dist
		# print("Vehical 3 : ",shortest_dist)
		print(itr,",",sd1[0],",",sd2[0],",",sd3[0])








if __name__ == '__main__':
	main()