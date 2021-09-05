#Variation of T_ad with different inlet air temperature for different phi.

import matplotlib.pyplot as plt
import cantera as ct
import numpy as np
import sys
import csv


# Edit these parameters to change the initial temperature, the pressure, and
# the phases in the mixture.

P = 101325.0 

# phases
gas = ct.Solution('JP10.yaml')
carbon = ct.Solution('graphite.yaml')

# the phases that will be included in the calculation, and their initial moles
mix_phases = [(gas, 1.0), (carbon, 0.0)]

# gaseous fuel species
fuel_species = 'C10H16'

# inlet temperature range
npoints = 50
T = np.linspace(500,1000,npoints)


phi = [1,0.5,1.5,2]

mix = ct.Mixture(mix_phases)

# create some arrays to hold the data
tad = np.zeros(npoints)
xeq = np.zeros((mix.n_species, npoints))

for j in range(len(phi)):
    for i in range(npoints):
        # set the gas state
        gas.set_equivalence_ratio(phi[j], fuel_species, 'O2:1.0, N2:3.76')

        # create a mixture of 1 mole of gas, and 0 moles of solid carbon.
        mix = ct.Mixture(mix_phases)
        mix.T = T[i]
        mix.P = P

        # equilibrate the mixture adiabatically at constant P
        mix.equilibrate('HP', solver='gibbs', max_steps=1000)

        tad[i] = mix.T
        xeq[:, i] = mix.species_moles

        print('At T = {0:12.4g}, Tad = {1:12.4g}, phi = {2:12.4g}'.format(T[i], tad[i], phi[j]))
    plt.plot(T, tad,label = phi[j])


if '--plot' in sys.argv:
    plt.xlabel('Inlet Temperature')
    plt.ylabel('Adiabatic flame temperature [K]')
    plt.legend(['1','0.5','1.5','2'])
    plt.show()
    

#write output CSV file for importing into Excel
csv_file = 'Tad with temp.csv'
with open(csv_file, 'w', newline='') as outfile:
   writer = csv.writer(outfile)
   writer.writerow(['T', 'Tad(K)'] + mix.species_names)
   for i in range(npoints):
       writer.writerow([T[i], tad[i]] + list(xeq[:, i]))
print('Output written to {0}'.format(csv_file))


   


