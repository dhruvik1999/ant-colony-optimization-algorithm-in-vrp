import pandas as pd 
import numpy as np 
from random import *

num_particles = 13
iterations = 10

data = []
num_node = 0;

alpha = 0.5
beta = 0.5

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
		self.pbest=(self.getTime(self.position),self.position)

	def update(self,gbest):
		#vel = w*vel + a*(gbest-pos) + b*(pbest-pos)
		#pos = pos + velocity
		pass

	def getTime(self,position):
		cp=0
		total_time=0
		for i in position:
			total_time += data[cp][i]
			cp=i
		total_time+= data[cp][0]
		return total_time

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
		print(ans)
		return ans

	def add_velocity_to_position(self,position,velocity):
		for i in velocity:
			position[i[0]],position[i[1]] = position[i[1]],position[i[0]]
		return position

	def add_two_velocity(self,vel1,vel2):
		pass

	def print_state(self):
		print("Position : ",self.position)
		print("Velocity : ",self.velocity)

def get_randome_position(nodes):
	shuffle(nodes)
	return nodes

def get_randome_velocity(path_length):
	velocity = []
	velocity.append( ( randint(0,path_length-1) , randint(0,path_length-1) ) )
	return velocity

def start_pso(nodes):
	particles = [ Particle(get_randome_position(nodes.copy()),get_randome_velocity( len(nodes) ) ) for i in range(num_particles) ]

	for particle in particles:
		print("Particle")
		# particle.print_state()
		print("Path : ",particle.position)
		print("Total time : ",particle.getTime(particle.pbest[1]))

def main():
	read_data()
	start_pso([1,2,3,4,5])

if __name__ == '__main__':
	main()