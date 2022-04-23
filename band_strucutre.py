import numpy as np
import matplotlib.pyplot as plt

file=np.genfromtxt('band.bs')

bs = open ('band.bs','r')
line = bs.readline().split()
num_points, num_k_points, num_bands = int(line[3]),int(line[6]),int(line[8])
sp=[""]*num_points
i=0
for i in range(num_points):
    line = bs.readline().split()
    sp[i] = line[7]


new=np.resize(file,(num_k_points*2,num_bands,3))
ener=new[:,:,1:2]
ener=np.resize(new[:,:,1:2],(num_k_points*2,num_bands)).transpose()
num_homo = len(new[:,:,2][1][new[:,:,2][1]==1])
num_lumo = len(new[:,:,2][1][new[:,:,2][1]==0])

for i in range(num_homo):
    plt.plot(ener[i,::2],color='k')
for i in range(num_lumo):
    plt.plot(ener[i+num_homo,::2],color='k',linestyle='-')

plt.ylim([-4,6])
plt.xlim([0,num_k_points-1])
plt.xticks(np.linspace(0,num_k_points-1,num_points),sp)
plt.ylabel("Energy (eV)")
