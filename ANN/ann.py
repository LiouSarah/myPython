
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
# Preaper training data (input)
l1, l2 = 20, 10
t = np.linspace(0, np.pi/2, 20)
l = np.arange(l1 - l2 + 1, l1 + l2 + 1, 2)
X = l.reshape(-1,1) @ np.cos(t.reshape(1,-1))
Y = l.reshape(-1,1) @ np.sin(t.reshape(1,-1))


#circle
l1, l2 = 20, 10
f1 = lambda x: np.sqrt((l1+l2)**2-x**2)
f2 = lambda x: np.sqrt(l2**2-x**2)
plt.figure(figsize=(6,6))

x = np.linspace(0, l1+l2, 100)
plt.fill_between(x, f1(x), 0, color='#F0FFF0')
x = np.linspace(0,l2,100)
plt.fill_between(x, f2(x), 0,color='white')


t=np.linspace(0,np.pi/2,20)
l=np.arange(l1-l2+1,l1+l2+1,2)
X = l.reshape(-1,1)@np.cos(t.reshape(1,-1))
Y = l.reshape(-1,1)@np.sin(t.reshape(1,-1))
plt.scatter(X.ravel(),Y.ravel(),marker='+',s=60,color='#0000CD')
#ravel把向量變矩陣

# prepare training data (output)
theta2 = np.arccos((X.ravel()**2 + Y.ravel()**2 -l1**2 - l2**2)/(2*l1*l2))
theta1 = np.arctan(Y.ravel()/X.ravel()) - \
np.arctan(l2*np.sin(theta2)/(l1+l2*np.cos(theta2)))
# setup for ANN training
InputX = np.c_[X.ravel(), Y.ravel()]
OutputY = np.c_[theta1, theta2]
hidden_layers = (80, )  #隱藏層
solver = 'lbfgs' # the best for robot data
# solver = ’sgd’
# solver = ’adam’
mlp_reg = MLPRegressor(max_iter = 8000, solver = solver,
hidden_layer_sizes = hidden_layers, verbose = False,
activation = 'logistic', # default activation = ’relu’
tol=1e-6, random_state = 0)
mlp_reg.fit(InputX, OutputY) # Training ...
OutputY_hat = mlp_reg.predict(InputX) # Calculate fitted values
theta1_hat, theta2_hat = OutputY_hat[:,0], OutputY_hat[:,1]
# convert to (x,y) positions
x_hat = l1 * np.cos(theta1_hat) + l2 * np.cos(theta1_hat+theta2_hat)
y_hat = l1 * np.sin(theta1_hat) + l2 * np.sin(theta1_hat+theta2_hat)
rmse = np.sqrt(mean_squared_error(OutputY, OutputY_hat))
print('Root Mean square error is {:.4f}'.format(rmse))
LossFun=mlp_reg.loss_
print('The Loss function is {:.4f}'.format(LossFun))

plt.scatter(x_hat,y_hat,marker='o',color='#32CD32')
plt.grid(linestyle='--',lw=0.2)
plt.title('hidden layer is 80 and rmse is {:.4f}'.format(rmse))
# plt.savefig('C:\\Users\\sarah\\OneDrive\\桌面\\satatistic_hw\\XeLaTex\\eps_six\\ann_80.eps', format='eps')

plt.show()


