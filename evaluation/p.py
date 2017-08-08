# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import pandas as pd
import logging
from itertools import combinations
from itertools import groupby
import networkx 
from common.Base import get_logger, prob_star
from networkx.algorithms.components.connected import connected_components

Log = get_logger(__name__)

def find_crosstab(col1, col2):
	xtab = pd.crosstab(col1, col2)
	return np.asarray(xtab)

def get_expected_sum(xmat):
	rsums = np.sum(xmat, axis = 0).reshape(-1,1)
	csums = np.sum(xmat, axis = 1).reshape(1,-1)
	expected_sum = rsums * csums / float(np.sum(csums))
	return expected_sum

def get_mi(xmat):
	xmat = xmat / float(np.sum(xmat))
	expected_sum = get_expected_sum(xmat)
	summand = xmat/expected_sum.T
	zeros = np.where(summand == 0)
	summand[zeros] = 1
	return np.sum(xmat * np.log(summand))

def g_test(col1, col2, cramer):
	xmat = find_crosstab(col1, col2)
	mi = get_mi(xmat)
	attr1_lvs = sorted(set(col1))
	attr2_lvs = sorted(set(col2))
	min_length = min(len(attr1_lvs), len(attr2_lvs)) - 1

	cv2_lh = mi
	cv2_rh = (cramer ** 2) * min_length/2.
	return cv2_lh >= cv2_rh

def dep_edges(df_ano, cramer):
	filtered_pairs = []
	comb = combinations(list(df_ano), 2)
	for attrs_pair in comb:
		col1_val = df_ano[attrs_pair[0]]
		col2_val = df_ano[attrs_pair[1]]
		if g_test(col1_val, col2_val, cramer):
			filtered_pairs += [attrs_pair]
	return filtered_pairs

def to_graph(nodes, edges):
    G = networkx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

def algorithm(df_ori, df_ano, normalization):
	filtered_pairs = dep_edges(df_ano, 0.2)
	G = to_graph(list(df_ano), filtered_pairs)
	ccs = [list(cc) for cc in connected_components(G)]

	df_predict = df_ano[ccs[0]].drop_duplicates()
	df_predict['key'] = np.ones(len(df_predict))
	for i in xrange(1, len(ccs)):
		tmp = df_ano[ccs[i]].drop_duplicates()
		tmp['key'] = np.ones(len(tmp))
		df_predict = df_predict.merge(tmp)
	df_predict = df_predict[list(df_ano)]
	Xi = len(df_ori.merge(df_predict))
	p = (Xi / len(df_predict)) * (Xi / len(df_ori))
	print "p: {}".format(p)

	Log.info({"p": p, "Xi": Xi, "normalization": normalization})
	logging.shutdown()

def p_privacy(df_ori, df_ano):
	algorithm(df_ori, df_ano, False)

def p_summary(df_ori, df_ano):
	print "\np-privacy"
	filtered_pairs = dep_edges(df_ano, 0.2)
	G = to_graph(list(df_ano), filtered_pairs)
	ccs = [list(cc) for cc in connected_components(G)]

	df_predict = df_ano[ccs[0]].drop_duplicates()
	df_predict['key'] = np.ones(len(df_predict))
	for i in xrange(1, len(ccs)):
		tmp = df_ano[ccs[i]].drop_duplicates()
		tmp['key'] = np.ones(len(tmp))
		df_predict = df_predict.merge(tmp)
	df_predict = df_predict[list(df_ano)]
	Xi = len(df_ori.merge(df_predict))
	p = (Xi / len(df_predict)) * (Xi / len(df_ori))
	prob_star(p)
