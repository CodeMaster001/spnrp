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


# First, create a random data matrix
N = 2000
D = 3

X = numpy.random.randint(2,size=(N,D))




# Apply a random projection so the data's not totally boring
P = numpy.random.randn(D, D)

X = numpy.dot(X, P)

# Construct a tree.  By default, we get a KD-spill-tree with height
# determined automatically, and spill = 25%
ds_context = Context(parametric_types=[Categorical, Categorical,Categorical]).add_domains(X)


print('Building tree...')
T = spatialtree(X,ds_context=ds_context)
T.update_ids()
print(T.getIndices())
spn = T.spn_node_object()


plot_spn(spn, 'basicspn.png')
ll = log_likelihood(spn, X)
#print 'done.'

# Show some useful information about the tree
print( '# items in tree    : '+str(len(T)))
print('Dimensionality     : '+ str(T.getDimension()))
print('Height of tree     : '+ str(T.getHeight()))
#print 'Spill percentage   : ', T.getSpill()
#print 'Split rule         : ', T.getRule()

# If we want to compare accuracy against brute-force search,
# we can make a height=0 tree:
T_root = spatialtree(X, height=0,rule='rp')


# Find the 10 approximate nearest neighbors of the 500th data point
# returned list is row#'s of X closest to the query index, 
# sorted by increasing distance
knn_a = T.k_nearest(X, k=10, index=499)
#print 'KNN approx (index) : ', knn_a

# Now, get the true nearest neighbors
knn_t = T_root.k_nearest(X, k=10, index=499)
#print 'KNN true   (index) : ', knn_t

# Recall rate:
#print 'Recall             : ', (len(set(knn_a) & set(knn_t)) * 1.0 / len(set(knn_t)))

# We can also search with a new vector not already in the tree

# Generate a random test query
query = numpy.dot(numpy.random.randn(D), P)

# Find approximate nearest neighbors
knn_a = T.k_nearest(X, k=10, vector=query)
print('KNN approx (vector): '+str(knn_a))

# And the true neighbors
knn_t = T_root.k_nearest(X, k=10, vector=query)
print('KNN true   (vector): '+str(knn_t))

# Recall rate:
print('Recall'+str((len(set(knn_a) & set(knn_t)) * 1.0 / len(set(knn_t)))))

