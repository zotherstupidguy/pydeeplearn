# Handwritten Digit Recognition: LeNet on MNIST
# Author: Sameh Khamis (sameh@umiacs.umd.edu)
# License: GPLv2 for non-commercial research purposes only

import numpy as np
import cPickle, gzip, urllib, os
from pydeeplearn.core.layers import Data, Label, Conv, Pool, FC, Relu, Sum, Softmax
from pydeeplearn.core.solve import RMSprop, Inverse
from pydeeplearn.net.cnn import CNN

# Load the dataset files
mnistfile = 'mnist.pkl.gz'
if not os.path.exists(mnistfile):
    urllib.urlretrieve('http://deeplearning.net/data/mnist/' + mnistfile, mnistfile)

f = gzip.open(mnistfile, 'rb')
train_set, valid_set, test_set = cPickle.load(f)
f.close()

train_set = (train_set[0].reshape(-1, 28, 28, 1), train_set[1].reshape(-1, 1))
valid_set = (valid_set[0].reshape(-1, 28, 28, 1), valid_set[1].reshape(-1, 1))
test_set = (test_set[0].reshape(-1, 28, 28, 1), test_set[1].reshape(-1, 1))

# Create the CNN structure
lambdaa = 1e-4
data = Data(train_set[0].mean(axis=0))
label = Label()
c1 = Conv(data, nfilters=20, window=5, stride=1)
p1 = Pool(c1, window=2, stride=2)
c2 = Conv(p1, nfilters=50, window=5, stride=1)
p2 = Pool(c2, window=2, stride=2)
f1 = FC(p2, ndim=500)
r3 = Relu(f1, leak=0.01)
f2 = FC(r3, ndim=10)
reg = Sum(c1.input[1]**2) + Sum(c2.input[1]**2) + Sum(f1.input[1]**2) + Sum(f2.input[1]**2)
loss = Softmax(f2, label)
obj = loss + lambdaa * reg

# CNN training
cnn = CNN(obj, name='mnist', update=RMSprop(), step=Inverse())
cnn.train(np.r_[train_set[0], valid_set[0]], np.r_[train_set[1], valid_set[1]], epochs=10)

# CNN prediction
predicted = cnn.predict(test_set[0])
print (np.argmax(predicted, axis=1) == test_set[1].reshape(-1)).sum()
