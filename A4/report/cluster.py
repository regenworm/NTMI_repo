import sys

clusters = 20

cluster_list = [0] * clusters

for line in open('smoothing.dat', 'r').readlines():
	value = line.split(' ')[0]
	index = int((float(value)  * clusters)) - 1
	cluster_list[index] += 1

file_handle = open('smoothing_bar.dat', 'w')

for index in range(0, len(cluster_list)):
	file_handle.write(str(index) + ' ' + str(cluster_list[index]) + '\n')
 
file_handle.close()

cluster_list = [0] * clusters

for line in open('nosmoothing.dat', 'r').readlines():
	value = line.split(' ')[0]
	index = int((float(value)  * clusters)) - 1
	cluster_list[index] += 1

file_handle = open('nosmoothing_bar.dat', 'w')

for index in range(0, len(cluster_list)):
	file_handle.write(str(index) + ' ' + str(cluster_list[index]) + '\n')
 
file_handle.close()
