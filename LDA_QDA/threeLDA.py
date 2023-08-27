#範例五  三群LDA

import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
import numpy.linalg as LA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split

D = np.loadtxt('C:/Users/sarah/OneDrive/桌面/satatistic_hw/practice1/LDA/hw_data8.txt', comments='#')
fig = plt.figure(figsize=[6, 4])

#draw scatter plot
X = D[:, 0:2]
y = D[:,2]
C1, C2, C3 = X[y==0, :], X[y==1, :], X[y==2,:]

plt.scatter(C1[:,0],C1[:,1], c='#FE6F5E', s=10, marker='o',label='Group A')
plt.scatter(C2[:,0],C2[:,1], c='#00CC99', s=10, marker='o',label='Group B')
plt.scatter(C3[:,0],C3[:,1], c='#007FFF', s=10, marker='o',label='Group C')
plt.legend(loc = 'upper left')

x_min, x_max = plt.xlim()
y_min, y_max = plt.ylim()
nx = 100

# Lda = LinearDiscriminantAnalysis(tol = 1e-6)
# K=100
# Lda.trainingError = np.zeros(K)

#用套件畫LDA分界線

color = ['r', 'c', 'b']
for i in range(3):
    X1 = X[y !=i, :]
    y1 = y[y !=i]
    Lda = LinearDiscriminantAnalysis(tol = 1e-6)
    Lda.fit(X1, y1)
    K = Lda.intercept_
    L = Lda.coef_
    f = lambda x : -L[0,0]/L[0,1] * x - K[0]/L[0,1]
    x = np.linspace(x_min, x_max, nx)
    plt.ylim([y_min, y_max])
    plt.plot(x, f(x), color = color[i])


Lda = LinearDiscriminantAnalysis(tol = 1e-6)
K=300
Lda.trainingError = np.zeros(K)
Lda.testingError = np.zeros(K)

for i in range(K):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    Lda.fit(X_train, y_train)
    Lda.trainingError[i] = 1 - Lda.score(X_train, y_train)
    Lda.testingError[i] = 1 - Lda.score(X_test, y_test)

print('LDA training is ' + f'{Lda.trainingError.mean():.3f}')
print('LDA testing is ' + f'{Lda.testingError.mean():.3f}')

# MissClassRateLDA = 1 - Lda.score(X, y)

plt.title('The Training error of LDA is '  f'{Lda.trainingError.mean():.3f}')
plt.grid(lw=0.3)
# plt.savefig('C:\\Users\\sarah\\OneDrive\\桌面\\satatistic_hw\\XeLaTex\\eps_five\LDA_3_data8.eps', format='eps')

plt.show()