import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import plot_confusion_matrix
# D = np.loadtxt('C:/Users/sarah/OneDrive/桌面/satatistic_hw/practice1/LDA/hw_2_data5.txt', comments='#')
# data_dir =  '../ANN/'
D = loadmat('C:/Users/sarah/OneDrive/桌面/satatistic_hw/practice1/ANN/Letters_train.mat')
# D.keys()
X = D['X'] # images
y = D['y'] # labels: single output in 0~9

plt.figure(figsize = (9,6))
# prepare and diaplay a montage of digit images
n, m = 20, 30 # A n x m montage (total mn images)
sz = np.sqrt(X.shape[1]).astype('int') # image size sz x sz 一張28x28的小圖
M = np.zeros((m*sz, n*sz)) # montage image
A = X[:m*n,:] # show the first nm images
# Arrange images to form a montage
for i in range(m) :
    for j in range(n) :
        M[i*sz: (i+1)*sz, j*sz:(j+1)*sz] = \
        A[i*n+j,:].reshape(sz, sz)

plt.imshow(M.T, cmap = plt.cm.gray_r, interpolation = 'nearest')
plt.xticks([])
plt.yticks([])
plt.title('The Montage of handwriting letters')
plt.show()
# print(D.keys())


# prepare data
X_train, X_test, y_train, y_test = train_test_split(X/255, y.ravel(), test_size = 0.2)
# print(X_test.size)
# setup and run
hidden_layers = (30,) # one hidden layer 一層30個神經元
solver = 'adam' # default solver
clf = MLPClassifier(max_iter = 10000, solver = solver,
    hidden_layer_sizes = hidden_layers, verbose = True,
    activation = 'logistic', tol = 1e-6, random_state = 0)
# default activation = ’relu’
clf.fit(X_train, y_train)
y_test_hat = clf.predict(X_test)

score = clf.score(X_test, y_test)
# Confusion matrix
plot_confusion_matrix(clf, X_test, y_test,
    cmap = plt.cm.Reds, normalize = None) #None變成數字 #true比例
plt.title('Testing score ={:.2f}%' .format(100*clf.score(X_test, y_test)))
# plt.savefig('C:\\Users\\sarah\\OneDrive\\桌面\\satatistic_hw\\XeLaTex\\eps_six\\letter_none.eps', format='eps')
plt.show()

# Confusion matrix
plot_confusion_matrix(clf, X_test, y_test,
    cmap = plt.cm.PuBu, normalize = 'true') #None變成數字 #true比例
plt.title('Testing score ={:.2f}%' .format(100*clf.score(X_test, y_test)))
# plt.savefig('C:\\Users\\sarah\\OneDrive\\桌面\\satatistic_hw\\XeLaTex\\eps_six\\num_80_true.eps', format='eps')
plt.show()

# plt.title('Training score ={:.2f}%' .format(100*clf.score(X_test, y_test)))
plt.plot(clf.loss_curve_)
plt.title('Training Loss Curve')
plt.grid()

# plt.savefig('C:\\Users\\sarah\\OneDrive\\桌面\\satatistic_hw\\XeLaTex\\eps_six\\num_80_curve.eps', format='eps')
plt.show()
