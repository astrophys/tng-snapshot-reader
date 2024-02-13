import illustris_python as il
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
basePath = '/afs/crc.nd.edu/group/phillips/asnedden/Analysis/TNG-50/Illustris-3/output'
fields = ['Masses']
gas_mass = il.snapshot.loadSubset(basePath,135,'gas',fields=fields)
print(np.log10( np.mean(gas_mass,dtype='double')*1e10/0.704 ))
import matplotlib as mpl
#mpl.use('qtagg')
dm_pos = il.snapshot.loadSubset(basePath,135,'dm',['Coordinates']);
plt.hist2d(dm_pos[:,0], dm_pos[:,1], norm=mpl.colors.LogNorm(), bins=64);
plt.xlim([0,75000])
plt.ylim([0,75000])
plt.xlabel('x [ckpc/h]')
plt.ylabel('y [ckpc/h]')
stars = il.snapshot.loadHalo(basePath,135,100,'stars')
stars.keys()
for i in range(3):
    print(np.min(stars['Coordinates'][:,i]), np.max(stars['Coordinates'][:,i]))
plt.show()
