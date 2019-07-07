#!/usr/bin/env python
'''
CREATED:2011-11-12 08:23:33 by Brian McFee <bmcfee@cs.ucsd.edu>

Spatial tree demo for matrix data
'''


import numpy
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sklearn import preprocessing
from spatialtree import spatialtree
from spn.structure.Base import Context
from spn.io.Graphics import plot_spn
from spn.algorithms.Sampling import sample_instances
from spn.structure.leaves.parametric.Parametric import Categorical, Gaussian
from spn.algorithms.Inference import log_likelihood
from spn.algorithms.splitting.RDC import get_split_cols_RDC_py, get_split_rows_RDC_py
from sklearn.datasets import load_iris,load_digits,fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from spn.algorithms.LearningWrappers import learn_parametric
from spatialtree import SPNRPBuilder

from spn.structure.Base import Product, Sum, assign_ids, rebuild_scopes_bottom_up
from sklearn.metrics import accuracy_score
from numpy.random.mtrand import RandomState
from spn.algorithms.LearningWrappers import learn_parametric, learn_classifier
import urllib
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold
from spn.algorithms.Statistics import get_structure_stats
import numpy as np
import time
numpy.random.seed(42)
numpy.random.seed(42)


def  score(i):
	if i == 'g':
		return 0;
	else:
		return 1;

def one_hot(df,col):
	df = pd.get_dummies([col])
	df.drop()


credit=pd.read_csv("../dataset/Cropland.csv",delimiter=",") 
credit = credit.replace(r'^\s+$', numpy.nan, regex=True)

print(credit.shape)
kf = KFold(n_splits=10,shuffle=True)
theirs = list()
ours = list()
credit =credit.drop(credit.columns[1], axis=1)
credit =credit.drop(credit.columns[2], axis=1)
credit =credit.drop(credit.columns[-1], axis=1)
credit =credit.drop(credit.columns[1], axis=1)
print(credit.head())
credit= (credit - credit.mean()) / (credit.max() - credit.min())
credit.values.astype(float)
ours_time_list = list();
theirs_time_list = list();
theirs_time = 0
ours_time =0 
for train_index, test_index in kf.split(credit):
	X = credit.values[train_index]
	X_test = credit.values[test_index];
	X=numpy.nan_to_num(X)
	X = preprocessing.normalize(X, norm='l2')
	X_test = credit.values[test_index];	
	X_test = numpy.nan_to_num(X_test)
	X_test = preprocessing.normalize(X_test, norm='l2')
	X = X.astype(numpy.float32)
	print(X.shape)
	
	N = X.shape[0]
	D = X.shape[1]
	X_zero = X[X[:,-1]==0]

	context = list()
	Categorical_index = [0]
	for i in range(0,X.shape[1]):
		context.append(Gaussian)





	ds_context = Context(parametric_types=context).add_domains(X)
	print("training normnal spm")
	original = time.time()
	spn_classification = learn_parametric(numpy.array(X),ds_context)


	ll_original = log_likelihood(spn_classification, X)
	ll = log_likelihood(spn_classification, X)
	ll_test = log_likelihood(spn_classification,X_test)
	theirs_time = time.time()-original
	ll_test_original=ll_test

	original = time.time()
	print('Building tree...')
	T = SPNRPBuilder(data=numpy.array(X),ds_context=ds_context,target=X,prob=0.5,leaves_size=2,height=2,spill=0.3)
	T= T.build_spn();
	T.update_ids();

	spn = T.spn_node_object()
	print("Building tree complete")
	ll_test = log_likelihood(spn,X_test)
	ours_time = time.time()-original
	ll_test=ll_test

	print(numpy.mean(ll_test))
	print(numpy.mean(ll_test_original))
	plot_spn(spn, 'basicspn.png')
	plot_spn(spn_classification, 'basicspn-original.png')
	theirs.extend(ll_test_original)
	ours.extend(ll_test)
	print(numpy.mean(ll_test_original))
	print(numpy.mean(ll_test))
	theirs.extend(ll_test_original)
	ours.extend(ll_test)
	theirs_time_list.append(theirs_time)
	ours_time_list.append(ours_time)


#plot_spn(spn_classification, 'basicspn-original.png')
plot_spn(spn, 'basicspn.png')
print("--ll--")
print(theirs)
print(np.mean(theirs))
print(np.var(theirs))
print(np.mean(ours))
print(np.var(ours))
print("------")



print("--tt--")
print(np.mean(theirs_time_list))
print(np.var(theirs_time_list))
print(np.mean(ours_time_list))
print(np.var(ours_time_list))
print("------")






