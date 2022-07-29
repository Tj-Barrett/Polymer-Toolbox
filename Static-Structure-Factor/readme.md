Reads and computes Static Structure Factor from LAMMPS output data.

#######################
# RDF_read.py
#######################
Reads rdf from LAMMPS. RDFs will trend to 1 for LJ fluids and have pronounced peaks for crystalline materials. Polymers do a bit of both, with peaks corresponding to bonded or non-bonded intervals depending on how RDF is set up in lammps using special bonds.

If using RDFs for something like iterative boltzmann inversion, see Iterative Boltzmann folder.

# all neighbors
special_bonds lj 1.0 1.0 1.0

# 1-3, 1-4
special_bonds lj 0.0 1.0 1.0

# 1-4
special_bonds lj 0.0 0.0 1.0

# Inter chain only (in the case of polymers)
special_bonds lj 0.0 0.0 0.0

![RDF Example](https://user-images.githubusercontent.com/71855260/181778781-ad9e8f0f-a447-416b-994a-a599ec51dc4e.png)


#######################
# SimpleStructure.py
#######################
Simple Structure computes the static structure factor and outputs ratios with the following plot. Takes the RDF and a dump file to get the volume of the system.  

To sample something like the carbon in CHOH groups of PVA, the necessary outputs would be

# CHOH groups
# type 1 is carbon in ch2, type 2 carbon in choh
group backbone2 type 2

compute CCrdf all rdf 200 *3 *3 cutoff 20.0 # bin is 0.1 Angstrom
fix	 1 all ave/time  10000 1 10000 c_CCrdf[*] file test-RDF.txt mode vector
dump 1 backbone2 custom 1 test-end_xyz.dump id mol type x y z xu yu zu
run 0

 Ratios
[ 0.825  2.425  3.675  4.825  6.125  7.525  9.175 10.425 11.575 13.275
 15.125 16.975 18.675 20.325 21.825 22.925]

![Structure Factor Example](https://user-images.githubusercontent.com/71855260/181775994-89e7004d-72c7-47dd-9720-9d7200d5f676.png)
