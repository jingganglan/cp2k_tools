import numpy as np
import scipy.integrate as spint
from scipy.interpolate import interp1d


x = np.genfromtxt('./av_force_vs_x.dat')[:,0]*0.529
y = np.genfromtxt('./av_force_vs_x.dat')[:,1]*51.4

xnew = np.linspace(-0.2,2.8, num=100, endpoint=True)
xnew = xnew*0.529
f2 = interp1d(x, y)

plt.plot(x,y)
plt.plot(xnew,f2(xnew))
y_int = -spint.cumtrapz(y,x, initial=0)
f2_int = -spint.cumtrapz(f2(xnew),xnew, initial=0)
plt.xlim([1.5,-0.2])
plt.plot(x, y_int-np.min(y_int))
plt.plot(xnew, f2_int-np.min(f2_int))
plt.show()
