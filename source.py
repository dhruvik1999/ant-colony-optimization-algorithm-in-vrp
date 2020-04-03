import pandas as pd
import numpy as np

iterations = 100
ants = 22

graph = []
ph = []
num_node = 0
nodes = []

alpha=0.8
beta=0.5
dens=0.8

def read_data():
	global graph
	global ph
	global num_node
	global nodes

	print("Ant colony opt for VRP")
	dt = pd.read_csv('ip.csv')
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
		path.append(cp)
		nvis.remove(cp)
	return path

def update_feromone(dpot,best_solution):
	for i in range(num_node):
		for j in range(num_node):
			ph[i][j] -= dens*ph[i][j]
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

def start_spreading_ants(nvis):
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
	print(best_solution)
	update_feromone(0,best_solution)

def main():
	read_data()
	for _ in range(iterations):
		start_spreading_ants([i for i in range(num_node)])
		pass

	print("------------------------------------------------------------------")
	veh1 = input("Vehical 1's nodes :").split(" ")
	veh2 = input("Vehical 2's nodes :").split(" ")
	veh3 = input("Vehical 3's nodes :").split(" ")

	veh1 = [ int(i) for i in veh1 ]
	veh2 = [ int(i) for i in veh2 ]
	veh3 = [ int(i) for i in veh3 ]




if __name__ == '__main__':
	main()