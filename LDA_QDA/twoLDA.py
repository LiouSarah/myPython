#範例 二群LDA

import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
import numpy.linalg as LA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split

D = np.loadtxt('C:/Users/sarah/OneDrive/桌面/satatistic_hw/practice1/LDA/hw_2_data6.txt')
# C:\Users\sarah\OneDrive\桌面\satatistic_hw\practice1\LDA
fig = plt.figure(figsize=[6, 4])

#draw scatter plot
X = D[:, 0:2]
y = D[:,2]
C1, C2 = X[y==0, :], X[y==1, :]

plt.scatter(C1[:,0],C1[:,1], c='c', s=10, marker='o', label = 'Group A')
plt.scatter(C2[:,0],C2[:,1], c='b', s=10, marker='<', label = 'Group B')
# plt.legend(loc='upper left')

x_min, x_max = plt.xlim()
y_min, y_max = plt.ylim()
nx = 100

#用套件畫LDA分界線
X = D[:, 0:2]
y = D[:,2]
Lda = LinearDiscriminantAnalysis(tol = 1e-6)
Lda.fit(X, y)
K = Lda.intercept_
L = Lda.coef_
MissClassRateLDA = 1 - Lda.score(X, y)
f = lambda x : -L[0,0]/L[0,1] * x - K/L[0,1]
x = np.linspace(x_min, x_max, nx)
plt.ylim([y_min, y_max])

plt.plot(x, f(x),'#F984E5', label ='LDA '  f'{MissClassRateLDA:.3f}')


#QDA畫曲線
Qda = QuadraticDiscriminantAnalysis(tol = 1e-6, store_covariance = True)
Qda.fit(X, y)
MissClassRateQDA = 1 - Qda.score(X, y)

nx, ny = 100, 100
x_min, x_max = plt.xlim()
y_min, y_max = plt.ylim()
x_ = np.linspace(x_min, x_max, nx)
y_ = np.linspace(y_min, y_max, ny)
xx, yy = np.meshgrid(x_, y_)
Z = Qda.predict_proba(np.c_[xx.ravel(), yy.ravel()])
Z = Z[:, 0].reshape(xx.shape)
contoursQDA = plt.contour(xx, yy, Z, [0.5])
contoursQDA.collections[0].set_label('QDA 'f'{MissClassRateQDA:.3f}')

# 用套件算Qda
Qda = QuadraticDiscriminantAnalysis(tol = 1e-6, store_covariance = True)
Lda = LinearDiscriminantAnalysis(tol = 1e-6)
# Qda.fit(X, y)
# MissClassRateQDA = 1 - Qda.score(X, y)

# MissClassRateLDA = 1 - Lda.score(X, y)
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

# plt.title('The Training error of LDA is '  f'{MissClassRateLDA:.3f}')

legend = plt.legend(['Group A','Group B','LDA'  f'{MissClassRateLDA:.3f}','QDA 'f'{MissClassRateQDA:.3f} '])

#get handles and labels
handles, labels = plt.gca().get_legend_handles_labels()
#specify order of items in legend
order = [1,2,0,3]
#add legend to plot
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc='upper left')
# plt.legend(loc='upper left')
plt.grid(lw=0.3)
# plt.savefig('C:\\Users\\sarah\\OneDrive\\桌面\\satatistic_hw\\XeLaTex\\eps_five\\LDA_2_data6.eps', format='eps')
plt.show()