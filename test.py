import pandas as pd
import numpy as np 

# data = pd.read_csv('op2.csv')
# data = data.to_numpy()

# for i in data:
# 	if i[1]<=240 and i[2]<=240 and i[3]<=240:
# 		print(i)

def opt_2(path):
	temp_path = path.copy()
	rnd_node = np.random.choice(path[:-1])
	path.remove(rnd_node)
	path.insert( np.random.choice( [i for i in range(0,len(path[:-1]))]),rnd_node)
	print(temp_path)
	print(path)

a = [1,5,4,2,3,6,7,0]
opt_2(a)