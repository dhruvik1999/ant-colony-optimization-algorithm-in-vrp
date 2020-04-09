import pandas as pd
import numpy as np
from random import randint
import matplotlib.pyplot as plt

#code init
iterations = 75
ants = 13
twt = 240


#datastructure
graph = []
ph = []
num_node = 0

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
	#all the variables are global.
	global graph
	global ph
	global num_node
	global nodes

	#reading time matrix from csv file
	dt = pd.read_csv('ip3.csv')
	graph = dt.to_numpy()
	num_node = len(graph)
	temp = []

	#initiallization of feromoan level for ants
	#all edges have same and unit feromoan level
	for i in range(num_node):
		ph.append([1 for i in range(num_node)])


def start_ant(nvis,dpot):
	global graph
	global ph
	global num_node
	global nodes

	# init, cp(current position) is dpot.
	cp=dpot
	#path will store the route of the ant
	path = []
	#starting point of the rout is dpot
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

def update_feromone(dpot,best_solution,shortedt_time):
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

def gettotal_time(path,dpot):
	# this function counts the time requires to follow a path..
	x=dpot
	total_time = 0
	for y in path:
		total_time+=graph[x][y]
		x=y
	total_time+=graph[x][dpot]
	return total_time

def get_best_solution(solution):
	# this function returns path which has min length.
	ma=solution[0]
	for soln in solution:
		if ma[0]>soln[0]:
			ma=soln
	return ma

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

def start_spreading_ants(nvis,shortedt_time,veh_type,itr,limit):
	"""
		This function will take nvis(non visited nodes) , shortest time of the previous iterations, typeofvehicle,
		itr number of iterations, limit after which iteration we have to apply idle time opt.
	"""
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
		solution.append( (gettotal_time(path,0),path) )

	# "get_best_solution" will return shortest path coverd among all the ants.
	best_solution = get_best_solution(solution)

	#count the Idle timme for the given vehicle type
	ID = 240-best_solution[0]
	# if the idle time is positive and pass the given condition then only we can apply idle time optimization
	if itr>limit and ID>0:
		if veh_type==2:
			from_veh_type = 1
			inds = []

			# if the idle time is greater then twt/4, then only vehicle can adopt the node from othervehivle
			# this is minimum cindition
			while twt/4 <= ID:
				# select node will return the list of node of from_veh_type
				# this list of node is sorted inorder to get the node which decrease the traveling time most
				inds = select_nodes(all_st[from_veh_type][1])
				#lock is use to terminate the while loop. if the vehicle is not able to adopt any node from other vehicle
				lock = True
				for ind in inds:
					#slp = second last position
					#lp = last position
					# for exaample path : 1-2-3-4-5-6 then slp=5, lp=6
					slp = best_solution[1][-2]
					lp = best_solution[1][-1]

					#checking that after adding one node, the total time of the path is less then 240 or not
					if graph[slp][ind[1]]+graph[ind[1]][lp]-graph[slp][lp]+best_solution[0] <= twt:
						#lock is false because we found one node which is adopted by the vehicle
						lock=False
						#removing and updating the node from the solution of from vehicle
						all_st[from_veh_type][1].remove(ind[1])
						all_st[from_veh_type]=(gettotal_time(all_st[from_veh_type][1],0),all_st[from_veh_type][1])

						#appending the new node in the vehicle's path, and updating the best solution of this vehicle.
						veh2.append(ind[1])
						all_st[2][1].append(ind[1])
						all_st[2]=(gettotal_time(all_st[2][1],0) , all_st[2][1] )

						#after adding new node, updating the best solution.
						shortedt_time=all_st[2]
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
			while twt/4<=ID:
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
				# select node will return the list of node of from_veh_type
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
					if ind[1]!=0 and graph[slp][ind[1]]+graph[ind[1]][lp]-graph[slp][lp]+best_solution[0] < twt:
						#lock is false because we found one node which is adopted by the vehicle
						lock=False
						#removing and updating the node from the solution of from vehicle
						all_st[from_veh_type][1].remove(ind[1])
						all_st[from_veh_type]=(gettotal_time(all_st[from_veh_type][1],0),all_st[from_veh_type][1])
						
						#appending the new node in the vehicle's path, and updating the best solution of this vehicle.
						veh3.append(ind[1])
						all_st[3][1].remove(0)
						all_st[3][1].append(ind[1])
						all_st[3][1].append(0)
						all_st[3]=(gettotal_time(all_st[3][1],0) , all_st[3][1] )
						#after adding new node, updating the best solution.
						shortedt_time=all_st[3]
						best_solution=all_st[3]
						#removing the node from from_veh_type vehicle
						if from_veh_type==1:
							veh1.remove(ind[1])
						else:
							veh2.remove(ind[1])

						# counting IDLE time again, if the idle time is more than twt/4, then again we will adopt one more node.
						ID = 240-best_solution[0]
						break
				# if vehicle not able to adopt any node then we will break the current while loop
				if lock:
					break

	#updating the shortest time.
	if shortedt_time[0] > best_solution[0]:
		shortedt_time=best_solution

	#This will update the feromone level.
	update_feromone(0,best_solution,shortedt_time)
	return shortedt_time

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
	veh2 = [8,11,13,2,5]
	veh3 = [3,7]

	# #output graph datastructure = x,veh1,veh2,veh3
	# output_graph = [ [] , [] , [] , [] ]

	#printing the value of parameters of the algo
	print("alpha:",alpha, " | beta:", beta, " | density",dens, " | Iterations: ",iterations, " | ants:",ants)

	#inti max shortest time for all vehicles 
	vehs_type1 = [[1,4,6,9,10,12],[55,92,20,33,18],[72,51,79,41,39],[98,16,17,76,56],[21,84,52,99,28],[15,93,27,73,24],[53,59,68,82,25,14],[50,38,75,91,97],[90,85,83,74,29],[70,64,54,46,66,81]]
	vehs_type2 = [[45,48,77,86],[8,11,13,2,5],[26,30,43,96],[31,40,58,62],[34,47,95,63],[36,49,60,65,67],[37,44,61],[69,71,78,80]]
	vehs_type3 = [[42,32,23],[19,100,89],[57,88,94],[87,22,35],[3,7]]
	

	for comb in range(0,10):
		veh1 = vehs_type1[ comb%10 ]
		veh2 = vehs_type2[ comb%8 ]
		veh3 = vehs_type3[ comb%5 ]
		limit = randint(40,70)
		plt.clf()
		output_graph = [ [] , [] , [] , [] ]
		#For n number ofoperations
		all_st[1] = (10**200,[])
		all_st[2] = (10**200,[])
		all_st[3] = (10**200,[])
		for itr in range(iterations):
			read_data()




			#setting up the opertions number
			iterations=itr
			
			for ii in range(itr):
				# this will start spreading ants in the graph.This will return shortest time of all the previous iterations
				all_st[1]= start_spreading_ants(veh1,all_st[1],1,ii,limit)
				all_st[1] = ( gettotal_time( all_st[1][1] , 0 ) , all_st[1][1] )

			for ii in range(itr):
				# this will start spreading ants in the graph.This will return shortest time of all the previous iterations
				all_st[2] = start_spreading_ants(veh2,all_st[2],2,ii,limit)
				all_st[2] = ( gettotal_time( all_st[2][1] , 0) , all_st[2][1] )


			for ii in range(itr):
				# this will start spreading ants in the graph.This will return shortest time of all the previous iterations
				all_st[3] = start_spreading_ants(veh3,all_st[3],3,ii,limit)
				all_st[3] = ( gettotal_time( all_st[3][1] , 0) , all_st[3][1] )
				
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
		plt.title("ACO algo")
		plt.legend()
		plt.show()

if __name__ == '__main__':
	main()
