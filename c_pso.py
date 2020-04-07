import pandas as pd 
import numpy as np 
import math
from random import *
from collections import OrderedDict
import time

num_particles = 20
iterations = 100

graph = []
num_node = 0;
all_st = {}
veh1 = []
veh2 = []
veh3 = []

w=0.7
alpha = 0.5
beta = 0.5

twt = 240

def read_graph():
	global graph
	global num_node

	df = pd.read_csv('ip3.csv')
	graph  = df.to_numpy()
	num_node = len(graph)

class Particle:

	def __init__(self,position,velocity):
		self.position=position
		self.velocity=velocity
		self.pbest=(self.getTime(self.position),self.position.copy())

	def update(self,gbest):
		#vel = w*vel) + a*(gbest-pos) + b*(pbest-pos)
		#pos = pos + velocity
		#velocity  = [  (1,2) , () , ()  ]
		#pos = [1,2,3,4,5] + velocity = [1,3,2,4,5]

		self.velocity = self.merge_list( self.mul_const_list(w,self.velocity.copy()) , self.mul_const_list(alpha, self.sub_position( gbest[1] , self.position.copy() ) ) )
		self.velocity = self.merge_list( self.velocity.copy() , self.mul_const_list(beta, self.sub_position( self.pbest[1] , self.position.copy() ) ) )
	
		# shuffle(self.velocity)
		# self.velocity = self.velocity[:1]
		# self.velocity = self.velocity[:-1]
		self.position = self.add_velocity_to_position(self.position , self.velocity)
		
		
		# self.velocity=list(OrderedDict.fromkeys(self.velocity))
		total_time = self.getTime(self.position)

		if total_time < self.pbest[0]:
			self.pbest = ( self.getTime(self.position) , self.position)

	def getTime(self,position):
		cp=0
		total_time=0
		for i in position:
			total_time += graph[cp][i]
			cp=i
		total_time+= graph[cp][0]
		return total_time
	
	def merge_list(self,l1,l2):
		l = []
		if l1!=None:
			for i in l1:
				l.append(i)
		if l2!=None:
			for i in l2:
				l.append(i)
		return l

	def mul_const_list(self,param,velocity):
		n = len(velocity)
		
		ans = []
		for vel in velocity:
			if param >= random():
				ans.append(vel)

		# for i in range(param):

		# 	ans.append( velocity[ randint(0,len(velocity)-1) ] )
		# 	velocity.remove( ans[-1] )
		return ans

	def sub_position(self,pos_a,pos_b):
		ans = []
		hash = {}
		for i in range( len(pos_b) ):
			hash[ pos_b[i] ]=i

		for i in range( len(pos_a) ):
			if pos_a[i]!=pos_b[i]:
				temp_a=pos_b[i]
				temp_b=pos_a[i]
				ans.append( (i,hash[pos_a[i]]) )
				pos_b[i],pos_b[ hash[pos_a[i]] ] = pos_b[ hash[pos_a[i]] ],pos_b[i]
				hash[ temp_a ] , hash[ temp_b ] = hash[ temp_b ] , hash[ temp_a ]
		# print(ans)
		return ans

	def add_velocity_to_position(self,position,velocity):
		for i in velocity:
			position[i[0]],position[i[1]] = position[i[1]],position[i[0]]
		return position

	def add_two_velocity(self,vel1,vel2):
		pass

	def print_state(self):
		print("Position : ", self.getTime(self.position) ,self.position)
		print("Velocity : ",self.velocity)
		print("pbest : ",self.pbest)

def get_randome_position(nodes):
	shuffle(nodes)
	return nodes

def getTime(position):
	cp=0
	total_time=0
	for i in position:
		total_time += graph[cp][i]
		cp=i
	total_time+= graph[cp][0]
	return total_time

def get_randome_velocity(path_length,seq_length):
	velocity = []
	for i in range(seq_length):
		velocity.append( ( randint(0,path_length-1) , randint(0,path_length-1) ) )
	return velocity

def select_nodes(path):
	#0-1--3-4-5-6-0
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
	particles = [ Particle(get_randome_position(nodes.copy()),get_randome_velocity( len(nodes),3 ) ) for i in range(num_particles) ]
	gbest = (10**200 , [])

	for particle in particles:
			if particle.pbest[0] < gbest[0]:
				gbest=particle.pbest

	for i in range(itr):

		for particle in particles:
			if particle.pbest[0] < gbest[0]:
				gbest=particle.pbest
		
		for particle in particles:
			# print("\n particle")
			# particle.print_state()
			particle.update(gbest)
			#print("pbest",particle.pbest)
			# particle.print_state()
		# print("gbest",gbest)
	if gbest[0]<best_solution[0]:
		best_solution=gbest
		
	ID = twt - gbest[0]
	if twt/4 <= ID and itr>limit:
		if veh_type==2:
			from_veh = 1
			inds = []
			while twt/4 <= ID:
				inds = select_nodes(all_st[from_veh][1])
				lock = True
				for ind in inds:
					slp = best_solution[1][-2]
					lp = best_solution[1][-1]
					if graph[slp][ind[1]]+graph[ind[1]][lp]-graph[slp][lp]+best_solution[0] < twt:
						lock=False
						all_st[from_veh][1].remove(ind[1])
						all_st[from_veh]=(getTime(all_st[from_veh][1]),all_st[from_veh][1])
						veh2.append(ind[1])
						all_st[2][1].append(ind[1])
						all_st[2]=(getTime(all_st[2][1]) , all_st[2][1] )
						gbest=all_st[2]
						best_solution=all_st[2]
						veh1.remove(ind[1])
						ID = 240-best_solution[0]
				if lock:
					break

		elif veh_type==3:
			inds = []
			while twt/4<=ID:
				lock = True
				ID1 = 240 - all_st[1][0]
				ID2 = 240 - all_st[2][0]
				from_veh = -1

				if ID1>ID2:
					from_veh=2
				else:
					from_veh=1
				inds = select_nodes(all_st[from_veh][1])
				for ind in inds:
					slp = best_solution[1][-2]
					lp = best_solution[1][-1]
					if graph[slp][ind[1]]+graph[ind[1]][lp]-graph[slp][lp]+best_solution[0] < twt:
						lock=False
						all_st[from_veh][1].remove(ind[1])
						all_st[from_veh]=(getTime(all_st[from_veh][1]),all_st[from_veh][1])
						veh3.append(ind[1])
						all_st[3][1].append(ind[1])
						all_st[3]=(getTime(all_st[3][1]) , all_st[3][1] )
						gbest=all_st[3]
						best_solution=all_st[3]
						if from_veh==1:
							veh1.remove(ind[1])
						else:
							veh2.remove(ind[1])
						ID = 240-best_solution[0]
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

	veh1 = [1,4,6,9,10,12]
	veh2 = [8,13,11,2,5]
	veh3 = [3,7]
	all_st = {}
	ans = {}
	count = {}
	for i in range(23):
		ans[i]=0
		count[i]=0
	total_combinations = 0
	vehs = [[1,4,6,9,10,12],[55,92,20,33,18],[72,51,79,41,39],[98,16,17,76,56],[21,84,52,99,28],[15,93,27,73,24],[53,59,68,82,25,14],[50,38,75,91,97],[90,85,83,74,29],[70,64,54,46,66,81],[45,48,77,86],[8,11,13,2,5],[26,30,43,96],[31,40,58,62],[34,47,95,63],[36,49,60,65,67],[37,44,61],[69,71,78,80],[42,32,23],[19,100,89],[57,88,94],[87,22,35],[3,7]]


	for veh in range(100):
		t1 = time.time()
		
		v1 = np.random.choice([0,1,2,3,4,5,6,7,8,9])
		v2 = np.random.choice([10,11,12,13,14,15,16,17])
		v3 = np.random.choice([18,19,20,21,22])

		print(v1,v2,v3)
		count[v1]+=1
		count[v2]+=1
		count[v3]+=1

		veh1 = vehs[v1].copy()
		veh2 = vehs[v2].copy()
		veh3 = vehs[v3].copy()

		all_st[1] = (10**200,[])
		all_st[2] = (10**200,[])
		all_st[3] = (10**200,[])
		limit = randint(20,40)

		read_graph()
		for i in range(40):
			all_st[1] = start_pso(veh1,i,1,all_st[1],limit)

			all_st[2] = start_pso(veh2,i,2,all_st[2],limit)

			all_st[3] = start_pso(veh3,i,3,all_st[3],limit)

			if all_st[1][0]<240 and all_st[2][0]<240 and all_st[3][0]<240:
				print(i , all_st,time.time()-t1)

		input()
		ans[v1]+=all_st[1][0]
		ans[v2]+=all_st[2][0]
		ans[v3]+=all_st[3][0]

		print("--->ans",ans)
		print("--->count",count)

		






if __name__ == '__main__':
	main()