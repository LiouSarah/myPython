
#範例五  三群QDA

import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split

D = np.loadtxt('C:/Users/sarah/OneDrive/桌面/satatistic_hw/practice1/LDA/hw_data8.txt', comments='#')
fig = plt.figure(figsize=[6, 4])

#draw scatter plot
X = D[:, 0:2]
y = D[:,2]
C1, C2, C3 = X[y==0, :], X[y==1, :], X[y==2,:]

plt.scatter(C1[:,0],C1[:,1], c='#FE6F5E', s=10, marker='o', label = 'Group A')
plt.scatter(C2[:,0],C2[:,1], c='#00CC99', s=10, marker='o', label = 'Group B')
plt.scatter(C3[:,0],C3[:,1], c='#007FFF', s=10, marker='o', label = 'Group C')
plt.legend(loc='upper left')

#QDA畫曲線
Qda = QuadraticDiscriminantAnalysis(tol = 1e-6, store_covariance = True)
Qda.fit(X, y)
color = ['r', 'c', 'b']
for i in range(3):
    nx, ny = 100, 100
    x_min, x_max = plt.xlim()
    y_min, y_max = plt.ylim()
    x_ = np.linspace(x_min, x_max, nx)
    y_ = np.linspace(y_min, y_max, ny)
    xx, yy = np.meshgrid(x_, y_)
    Z = Qda.predict_proba(np.c_[xx.ravel(), yy.ravel()])
    Z = Z[:, i].reshape(xx.shape)
    contoursQDA = plt.contour(xx, yy, Z, [0.5],colors = color[i])

#用套件算Qda
# Qda = QuadraticDiscriminantAnalysis(tol = 1e-6, store_covariance = True)
# Qda.fit(X, y)
# MissClassRateQDA = 1 - Qda.score(X, y)

Qda = QuadraticDiscriminantAnalysis(tol = 1e-6, store_covariance = True)
K=300
Qda.trainingError = np.zeros(K)
Qda.testingError = np.zeros(K)
for i in range(K):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    Qda.fit(X_train, y_train)
    Qda.trainingError[i] = 1 - Qda.score(X_train, y_train)
    Qda.testingError[i] = 1 - Qda.score(X_test, y_test)

print('QDA training is ' + f'{Qda.trainingError.mean():.3f}')
print('QDA testing is ' + f'{Qda.testingError.mean():.3f}')

plt.grid(lw=0.3)
plt.title('The Training error of QDA is '  f'{Qda.trainingError.mean():.3f}')
# plt.savefig('C:\\Users\\sarah\\OneDrive\\桌面\\satatistic_hw\\XeLaTex\\eps_five\QDA_3_data2.eps', format='eps')
plt.show()


