import pandas as pd
import numpy as np
from random import randint
import matplotlib.pyplot as plt

#code init
iterations = 25
ants = 100
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
all_st = {}

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

def update_feromone(dpot,best_solution,shortest_time):
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
			ph[cp][x] += 1/graph[cp][x] + (ants/6)*(1/shortest_time[0])
			ph[x][cp] = ph[cp][x]
			cp=x

def total_traveltime(path,dpot):
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
	bs=solution[0]
	for soln in solution:
		if bs[0]>soln[0]:
			bs=soln
	return bs

def opt_2(path):
	#making 2 path. temp_path is old path. "path" is the path where all the 2-opt changes gonna happen.
	temp_path = path.copy()

	#temp_path,path

	# path <- 2-opt

	# path = [2,3,4,5,2,3,0]
	# selecting rendomly node from the path and removing that node.
	rnd_node = np.random.choice(path[:-1])
	path.remove(rnd_node)

	#inserting the selected node randomaly.
	path.insert( randint(0, len(path[:-1])) ,rnd_node)

	#path = [ 2,5,3,4,2,3,0]
	# return temp_path
	#If the new path has less cost than old one, update the  path by returning new one.
	if total_traveltime(temp_path,0) > total_traveltime(path,0):
		return path
	else:
		return temp_path

def select_nodes(path):
	#1--3-4-5-6
	# 3 = 66
	# 1 = 50
	inds = []
	cp=0
	# path = 0-1-2 = 0-2
	# time(0,1) + time(1,2) - time(0,2)
	# ans = [ (-50,2) , ( -100 , 1 )  ]
	for i in range(0,len(path)-1):
		change = graph[path[cp]][path[i]]+graph[path[i]][ path[i+1] ]-graph[path[cp]][path[i+1]]
		inds.append( (-1*change, path[i] ) )
		cp=i
	inds.sort()
	#ans = [ (-100,1) , (-50,2) ]
	return inds

def start_spreading_ants(nvis,shortest_time,veh_type,itr,limit):
	global graph
	global ph
	global num_node
	global nodes

	global veh1
	global veh2
	global veh3
	global all_st


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
		path = opt_2(path)
		solution.append( (total_traveltime(path,0),path) )

	# "get_best_solution" will return shortest path coverd among all the ants.
	best_solution = get_best_solution(solution)

	# "opt_2" will apply 2-opt method on best solution.
	opt_best_solution = opt_2(best_solution[1])
	# upedating the best solution.
	#todo:
	best_solution = ( total_traveltime(opt_best_solution,0) , opt_best_solution )

	# print("best",best_solution)
	ID = 240-best_solution[0]
	# if the idle time is positive and pass the given condition then only we can apply idle time optimization
	if itr>limit and ID>0:
		if veh_type==2:
			from_veh_type = 1
			inds = []

			# if the idle time is greater then twt/4, then only vehicle can adopt the node from othervehivle
			# this is minimum cindition

			while 25 <= ID:
				# select node will return the list of node of from_veh_type_type
				# this list of node is sorted inorder to get the node which decrease the traveling time most
				inds = select_nodes(all_st[from_veh_type][1])
				# inds = [ (-100,1) , (-50,2) ]
				#lock is use to terminate the while loop. if the vehicle is not able to adopt any node from other vehicle
				lock = True

				for ind in inds:
					#ind = (-100,1)
					#slp = second last position
					#lp = last position
					# for exaample path : 1-2-3-4-5-6 then slp=5, lp=6
					slp = best_solution[1][-2]
					lp = best_solution[1][-1]

					#checking that after adding one node, the total time of the path is less then 240 or not
					if graph[slp][ind[1]]+graph[ind[1]][lp]-graph[slp][lp]+best_solution[0] < twt:
						#lock is false because we found one node which is adopted by the vehicle
						lock=False
						#removing and updating the node from the solution of from vehicle
						all_st[from_veh_type][1].remove(ind[1])
						all_st[from_veh_type]=(total_traveltime(all_st[from_veh_type][1],0),all_st[from_veh_type][1])
						
						#appending the new node in the vehicle's path, and updating the best solution of this vehicle.
						veh2.append(ind[1])
						all_st[2][1].remove(0)
						all_st[2][1].append(ind[1])
						all_st[2][1].append(0)
						all_st[2]=(total_traveltime(all_st[2][1],0) , all_st[2][1] )
						
						#after adding new node, updating the best solution.
						shortest_time=all_st[2]
						best_solution=all_st[2]
						veh1.remove(ind[1])
						# counting IDLE time again, if the idle time is more than twt/4, then again we will adopt one more node.
						ID = 240-best_solution[0]
						break
				# if vehicle not able to adopt any node then we will break the current while loop
				if lock:
					break
		elif veh_type==3:
			inds = []
			# checking basic condition for single node adoption.
			while 25<=ID:
				#lock is use to terminate the while loop. if the vehicle is not able to adopt any node from other vehicle
				lock = True
				
				# vehicle 3 can adopt node for either vehicle1 or vehicle2
				# counting idle time for both vehicles, 
				ID1 = 240 - all_st[1][0]
				ID2 = 240 - all_st[2][0]
				from_veh_type = -1

				#which ever vehicle has higher value we will adopt node from that vehicle.
				if ID1>ID2:
					from_veh_type=2
				else:
					from_veh_type=1

				# selectiong node from selected vehicle
				# select node will return the list of node of from_veh_type_type
				# this list of node is sorted inorder to get the node which decrease the traveling time most
				inds = select_nodes(all_st[from_veh_type][1])
				
				#iterate through all the nodes and chech the conditions.
				for ind in inds:
					#slp = second last position
					#lp = last position
					# for exaample path : 1-2-3-4-5-6 then slp=5, lp=6
					slp = best_solution[1][-2]
					lp = best_solution[1][-1]

					#checking that after adding one node, the total time of the path is less then 240 or not
					if graph[slp][ind[1]]+graph[ind[1]][lp]-graph[slp][lp]+best_solution[0] < twt:
						#lock is false because we found one node which is adopted by the vehicle
						lock=False
						#removing and updating the node from the solution of from vehicle
						all_st[from_veh_type][1].remove(ind[1])
						all_st[from_veh_type]=(total_traveltime(all_st[from_veh_type][1],0),all_st[from_veh_type][1])
						
						#appending the new node in the vehicle's path, and updating the best solution of this vehicle.
						veh3.append(ind[1])
						all_st[3][1].remove(0)
						all_st[3][1].append(ind[1])
						all_st[3][1].append(0)
						all_st[3]=(total_traveltime(all_st[3][1],0) , all_st[3][1] )
						#after adding new node, updating the best solution.
						shortest_time=all_st[3]
						best_solution=all_st[3]
						#removing the node from from_veh_type_type vehicle
						if from_veh_type==1:
							if ind[1] in veh1:
								veh1.remove(ind[1])
						else:
							if ind[1] in veh2:
								veh2.remove(ind[1])
						# counting IDLE time again, if the idle time is more than twt/4, then again we will adopt one more node.
						ID = 240-best_solution[0]
						break
				# if vehicle not able to adopt any node then we will break the current while loop
				if lock:
					break

	#updating the shortest time
	if shortest_time[0] > best_solution[0]:
		shortest_time=best_solution

	#This will update the feromone level.
	update_feromone(0,best_solution,shortest_time)
	return shortest_time

def main():
	global alpha
	global beta
	global dens
	global iterations

	global veh1
	global veh2
	global veh3
	global all_st

	# init the path of all vehicles
	veh1 = [1, 4, 6, 9, 10, 12]
	veh2 = [8,11,2,13,5]
	veh3 = [3,7]

	#output graph datastructure = x,veh1,veh2,veh3
	output_graph = [ [] , [] , [] , [] ]

	#printing the value of parameters of the algo
	print("alpha:",alpha, " | beta:", beta, " | density",dens, " | Iterations: ",iterations, " | ants:",ants)

	# code for n number of iteration
	limit = randint(4,8)
	for itr in range(iterations):
		read_data()

		iterations=itr

		# for n number of iterations, spreading ants in the graph.
		all_st[1] = (10**200,[])
		all_st[2] = (10**200,[])
		all_st[3] = (10**200,[])


		for ii in range(iterations):
			# this will start spreading ants in the graph.This will return shortest time of all the previous iterations
			all_st[1]= start_spreading_ants(veh1,all_st[1],1,ii,limit)
			all_st[1] = ( total_traveltime( all_st[1][1] , 0 ) , all_st[1][1] )

		for ii in range(iterations):
			# this will start spreading ants in the graph.This will return shortest time of all the previous iterations
			all_st[2] = start_spreading_ants(veh2,all_st[2],2,ii,limit)
			all_st[2] = ( total_traveltime( all_st[2][1] , 0) , all_st[2][1] )


		for ii in range(iterations):
			# this will start spreading ants in the graph.This will return shortest time of all the previous iterations
			all_st[3] = start_spreading_ants(veh3,all_st[3],3,ii,limit)
			all_st[3] = ( total_traveltime( all_st[3][1] , 0) , all_st[3][1] )
			



		#printing result, shortest time of all the vehicals.
		if itr!=0:
			print(itr,all_st)
			output_graph[0].append(itr)
			output_graph[1].append(all_st[1][0])
			output_graph[2].append(all_st[2][0])
			output_graph[3].append(all_st[3][0])

	plt.plot(output_graph[0] , output_graph[1], label="Vehicle 1"  )
	plt.plot(output_graph[0] , output_graph[2], label="Vehicle 2"  )
	plt.plot(output_graph[0] , output_graph[3], label="Vehicle 3"  )
	plt.title("Elist algo")
	plt.legend()
	plt.show()



if __name__ == '__main__':
	main()
