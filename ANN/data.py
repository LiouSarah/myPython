import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gammainc

#circle

radius_in, radius_out =10, 30

def randsphere(center, radius, n_per_sphere):
    r = radius
    ndim = center.size
    x = np.random.normal(size=(n_per_sphere, ndim))
    ssq = np.sum(x ** 2, axis=1)
    fr = r * gammainc(ndim / 2, ssq / 2) ** (1 / ndim)\
    / np.sqrt(ssq)
    frtiled = np.tile(fr.reshape(n_per_sphere, 1), (1, ndim))
    p = center + np.multiply(x, frtiled)
    return p

p = randsphere(np.array([0, 0]), 30, 1000)
# p = p[(p[:,0] > 0) & (p[:,1] > 0), :] # 第一象限
# d = np.sum(p**2, axis=1)
# p = p[d >= radius_in**2, :] # 扇形內
plt.figure(figsize=(6,6))
plt.scatter(p[:,0],p[:,1],marker='o',s=10, color='#FFCC99')

a, b =0 ,0
r = 30
theta = np.arange(0, 2*np.pi, 0.01)
x1 = a+r*np.cos(theta)
x2 = b+r*np.sin(theta)
# f2 = lambda x: np.sqrt(l2**2-x**2)
# x = np.linspace(0, l1, 100)
plt.plot(x1, x2, color='#FF8000')

# plt.savefig('C:\\Users\\sarah\\OneDrive\\桌面\\satatistic_hw\\XeLaTex\\eps_six\\data.eps', format='eps')
plt.show()