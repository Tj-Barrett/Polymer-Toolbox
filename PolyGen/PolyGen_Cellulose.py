import math
import os
import subprocess

# number of units per polymer (2 for 1 mer)
nmon = 20
# number of polymers
npoly = 500
# length
mon = 5

#-------------------------------------
# Polymer Section
#-------------------------------------
# Polymer
poly = "cellulose"
forcefield = "glycam_06j.lt"
ff = 'glycam06j'

#-------------------------------------
# ndmansfield
#-------------------------------------
# ndmansfield output
crds = 'crds.raw'
# number of monomers in total
nunits  = nmon * npoly

# number of lattice points for ndmansfield
Nx = math.ceil(nunits**(1./3))
Ny = Nx
Nz = Ny

tsave = 10000000
tstop = 30000000
# plus one for the blank line separating each frame
tail = nunits + 1

argsND = 'ndmansfield -box '+str(Nx)+' '+str(Ny)+' '+str(Nz)+' -tsave '+str(tsave)+' -tstop '+str(tstop)+' | tail -n '+str(tail)+' > '+ crds

os.system(argsND)

#-------------------------------------
# .system file
#-------------------------------------
dx = math.ceil(nunits**(1./3)*mon)
dy = dx
dz = dy
cgsys = open(poly+'.system','w+')
cgsys.write('#----------------\n')
cgsys.write('# Lammps Settings\n')
cgsys.write('#----------------\n \n')
cgsys.write('write_once("Data Boundary"){ \n')
cgsys.write('0.0'+' '+str(dx)+' xlo xhi \n')
cgsys.write('0.0'+' '+str(dy)+' ylo yhi \n')
cgsys.write('0.0'+' '+str(dz)+' zlo zhi \n } \n')
cgsys.write(poly+' = new '+poly)
cgsys.close()



#-------------------------------------
# interpolate
# https://github.com/jewettaij/moltemplate/blob/master/doc/doc_interpolate_curve.md
#-------------------------------------
#interpolated output
scrds = 'scrds.raw'

lattice_points = Nx*Ny*Nz
scale = round(mon * nunits / lattice_points,5)

argsint = 'interpolate_curve.py '+str(nunits)+' '+str(scale)+' < '+crds+' > '+scrds

os.system(argsint)
#-------------------------------------
# Genpoly
# https://github.com/jewettaij/moltemplate/blob/master/doc/doc_genpoly_lt.md
#-------------------------------------

# prep by making a sequence file
seq = open(poly+'_Sequence.txt','w+')
for j in range(npoly):
	for i in range(nmon):
		if i == 0: # First
			seq.write(''+poly+'L \n')
		elif i== nmon-1: # End
			seq.write(''+poly+'R \n')
		else: # Odds
			seq.write(''+poly+'RU \n')
seq.close()

# and a cuts file
cuts = open(poly+'_Cuts.txt','w+')
for i in range(1,npoly):
	cuts.write(str(nmon*i)+' \n')
cuts.close()

'''
Modify this section as needed for genpoly.

=== Used in this script ===
Cuts - includes the created cut file
Sequence - includes the created sequence file

Bonds - links monomers using the specified ID's, that will be in the *.lt files

Inheirts - needs to inherit forcefields from the *.lt and external forcefield files to write the proper data files

=== Optional ===
Helix - rotates the backbone
'''
start = 'python genpoly_lt_new.py '
header = '-header \"import '+forcefield+'\" '
polymer = '-polymer-name '+'\"'+poly+'\" '
monomer = '-monomer-name '+'\"'+poly+'\" '
sequence = '-sequence '+poly+'_Sequence.txt '
cuts = '-cuts '+poly+'_Cuts.txt '
helix = '-helix 180.0 '
# cl - cr
bonds = '-bond \"Cg-Os\" \"O0\" \"C0\" '

inherits = '-inherits \"'+ff+'\" '

inputcrds = '< '+scrds+' > '
outputlt = poly+'_system.lt'

argsGen = start+polymer+monomer+sequence+cuts+inherits+helix+bonds+inputcrds+outputlt

os.system(argsGen)

#-------------------------------------
# Modifying _system file
#-------------------------------------

'''
Modify this section to include all *.lt files and the forcefields. See MOLTEMPLATE's documentation for more info

'''
#add beginning and end
add = []
add.append('import \"glycam_06j.lt\" \n')
add.append('import \"'+poly+'_glycam_l.lt\" \n')
add.append('import \"'+poly+'_glycam_r.lt\" \n')
add.append('import \"'+poly+'_glycam_ru.lt\" \n')
add.append('import \"'+poly+'.system\" \n')

with open(poly+'_system.lt') as f:
    contents = f.readlines()

contents = add+contents

with open(poly+'_system.lt', 'w') as f:
    f.writelines(contents)

argsMol = 'moltemplate.sh -atomstyle full -nocheck '+poly+'_system.lt'# -checkff

os.system(argsMol)
