import pandas as pd
import numpy as np
from random import randint
import time

#code init
iterations = 1000
ants = 13
twt = 240


#datastructure
graph = []
ph = []
num_node = 0
nodes = []

#param
alpha=0.5
beta=0.5
dens=0.25

#vehicals path
veh1 = []
veh2 = []
veh3 = []
all_sd = {}

def read_data():
	global graph
	global ph
	global num_node
	global nodes

	#reading time matrix from csv file
	dt = pd.read_csv('ip3.csv')
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
			ph[cp][x] += 1/graph[cp][x] 
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
	return temp_path
	#If the new path has less cost than old one, update the  path by returning new one.
	if getWeight(temp_path,0) > getWeight(path,0):
		return path
	else:
		return temp_path

def select_nodes(path):
	#1--3-4-5-6
	# 3 = 66
	# 1 = 50
	ans = []
	cp=0
	for i in range(0,len(path)-1):
		change = graph[path[cp]][path[i]]+graph[path[i]][ path[i+1] ]-graph[path[cp]][path[i+1]]
		ans.append( (-1*change, path[i] ) )
		cp=i
	ans.sort()
	return ans

def start_spreading_ants(nvis,shortest_dist,veh_type,itr,limit):
	global graph
	global ph
	global num_node
	global nodes

	global veh1
	global veh2
	global veh3
	global all_sd


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
	# opt_best_solution = opt_2(best_solution[1])
	opt_best_solution = best_solution[1]
	# upedating the best solution.
	#todo:
	best_solution = ( getWeight(opt_best_solution,0) , opt_best_solution )

	# print("best",best_solution)
	ID = 240-best_solution[0]
	if itr>limit and ID>0:
		if veh_type==2:
			from_veh = 1
			inds = []

			while twt/4 <= ID:
				inds = select_nodes(all_sd[from_veh][1])
				lock = True
				for ind in inds:
					#slp-lp-0
					#slp-node-lp-0
					slp = best_solution[1][-2]
					lp = best_solution[1][-1]
					if graph[slp][ind[1]]+graph[ind[1]][lp]-graph[slp][lp]+best_solution[0] < twt:
						lock=False
						all_sd[from_veh][1].remove(ind[1])
						all_sd[from_veh]=(getWeight(all_sd[from_veh][1],0),all_sd[from_veh][1])
						veh2.append(ind[1])
						all_sd[2][1].append(ind[1])
						all_sd[2]=(getWeight(all_sd[2][1],0) , all_sd[2][1] )
						shortest_dist=all_sd[2]
						best_solution=all_sd[2]
						veh1.remove(ind[1])
						ID = 240-best_solution[0]
						break
				if lock:
					break
		elif veh_type==3:
			inds = []
			while twt/4<=ID:
				lock = True
				ID1 = 240 - all_sd[1][0]
				ID2 = 240 - all_sd[2][0]
				from_veh = -1

				if ID1>ID2:
					from_veh=2
				else:
					from_veh=1
				inds = select_nodes(all_sd[from_veh][1])
				for ind in inds:
					slp = best_solution[1][-2]
					lp = best_solution[1][-1]
					if ind[1]!=0 and graph[slp][ind[1]]+graph[ind[1]][lp]-graph[slp][lp]+best_solution[0] < twt:
						lock=False
						all_sd[from_veh][1].remove(ind[1])
						all_sd[from_veh]=(getWeight(all_sd[from_veh][1],0),all_sd[from_veh][1])
						veh3.append(ind[1])
						all_sd[3][1].remove(0)
						all_sd[3][1].append(ind[1])
						all_sd[3][1].append(0)
						all_sd[3]=(getWeight(all_sd[3][1],0) , all_sd[3][1] )
						shortest_dist=all_sd[3]
						best_solution=all_sd[3]
						if from_veh==1:
							veh1.remove(ind[1])
						else:
							veh2.remove(ind[1])
						ID = 240-best_solution[0]
						break
				if lock:
					break



		# 	if twt/4 <= ID and ID <twt/2:
		# 		# inds.append( np.random.choice( all_sd[from_veh][1][:-1] ) )
		# 		inds = select_nodes(1,all_sd[from_veh][1])
		# 		# print("----> ", inds)
		# 		all_sd[from_veh][1].remove(inds[0])
		# 		all_sd[from_veh]=(getWeight(all_sd[from_veh][1],0),all_sd[from_veh][1])
		# 		veh3.append(inds[0])
		# 		all_sd[3][1].append(inds[0])
		# 		all_sd[3]=(getWeight(all_sd[3][1],0) , all_sd[3][1] )
		# 		shortest_dist=all_sd[3]
		# 		best_solution=all_sd[3]

		# 		if from_veh==1:
		# 			veh1.remove(inds[0])
		# 		else:
		# 			veh2.remove(inds[0])

		# 	elif twt/2 <= ID and ID < 3*twt/4:
		# 		inds = select_nodes(2,all_sd[from_veh][1])
		# 		all_sd[from_veh][1].remove(inds[0])
		# 		all_sd[from_veh][1].remove(inds[1])
		# 		all_sd[from_veh]=(getWeight(all_sd[from_veh][1],0),all_sd[from_veh][1])
		# 		veh3.append(inds[0])
		# 		veh3.append(inds[1])

		# 		all_sd[3][1].append(inds[0])
		# 		all_sd[3][1].append(inds[0])
		# 		all_sd[2]=(getWeight(all_sd[2][1],0) , all_sd[2][1] )
		# 		shortest_dist=all_sd[2]
		# 		best_solution=all_sd[2]
		# 		if from_veh==1:
		# 			veh1.remove(inds[0])
		# 			veh1.remove(inds[1])
		# 		else:
		# 			veh2.remove(inds[0])
		# 			veh2.remove(inds[1])

		# 	elif 3*twt/4 >= ID:
		# 		pass
		# 	else:
		# 		pass
		# else:
		# 	pass

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

	global veh1
	global veh2
	global veh3
	global all_sd

	#taking input from user
	print("------------------------------------------------------------------")
	# veh1 = input("Vehical 1's nodes :").split(' ')
	# veh2 = input("Vehical 2's nodes :").split(' ')
	# veh3 = input("Vehical 3's nodes :").split(' ')

	# veh1 = [ int(i) for i in veh1 ]
	# veh2 = [ int(i) for i in veh2 ]
	# veh3 = [ int(i) for i in veh3 ]

	veh1 = [1,4,6,9,10,12]
	veh2 = [8,11,13,2,5]
	veh3 = [3,7]

	print("alpha:",alpha, " | beta:", beta, " | density",dens, " | Iterations: ",iterations, " | ants:",ants)

	# code for n number of iteration
	all_sd[1] = (10**200,[])
	all_sd[2] = (10**200,[])
	all_sd[3] = (10**200,[])


	vehs = [[1,4,6,9,10,12],[55,92,20,33,18],[72,51,79,41,39],[98,16,17,76,56],[21,84,52,99,28],[15,93,27,73,24],[53,59,68,82,25,14],[50,38,75,91,97],[90,85,83,74,29],[70,64,54,46,66,81],[45,48,77,86],[8,11,13,2,5],[26,30,43,96],[31,40,58,62],[34,47,95,63],[36,49,60,65,67],[37,44,61],[69,71,78,80],[42,32,23],[19,100,89],[57,88,94],[87,22,35],[3,7]]
	print(vehs)

	ans = {}
	count = {}
	for i in range(23):
		ans[i]=0
		count[i]=0
	total_combinations = 0


	for v1 in range(100) :
		for v2 in range(1):
			for v3 in range(1):


				v1 = np.random.choice([0,1,2,3,4,5,6,7,8,9])
				v2 = np.random.choice([10,11,12,13,14,15,16,17])
				v3 = np.random.choice([18,19,20,21,22])

				total_combinations+=1
				print("----------------------------------------------------------------")
				print(v1,v2,v3)
				count[v1]+=1
				count[v2]+=1
				count[v3]+=1

				limit = randint(40,70)
				all_sd[1] = (10**200,[])
				all_sd[2] = (10**200,[])
				all_sd[3] = (10**200,[])
				veh1 = vehs[v1].copy()
				veh2 = vehs[v2].copy()
				veh3 = vehs[v3].copy()

				read_data()

				t1 = time.time()

				for itr in range(0,75):
					iterations=itr		
					for ii in range(iterations):
						# this will start spreading ants in the graph.This will return shortest distance of all the previous iterations
						all_sd[1]= start_spreading_ants(veh1,all_sd[1],1,itr,limit)
						all_sd[1] = ( getWeight( all_sd[1][1] , 0 ) , all_sd[1][1] )

					for ii in range(iterations):
						# this will start spreading ants in the graph.This will return shortest distance of all the previous iterations
						all_sd[2] = start_spreading_ants(veh2,all_sd[2],2,itr,limit)
						all_sd[2] = ( getWeight( all_sd[2][1] , 0) , all_sd[2][1] )


					for ii in range(iterations):
						# this will start spreading ants in the graph.This will return shortest distance of all the previous iterations
						all_sd[3] = start_spreading_ants(veh3,all_sd[3],3,itr,limit)
						all_sd[3] = ( getWeight( all_sd[3][1] , 0) , all_sd[3][1] )
						
					# printing result, shortest distance of all the vehicals.
					if itr!=0 and all_sd[1][0]<240 and all_sd[2][0]<240 and all_sd[2][0]<240:
						# print(itr,",",sd1[0],",",sd2[0],",",sd3[0])
						print(itr,all_sd,time.time()-t1)

				ans[v1]+=all_sd[1][0]
				ans[v2]+=all_sd[2][0]
				ans[v3]+=all_sd[3][0]
				print("-->ans",ans)
				print("-->count",count)
				input()

				print("--------------------------------------------------------")



	

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