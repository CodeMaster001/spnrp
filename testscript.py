#!/usr/bin/env python
'''
CREATED:2011-11-12 08:23:33 by Brian McFee <bmcfee@cs.ucsd.edu>

Spatial tree demo for matrix data
'''

import numpy
from spatialtree import spatialtree
from spn.structure.Base import Context
from spn.io.Graphics import plot_spn
from spn.structure.leaves.parametric.Parametric import Categorical, Gaussian
from spn.algorithms.Inference import log_likelihood
from spn.algorithms.splitting.RDC import get_split_cols_RDC_py, get_split_rows_RDC_py
from sklearn.datasets import load_iris,load_digits,fetch_california_housing
from sklearn.model_selection import train_test_split

data = load_digits()

# First, create a random data matrix
print(data.data.shape)

X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.33, random_state=42)
print(y_train.shape)
X = numpy.concatenate((X_train, y_train.reshape(-1,1)),axis=1)
X_test = numpy.concatenate((X_test, y_test.reshape(-1,1)),axis=1)
N = X.shape[0]
D = X.shape[1]

print(X.shape)

# Apply a random projection so the data's not totally boring
P = numpy.random.randn(D, D)

#X = numpy.dot(X, P)

# Construct a tree.  By default, we get a KD-spill-tree with height
# determined automatically, and spill = 25%
context = [Gaussian]*(D-1);
context.append(Categorical)

ds_context = Context(parametric_types=context).add_domains(X)


print('Building tree...')
T = spatialtree(X,ds_context=ds_context)
T.update_ids()
print(T.getIndices())
spn = T.spn_node_object()


plot_spn(spn, 'basicspn.png')
ll = log_likelihood(spn, X_test)
print(numpy.mean(ll))