'''
Thomas Barrett
Minus Lab
Northeastern University
RDF and Static Structure

See for more info:
K. Zhang, On the Concept of Static Structure Factor, arXiv:1606.03610 (2016)


Takes RDF output and dump file at final step (only 1 timestep in output)

Dump form : 'atom', 'id', 'x', 'y', 'z', 'ix', 'iy', 'iz'
'''
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

# fixes qt conflict with pyside 6, unnecessary in most cases
# import matplotlib
# matplotlib.use('Qt5Agg')

# Inputs from lammps file
# RDF

prefix = ['test-']
legend = ['Test']

suffixRDF = 'RDF.txt'
suffixXYZ = 'end_xyz.dump'

RDFfile = []
XYZfile = []

# converts from LJ units
ratio = 8.646 # 2*np.pi/(0.89*np.sqrt(2/3))

# max wavevector
qmax = 25

for i in prefix:
	RDFfile.append(i+suffixRDF)
	XYZfile.append(i+suffixXYZ)

# RDF

Rad_Dict = {}
Int_Dict = {}

for i in range(len(RDFfile)):
	# Volume
	data = pd.read_csv(XYZfile[i], delimiter = ' ', header = 9, names = ['atom', 'id', 'x', 'y', 'z', 'ix', 'iy', 'iz'])

	x = np.array(data.x)
	y = np.array(data.y)
	z = np.array(data.z)

	num_particles = len(z)

	xlo = np.min(x)
	xhi = np.max(x)
	ylo = np.min(y)
	yhi = np.max(y)
	zlo = np.min(z)
	zhi = np.max(z)

	volume = (xhi-xlo)*(yhi-ylo)*(zhi-zlo)
	l = xhi-xlo

	del data, x, y, z

	# Structure Factor
	data = pd.read_csv(RDFfile[i], skiprows=4, delimiter=' ', names=['Row', 'Radius', 'Intensity', 'C'])

	key = 'Rad'+str(i)
	val = 'Int'+str(i)

	num_rbins = len(data.Radius)
	num_qbins = num_rbins

	radius = np.array(data.Radius)
	count = np.array(data.Intensity)

	# number density
	rho = num_particles/volume
	# dr
	dr = radius[1]-radius[0]
	dq = (qmax - 0.0)/num_qbins

	# 3D S(q)
	Sq = []
	qi = []
	for j in range(num_qbins):
		qi.append((j+0.5)*dq)

		step = 0.0
		for k in range(num_rbins):
			step = step + radius[k]*(count[k]-1.0)*np.sin(qi[j]*radius[k])/qi[j]
		step = step * dr*4*np.pi*rho + 1

		Sq.append(step)

	Rad_Dict[key] = np.array(qi)
	Int_Dict[val] = np.array(Sq)

	print(RDFfile[i] + '\n' + ' Ratios')

	xout = np.array(qi)
	print(xout[argrelextrema(np.array(Sq), np.greater)[0]])
	# print(xout[argrelextrema(np.array(Sq), np.greater)[0]]/ratio)


xhi = np.max(qi)

for i in range(len(RDFfile)):
	key = 'Rad'+str(i)
	val = 'Int'+str(i)
	plt.plot(Rad_Dict[key], Int_Dict[val], linestyle='-')

plt.xlim(4,qmax)
plt.ylim((0, 5))
plt.xlabel('q')
plt.ylabel('Sq')
plt.legend(legend)
plt.show()
