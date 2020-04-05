import pandas as pd 
import numpy as np 
import math
from random import *
from collections import OrderedDict

num_particles = 11
iterations = 100

data = []
num_node = 0;

w=0.6
alpha = 0.9
beta = 0.3

def read_data():
	global data
	global num_node

	df = pd.read_csv('ip2.csv')
	data  = df.to_numpy()
	num_node = len(data)

class Particle:

	def __init__(self,position,velocity):
		self.position=position
		self.velocity=velocity
		self.pbest=(self.getTime(self.position),self.position.copy())

	def update(self,gbest):
		#vel = w*vel + a*(gbest-pos) + b*(pbest-pos)
		#pos = pos + velocity

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
			total_time += data[cp][i]
			cp=i
		total_time+= data[cp][0]
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
		param = math.ceil(n*param)

		ans = []
		for i in range(param):
			ans.append( velocity[ randint(0,len(velocity)-1) ] )
			velocity.remove( ans[-1] )
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
	# shuffle(nodes)
	return nodes

def get_randome_velocity(path_length,seq_length):
	velocity = []
	for i in range(seq_length):
		velocity.append( ( randint(0,path_length-1) , randint(0,path_length-1) ) )
	return velocity


def start_pso(nodes,itr):
	particles = [ Particle(get_randome_position(nodes.copy()),get_randome_velocity( len(nodes),3 ) ) for i in range(num_particles) ]
	gbest = (10**200 , [])
	list_gbest = []
	for i in range(itr):
		for particle in particles:
			if particle.pbest[0] < gbest[0]:
				gbest=particle.pbest

		for particle in particles:
			print("\n particle")
			particle.print_state()
			particle.update(gbest)
			#print("pbest",particle.pbest)
			particle.print_state()


		
		# print("gbest",gbest)
		list_gbest.append(gbest)

	return list_gbest

def main():
	read_data()
	st1 = start_pso([1,4,6,9,10,12],iterations)
	st2 = start_pso([8,13,11,2,5],iterations)
	st3 = start_pso([3,7],iterations)

	for i in range(iterations):
		print(i+1 , st1[i] , st2[i] , st3[i])
		# print(i+1,st1[i])


if __name__ == '__main__':
	main()