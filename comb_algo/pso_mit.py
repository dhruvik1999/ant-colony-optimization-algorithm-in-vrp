import pandas as pd 
import numpy as np 
import math
from random import *
from collections import OrderedDict
import matplotlib.pyplot as plt


#parameters of PSO
num_particles = 5
iterations = 100

#datastructure
graph = []
num_node = 0;
all_st = {}
veh1 = []
veh2 = []
veh3 = []

#const value
w=0.7
alpha = 0.5
beta = 0.5

#total time
twt = 240

def read_graph():
	# thtis function will read time and make a 2D array from .csv file. which containes time matrix
	global graph
	global num_node

	#using panda library, reading csv file.
	df = pd.read_csv('ip3.csv')
	#converting information to 2D array
	graph  = df.to_numpy()
	#setting up the total number of nodes
	num_node = len(graph)

class Particle:

	def __init__(self,position,velocity):
		#current position of particle
		#for eg = [0,1,4,3,2,5,0]
		self.position=position
		#current velocity of particle
		#for eg = [(1,2),(3,4)]
		self.velocity=velocity
		#personal best position of the particle
		#for eg = [0,3,2,4,5,0]
		self.pbest=(self.getTime(self.position),self.position.copy())

	def update(self,gbest):
		#vel = w*vel) + a*(gbest-pos) + b*(pbest-pos)
		#pos = pos + velocity
		
		# velocity update using above formula
		self.velocity = self.merge_list( self.mul_const_list(w,self.velocity.copy()) , self.mul_const_list(alpha, self.sub_position( gbest[1] , self.position.copy() ) ) )
		self.velocity = self.merge_list( self.velocity.copy() , self.mul_const_list(beta, self.sub_position( self.pbest[1] , self.position.copy() ) ) )
		
		# position update using above formula
		self.position = self.add_velocity_to_position(self.position , self.velocity)

		# self.velocity=list(OrderedDict.fromkeys(self.velocity))
		total_time = self.getTime(self.position)

		# if the personal best solution is better then global best result, then update the global best result
		if total_time < self.pbest[0]:
			self.pbest = ( self.getTime(self.position) , self.position)

	def getTime(self,position):
		# this function will reurn the total time taken by the path(posiion of paricle)
		# cp is current posiion
		cp=0
		total_time=0
		#  this loop will iterate through enire path and count the total time.
		for i in position:
			total_time += graph[cp][i]
			cp=i
		total_time+= graph[cp][0]
		return total_time
	
	def merge_list(self,l1,l2):
		# for addition of two velocity in formula of updation
		# for eg = [(0,1),(2,4)] + [(5,6)] = [(0,1),(2,4) , (5,6)]
		l = []
		if l1!=None:
			for i in l1:
				l.append(i)
		if l2!=None:
			for i in l2:
				l.append(i)
		return l

	def mul_const_list(self,param,velocity):
		# constant multiplication with the velocity
		# param * [velocity] = 0.6 * [ (1,5) , (2,3) ] = chance of selection of the item is 0.6
		n = len(velocity)
		
		ans = []
		for vel in velocity:
			if param >= random():
				ans.append(vel)

		return ans

	def sub_position(self,pos_a,pos_b):
		# substracion of two position will give the velocity.
		# pos1-pos2 = [1,3,2,4,5]-[1,2,3,4,5] = [ (1,2) ] (index of swapped item)
		ans = []
		hash = {}

		# used hash function for saving the position of the node
		for i in range( len(pos_b) ):
			hash[ pos_b[i] ]=i

		#substraction of two position
		for i in range( len(pos_a) ):
			if pos_a[i]!=pos_b[i]:
				temp_a=pos_b[i]
				temp_b=pos_a[i]
				ans.append( (i,hash[pos_a[i]]) )
				pos_b[i],pos_b[ hash[pos_a[i]] ] = pos_b[ hash[pos_a[i]] ],pos_b[i]
				hash[ temp_a ] , hash[ temp_b ] = hash[ temp_b ] , hash[ temp_a ]
		# for eg ans = [ (1,2) , (4,5) ]
		return ans

	def add_velocity_to_position(self,position,velocity):
		# this function adds velocity in position
		# for eg: pos + vel = [5,4,3,2,1] + [ (1,2) ] = [4,5,3,2,1]
		for i in velocity:
			position[i[0]],position[i[1]] = position[i[1]],position[i[0]]
		return position

	def print_state(self):
		#prints the details ofparticle
		print("Position : ", self.getTime(self.position) ,self.position)
		print("Velocity : ",self.velocity)
		print("pbest : ",self.pbest)

def get_randome_position(nodes):
	#provides random initial position
	shuffle(nodes)
	return nodes

def getTime(position):
	#this will reurn the rewuired time for traveling the current path(current position)
	cp=0
	total_time=0
	for i in position:
		total_time += graph[cp][i]
		cp=i
	total_time+= graph[cp][0]
	return total_time

def get_randome_velocity(path_length,seq_length):
	# this will return some randome velocity, and the length of the velocity is seq_length
	# for eg : if seq_length=2 , velocity = [ (1,2) , [4,5] ]
	velocity = []
	for i in range(seq_length):
		velocity.append( ( randint(0,path_length-1) , randint(0,path_length-1) ) )
	return velocity

def select_nodes(path):
	# this will count the channges been made by removing the each node
	# then sort the changes in assending ordere( changes are negative )
	# we will remove node which reduces the most traveling time.
	ans = []
	cp=0
	for i in range(0,len(path)-1):
		change = graph[path[cp]][path[i]]+graph[path[i]][ path[i+1] ]-graph[path[cp]][path[i+1]]
		ans.append( (-1*change, path[i] ) )
		cp=i
	ans.sort()
	return ans

def start_pso(nodes,itr,veh_type,best_solution,limit):
	global all_st
	global veh1
	global veh2
	global veh3

	#init all the particles, number of particle must be same as number of nodes
	particles = [ Particle(get_randome_position(nodes.copy()),get_randome_velocity( len(nodes),3 ) ) for i in range(num_particles) ]

	#init global best with maximam possible total time.
	gbest = (10**200 , [])

	# checking and updating gbest if any pbest is better than current pbest.
	for particle in particles:
			if particle.pbest[0] < gbest[0]:
				gbest=particle.pbest

	# this loop will run n iterations for given number of particles
	for i in range(itr):

		# checking and updating gbest if any pbest is better than current pbest.
		for particle in particles:
			if particle.pbest[0] < gbest[0]:
				gbest=particle.pbest

		# updating the position and velocity of each particles
		for particle in particles:
			particle.update(gbest)

	# updating the best solution, if the gbest of clusture is better than current best solution, then update it.
	if gbest[0]<best_solution[0]:
		best_solution=gbest
	
	# calculating idel time
	ID = twt - gbest[0]

	# if the idle time is greater then twt/4, then only vehicle can adopt the node from othervehivle
	# this is minimum cindition
	if twt/4 <= ID and itr>limit:
		if veh_type==2:
			from_veh = 1
			inds = []

			while twt/4 <= ID:
				# select node will return the list of node of from_veh_type
				# this list of node is sorted inorder to get the node which decrease the traveling time most
				inds = select_nodes(all_st[from_veh][1])
				#lock is use to terminate the while loop. if the vehicle is not able to adopt any node from other vehicle
				lock = True
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
						all_st[from_veh][1].remove(ind[1])
						all_st[from_veh]=(getTime(all_st[from_veh][1]),all_st[from_veh][1])
						
						#appending the new node in the vehicle's path, and updating the best solution of this vehicle.
						veh2.append(ind[1])
						all_st[2][1].append(ind[1])
						all_st[2]=(getTime(all_st[2][1]) , all_st[2][1] )
						
						#after adding new node, updating the best solution.
						gbest=all_st[2]
						best_solution=all_st[2]
						veh1.remove(ind[1])
						# counting IDLE time again, if the idle time is more than twt/4, then again we will adopt one more node.
						ID = 240-best_solution[0]
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
				from_veh = -1

				#which ever vehicle has higher value we will adopt node from that vehicle.
				if ID1>ID2:
					from_veh=2
				else:
					from_veh=1

				# selectiong node from selected vehicle
				# select node will return the list of node of from_veh_type
				# this list of node is sorted inorder to get the node which decrease the traveling time most
				inds = select_nodes(all_st[from_veh][1])
				
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
						all_st[from_veh][1].remove(ind[1])
						all_st[from_veh]=(getTime(all_st[from_veh][1]),all_st[from_veh][1])
						
						#appending the new node in the vehicle's path, and updating the best solution of this vehicle.
						veh3.append(ind[1])
						all_st[3][1].append(ind[1])
						all_st[3]=(getTime(all_st[3][1]) , all_st[3][1] )
						#after adding new node, updating the best solution.
						gbest=all_st[3]
						best_solution=all_st[3]
						if from_veh==1:
							veh1.remove(ind[1])
						else:
							veh2.remove(ind[1])
						# counting IDLE time again, if the idle time is more than twt/4, then again we will adopt one more node.
						ID = 240-best_solution[0]
				# if vehicle not able to adopt any node then we will break the current while loop
				if lock:
					break

	if gbest[0]<best_solution[0]:
		best_solution=gbest
	return best_solution

def main():
	global all_st
	global veh1
	global veh2
	global veh3

	read_graph()
	# init the path of all vehicles
	veh1 = [53, 59,68,82,25,14]
	veh2 = [8,11,13,2,5]
	veh3 = [3,7]
	all_st = {}

	#output graph datastructure = x,veh1,veh2,veh3
	output_graph = [ [] , [] , [] , [] ]

	#inti max shortest time for all vehicles 
	all_st[1] = (10**200,[])
	all_st[2] = (10**200,[])
	all_st[3] = (10**200,[])
	limit = randint(20,40)

	#For n number ofoperations
	for i in range(iterations):
		#starting pso for first vehicle
		all_st[1] = start_pso(veh1,i,1,all_st[1],limit)
		
		#starting pso for first vehicle
		all_st[2] = start_pso(veh2,i,2,all_st[2],limit)
		
		#starting pso for first vehicle
		all_st[3] = start_pso(veh3,i,3,all_st[3],limit)

		#printing result
		print(i , all_st)
		output_graph[0].append(i)
		output_graph[1].append(all_st[1][0])
		output_graph[2].append(all_st[2][0])
		output_graph[3].append(all_st[3][0])

	plt.plot(output_graph[0] , output_graph[1], label="Vehicle 1"  )
	plt.plot(output_graph[0] , output_graph[2], label="Vehicle 2"  )
	plt.plot(output_graph[0] , output_graph[3], label="Vehicle 3"  )
	plt.title("PSO algo")
	plt.legend()
	plt.show()

if __name__ == '__main__':
	main()