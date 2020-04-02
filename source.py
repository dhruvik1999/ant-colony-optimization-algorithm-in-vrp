import pandas as pd
import numpy as np

graph = []
ph = []
num_node = 0
nodes = []

alpha=1
beta=1
dens=1

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
			# print("AA" ,((ph[cp][i])**alpha)*((1/graph[cp][i])**beta) )
		for i in check:
			if(i[0]>mx[0] or i[0]==mx[0] and ph[cp][i[1]]>=ph[cp][mx[1]] ):
				mx=i
		path.append(mx[1])
		weight += graph[cp][mx[1]]
		cp=mx[1]
		print(cp,len(check))
		nvis.remove(cp)
	weight += graph[cp][0]
	cp=dpot
	path.append(dpot)
	print(ph)

	for i in path:
		ph[cp][i]+=1/weight
		ph[i][cp]=ph[cp][i]
		cp=i
	print("Weight : ", weight)
	print(path)
	print(ph)

def start_spreading_ants(num_ants,dpot):
	global graph
	global ph
	global num_node
	global nodes

	for i in range(num_ants):
		nvis = []
		for i in range(num_node):
			if i != dpot:
				nvis.append(i)
		start_ant(nvis,0)


def main():
	read_data()
	start_spreading_ants(10,0)


if __name__ == '__main__':
	main()