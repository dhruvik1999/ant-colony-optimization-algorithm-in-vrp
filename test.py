import pandas as pd
import numpy as np 

data = pd.read_csv('op2.csv')
data = data.to_numpy()

for i in data:
	if i[1]<=240 and i[2]<=240 and i[3]<=240:
		print(i)
