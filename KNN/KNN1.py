from matplotlib.colors import ListedColormap
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import neighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

D = np.loadtxt('C:/Users/sarah/OneDrive/桌面/satatistic_hw/practice1/LDA/hw_2_data6.txt', comments='#')
# fig = plt.figure(figsize=[6, 4])

X = D[:, 0:2]
y = D[:,2].astype('int') # convert to integers
n = len(y)
cmap_bold = ['#FF007F', '#9933FF']
Group_name = np.array(['Group A', 'Group B'])
plt.figure(figsize=(6, 4))
# sns.scatterplot(x = X[:, 0], y = X[:, 1], \
#     hue = Group_name[y], palette = cmap_bold, \
#  edgecolor = 'black')

K = 20
weights = 'uniform'
Knn = neighbors.KNeighborsClassifier(K, weights = weights)
Knn.fit(X, y)
trainingErr = 1 - Knn.score(X, y)
x_min, x_max = X[:,0].min() - 1, X[:,0].max() + 1
y_min, y_max = X[:,1].min() - 1, X[:,1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),np.arange(y_min, y_max, 0.1))
z = Knn.predict(np.c_[xx.ravel(), yy.ravel()])
Z = z.reshape(xx.shape)
cmap_light = ListedColormap(['#FFCCCC', '#E5CCFF'])

plt.contourf(xx, yy, Z, cmap = cmap_light)

sns.scatterplot(x = X[:, 0], y = X[:, 1], \
    hue = Group_name[y], palette = cmap_bold, edgecolor = 'black')
plt.title('KNN training error = %.3f for K = %i' % (trainingErr,K))

Knn = neighbors.KNeighborsClassifier(K, weights = weights)
G=300
Knn.trainingError = np.zeros(G)
Knn.testingError = np.zeros(G)
for i in range(G):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    Knn.fit(X_train, y_train)
    Knn.trainingError[i] = 1 - Knn.score(X_train, y_train)
    Knn.testingError[i] = 1 - Knn.score(X_test, y_test)

print('KNN(20) training is ' + f'{Knn.trainingError.mean():.3f}')
print('KNN(20) testing is ' + f'{Knn.testingError.mean():.3f}')

# plt.savefig('C:\\Users\\sarah\\OneDrive\\桌面\\satatistic_hw\\XeLaTex\\eps_five\\KNN_2_data6.eps', format='eps')

plt.show()