
#二群QDA

import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

D = np.loadtxt('C:/Users/sarah/OneDrive/桌面/satatistic_hw/practice1/data1/la_3.txt')
fig = plt.figure(figsize=[6, 4])

#draw scatter plot
X = D[:, 0:2]
y = D[:,2]
C1, C2= X[y==0, :], X[y==1, :]

plt.scatter(C1[:,0],C1[:,1], c='c', s=10, marker='o', label = 'Group A')
plt.scatter(C2[:,0],C2[:,1], c='b', s=10, marker='o', label = 'Group B')

plt.legend(loc='upper left')

#QDA畫曲線
Qda = QuadraticDiscriminantAnalysis(tol = 1e-6, store_covariance = True)
Qda.fit(X, y)

nx, ny = 100, 100
x_min, x_max = plt.xlim()
y_min, y_max = plt.ylim()
x_ = np.linspace(x_min, x_max, nx)
y_ = np.linspace(y_min, y_max, ny)
xx, yy = np.meshgrid(x_, y_)
Z = Qda.predict_proba(np.c_[xx.ravel(), yy.ravel()])
Z = Z[:, 0].reshape(xx.shape)
contoursQDA = plt.contour(xx, yy, Z, [0.5])

#用套件算Qda
Qda = QuadraticDiscriminantAnalysis(tol = 1e-6, store_covariance = True)
Qda.fit(X, y)
MissClassRateQDA = 1 - Qda.score(X, y)

plt.grid(lw=0.3)
plt.title('The Training error of QDA is '  f'{MissClassRateQDA:.3f}')
# plt.savefig('C:\\Users\\sarah\\OneDrive\\桌面\\satatistic_hw\\XeLaTex\\eps_five\\QDAex2.eps', format='eps')

plt.grid(lw=0.3)
plt.show()


