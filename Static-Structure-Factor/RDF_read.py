'''
Thomas Barrett
Minus Lab
Northeastern University

Read RDF output from LAMMPS
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# fixes qt conflict with pyside 6, unnecessary in most cases
import matplotlib
matplotlib.use('Qt5Agg')

prefix = ['test-']
legend = ['Test']

suffix = 'RDF.txt'

file = []
for i in prefix:
	file.append(i+suffix)

Rad_Dict = {}
Int_Dict = {}

for i in range(len(file)):
	data = pd.read_csv(file[i], skiprows=4, delimiter=' ', names=['Row', 'Radius', 'Intensity', 'C'])

	key = 'Rad'+str(i)
	val = 'Int'+str(i)

	xmax = np.max(data.Radius)

	Rad_Dict[key] = np.array(data.Radius)
	Int_Dict[val] = np.array(data.Intensity)

markers = ['-', '-.', '--',':', '-.', '--',':']

for i in range(len(file)):
	key = 'Rad'+str(i)
	val = 'Int'+str(i)
	plt.plot(Rad_Dict[key], Int_Dict[val], linestyle=markers[i])

plt.xlim(0,xmax)
plt.ylim(0,2.0)
plt.xlabel('Distance')
plt.ylabel('Intensity')
plt.legend(legend)
plt.show()
