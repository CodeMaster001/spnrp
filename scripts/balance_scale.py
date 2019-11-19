#!/usr/bin/env python
'''
CREATED:2011-11-12 08:23:33 by Brian McFee <bmcfee@cs.ucsd.edu>

Spatial tree demo for matrix data
'''


import numpy
import sys
import os
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sklearn import preprocessing
from spatialtree import SPNRPBuilder
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
from spn.gpu.TensorFlow import optimize_tf
from spn.structure.Base import Product, Sum, assign_ids, rebuild_scopes_bottom_up
from sklearn.metrics import accuracy_score
from numpy.random.mtrand import RandomState
from spn.algorithms.LearningWrappers import learn_parametric, learn_classifier
import urllib
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import fetch_openml
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold
from spn.gpu.TensorFlow import eval_tf
import time;
numpy.random.seed(42)


def  score(i):
	if i == 'g':
		return 0;
	else:
		return 1;

def one_hot(df,col):
	df = pd.get_dummies([col])
	df.drop()



credit,target = fetch_openml(name='balance-scale', version=2,return_X_y=True)
credit = pd.DataFrame(data=credit)
credit = credit.apply(LabelEncoder().fit_transform)
theirs = list()
ours = list()
kf = KFold(n_splits=10,shuffle=True)
print(credit.shape)
ours_time_list = list();
theirs_time_list = list();

for i in range(10):
	X, X_test = train_test_split(credit, train_size=0.40)

	context = list()
	for i in range(0,X.shape[1]):
		context.append(Categorical)





	ds_context = Context(parametric_types=context).add_domains(X)
	print("training normnal spm")
	
	theirs_time = time.time()
	spn_classification =  learn_parametric(numpy.array(X),ds_context,threshold=0.3,min_instances_slice=2)
	
	
	
	theirs_time = time.time()-theirs_time
	ll_test = log_likelihood(spn_classification,X_test)
	ll_test_original=ll_test




	print('Building tree...')
	original = time.time();
	T = SPNRPBuilder(data=numpy.array(X),ds_context=ds_context,target=X,prob=0.5,leaves_size=2,height=2,spill=0.3)
	
	T= T.build_spn();
	T.update_ids();
	spn = T.spn_node;
	print("Building tree complete")
	ours_time = time.time()-original;
	ours_time_list.append(ours_time)
	ll_test = log_likelihood(spn,X_test)
	print(numpy.mean(ll_test_original))
	print(numpy.mean(ll_test))
	theirs.extend(ll_test_original)
	ours.extend(ll_test)
	theirs_time_list.append(theirs_time)

#plot_spn(spn, 'basicspn.png')
print('---Time---')
print(numpy.mean(theirs_time_list))
print(numpy.var(theirs_time_list))
print(numpy.mean(ours_time_list))
print(numpy.var(ours_time_list))
print('---ll---')
print(numpy.mean(theirs))
print(numpy.var(theirs))
print(numpy.mean(ours))
print(numpy.var(ours))
os.makedirs("results/balance")
numpy.savetxt('results/balance/ours.time', ours_time_list, delimiter=',')
numpy.savetxt('results/balance/theirs.time',theirs_time_list, delimiter=',')
numpy.savetxt('results/balance/theirs.ll',theirs, delimiter=',')
numpy.savetxt('results/balance/ours.ll',ours, delimiter=',')





