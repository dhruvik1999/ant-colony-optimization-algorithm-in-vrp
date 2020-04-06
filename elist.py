import pandas as pd
import numpy as np
from random import randint

#code init
iterations = 1000
ants = 13

#datastructure
graph = []
ph = []
num_node = 0
nodes = []

#param
alpha=0.5
beta=0.5
dens=0.25

def read_data():
	global graph
	global ph
	global num_node
	global nodes

	#reading time matrix from csv file
	dt = pd.read_csv('ip2.csv')
	graph = dt.to_numpy()
	num_node = len(graph)
	temp = []

	#initiallization of 
	for i in range(num_node):
		ph.append([1 for i in range(num_node)])

	#initiallization of all nodes
	nodes = [ i for i in range(num_node) ]

def start_ant(nvis,dpot):
	global graph
	global ph
	global num_node
	global nodes

	# init, cp(current position) is dpot.
	cp=dpot
	path = []
	path.append(cp)
	# This loop makes ant to visit each&every vertex. By the time visiting the vertex, it will remove the vertex from nvis(not visited list).
	while len(nvis)!=0:
		#count the probabilities of non visited vertex.
		probabilities = list(map(lambda x: ( ( ( (ph[cp][x])**alpha)*((1/graph[cp][x])**beta))  ) , nvis))
		probabilities = probabilities/np.sum(probabilities)  

		# counting next vertex in the bases of heigest probability.
		cp=nvis[0]
		mm=probabilities[0]
		for i in range(len(probabilities)):
			if probabilities[i] >mm:
				mm=probabilities[i]
				cp=nvis[i]
		# appending next vertex in path and removing from the list of non visited vertex.
		path.append(cp)
		nvis.remove(cp)
	#returning the path of individual ant.
	return path

def update_feromone(dpot,best_solution,shortest_dist):
	# for all the edge, decresing the level of feromone.
	for i in range(num_node):
		for j in range(num_node):
			ph[i][j] -= (1-dens)*ph[i][j]
			# if the feromone level become 0 then it will not appropriate for the probability count.
			# So, I've taken 0.0000000001 insted of 0. 
			if ph[i][j]<=0:
				ph[i][j]=(10**(-10))

	# cp is current position
	# starting from dpot which is 0 by default.
	cp = dpot

	#end of the path is also dpot(0). so, i'm appending mnly.
	best_solution[1].append(dpot)
	#path = [1,2,3,4,0]
	# 0-1
	# 1-2
	# 2-3
	# 3-4
	# 4-0

	# taking each edges in best path and updating feromone level.
	for x in best_solution[1]:
		if cp != x:
			#Q=1,l=graph[cp][x]
			ph[cp][x] += 1/graph[cp][x] + (ants/6)*(1/shortest_dist[0])
			ph[x][cp] = ph[cp][x]
			cp=x

def getWeight(path,dpot):
	# this function counts the summation of the path.
	x=dpot
	weight = 0
	for y in path:
		weight+=graph[x][y]
		x=y
	weight+=graph[x][dpot]
	return weight

def get_best_solution(solution):
	# this function returns path which has min length.
	ma=solution[0]
	for soln in solution:
		if ma[0]>soln[0]:
			ma=soln
	return ma

def opt_2(path):
	#making 2 path. temp_path is old path. "path" is the path where all the 2-opt changes gonna happen.
	temp_path = path.copy()

	# path = [2,3,4,5,2,3,0]
	# selecting rendomly node from the path and removing that node.
	rnd_node = np.random.choice(path[:-1])
	path.remove(rnd_node)

	#inserting the selected node randomaly.
	path.insert( randint(0, len(path[:-1])) ,rnd_node)

	#path = [ 2,5,3,4,2,3,0]
	
	#If the new path has less cost than old one, update the  path by returning new one.
	if getWeight(temp_path,0) > getWeight(path,0):
		return path
	else:
		return temp_path

def start_spreading_ants(nvis,shortest_dist):
	global graph
	global ph
	global num_node
	global nodes

	#solution will store all the paths which are coverd by 13 ants.
	solution = []

	for i in range(ants):
		#nvis is list of not visited nodes.
		nnvis = nvis.copy()
		#selecting randome starting point.
		dpot = np.random.choice(nnvis)
		nnvis.remove(dpot)
		#ant will start from the mentioned dpot.
		path = start_ant(nnvis,dpot)
		# path = opt_2(path)
		solution.append( (getWeight(path,0),path) )

	# "get_best_solution" will return shortest path coverd among all the ants.
	best_solution = get_best_solution(solution)

	# "opt_2" will apply 2-opt method on best solution.
	opt_best_solution = opt_2(best_solution[1])
	# upedating the best solution.
	#todo:
	best_solution = ( getWeight(opt_best_solution,0) , opt_best_solution )
	
	#updating the shortest distance.
	if shortest_dist[0] > best_solution[0]:
		shortest_dist=best_solution

	#This will update the feromone level.
	update_feromone(0,best_solution,shortest_dist)
	return shortest_dist

def main():
	global alpha
	global beta
	global dens
	global iterations

	#taking input from user
	print("------------------------------------------------------------------")
	veh1 = input("Vehical 1's nodes :").split(' ')
	veh2 = input("Vehical 2's nodes :").split(' ')
	veh3 = input("Vehical 3's nodes :").split(' ')

	veh1 = [ int(i) for i in veh1 ]
	veh2 = [ int(i) for i in veh2 ]
	veh3 = [ int(i) for i in veh3 ]

	# veh1 = [1,4,6,9,10,12]
	# veh2 = [8,11,13,2,5]
	# veh3 = [3,7]

	print("alpha:",alpha, " | beta:", beta, " | density",dens, " | Iterations: ",iterations, " | ants:",ants)

	# code for n number of iteration
	for itr in range(500):
		read_data()

		iterations=itr
		#iteration = 1
		# for n number of iterations, spreading ants in the graph.
		shortest_dist = (10**200,[])

		for _ in range(iterations):
			# this will start spreading ants in the graph.This will return shortest distance of all the previous iterations
			shortest_dist = start_spreading_ants(veh1,shortest_dist)
		sd1=shortest_dist

		shortest_dist = (10**200,[])
		for _ in range(iterations):
			# this will start spreading ants in the graph.This will return shortest distance of all the previous iterations
			shortest_dist = start_spreading_ants(veh2,shortest_dist)
		sd2=shortest_dist

		shortest_dist = (10**200,[])
		for _ in range(iterations):
			# this will start spreading ants in the graph.This will return shortest distance of all the previous iterations
			shortest_dist = start_spreading_ants(veh3,shortest_dist)
		sd3=shortest_dist

		#printing result, shortest distance of all the vehicals.
		print(itr,",",sd1[0],",",sd2[0],",",sd3[0])

if __name__ == '__main__':
	main()


	
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

#TODO
#1. name of variables(ACC to problem)
#2. MM ideal time.