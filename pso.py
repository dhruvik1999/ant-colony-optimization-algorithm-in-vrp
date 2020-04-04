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
		pass

	def getTime(self,position):
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
		particle.print_state()

def main():
	read_data()
	start_pso([1,2,3,4,5])

if __name__ == '__main__':
	main()