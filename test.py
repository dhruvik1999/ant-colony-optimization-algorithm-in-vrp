from random import randint 

# def func(pos_a,pos_b):
# 	ans = []
# 	hash = {}
# 	for i in range( len(pos_b) ):
# 		hash[ pos_b[i] ]=i

# 	for i in range( len(pos_a) ):
# 		if pos_a[i]!=pos_b[i]:
# 			temp_a=pos_b[i]
# 			temp_b=pos_a[i]
# 			ans.append( (i,hash[pos_a[i]]) )
# 			pos_b[i],pos_b[ hash[pos_a[i]] ] = pos_b[ hash[pos_a[i]] ],pos_b[i]
# 			hash[ temp_a ] , hash[ temp_b ] = hash[ temp_b ] , hash[ temp_a ]
# 	print(ans)
# 	return ans


# def main():
# 	func([1,2,3,4,5,6,7,8],[1,8,6,7,2,3,4,5])

# if __name__ == '__main__':
# 	main()

for i in range(1,100):
	print(randint(35,65))


# number_list = [7, 14, 21, 28, 35, 42, 49, 56, 63, 70]
# print ("Original list : ",  number_list)

# random.shuffle(number_list) #shuffle method
# print ("List after first shuffle  : ",  number_list)

# data = pd.read_csv('op2.csv')
# data = data.to_numpy()

# for i in data:
# 	if i[1]<=240 and i[2]<=240 and i[3]<=240:
# 		print(i)

# def opt_2(path):
# 	temp_path = path.copy()
# 	rnd_node = np.random.choice(path[:-1])
# 	path.remove(rnd_node)
# 	path.insert( np.random.choice( [i for i in range(0,len(path[:-1]))]),rnd_node)
# 	print(temp_path)
# 	print(path)

# a = [1,5,4,2,3,6,7,0]
# opt_2(a)