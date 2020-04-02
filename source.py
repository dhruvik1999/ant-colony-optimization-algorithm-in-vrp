import pandas as pd
import numpy as np

iterations = 1000
ants = 22

graph = []
ph = []
num_node = 0
nodes = []

alpha=0.5
beta=0.4
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

	print("\n\nAnt started...")
	cp=dpot
	path = []
	weight = 0
	while len(nvis)!=0:
		mx = (-1,-1)
		check = []
		for i in nvis:
			check.append( ( ((ph[cp][i])**alpha)*((1/graph[cp][i])**beta),i) )
		for i in check:
			if(i[0]>mx[0] or i[0]==mx[0] and ph[cp][i[1]]>=ph[cp][mx[1]] ):
				mx=i
		path.append(mx[1])
		weight += graph[cp][mx[1]]
		cp=mx[1]
		nvis.remove(cp)
	weight += graph[cp][0]
	cp=dpot
	path.append(dpot)
	# print(ph)

	for i in range(num_node):
		for j in range(num_node):
			ph[i][j] -= dens*ph[i][j]

	for i in path:
		ph[cp][i]+=1/weight
		ph[i][cp]=ph[cp][i]
		cp=i
	print("Weight : ", weight)
	print("Dpot : ", dpot)
	print(path)
	return path
	# print(ph)

def start_spreading_ants():
	global graph
	global ph
	global num_node
	global nodes

	for i in range(ants):
		nvis = []
		for i in range(num_node):
			nvis.append(i)
		dpot = np.random.choice(nvis)
		nvis.remove(dpot)
		start_ant(nvis,dpot)

def main():
	read_data()
	for _ in range(iterations):
		start_spreading_ants()


if __name__ == '__main__':
	main()