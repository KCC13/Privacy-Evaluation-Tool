# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import logging
from scipy.optimize import linear_sum_assignment
from common.Base import get_logger, prob_star

Log = get_logger(__name__)

def algorithm(df_ori, df_ano, normalization):
	y = float(raw_input("Input y: "))
	p = float(raw_input("Input p: "))

	wt_mat = np.zeros(shape=(len(df_ori), len(df_ano)))
	for i in xrange(len(df_ori)):
		wt_mat[i] = [sum(abs(df_ori.iloc[i] - df_ano.iloc[j])) for j in xrange(len(df_ano))]
	row_ind, col_ind = linear_sum_assignment(wt_mat)
	pp = sum(wt_mat[row_ind, col_ind] < y) / len(df_ori)
	
	if p >= pp:
		print "fulfilled"
	else:
		print "not fulfilled"

	Log.info({"y": y, "p": p, "pp": pp, "fulfilled": p >= pp, "normalization": normalization})
	logging.shutdown()

def yp_privacy(df_ori, df_ano):
	print "Non-normalization version"
	algorithm(df_ori, df_ano, False)

def norm_yp_privacy(norm_ori, norm_ano):
	print "\nNormalization version"
	algorithm(norm_ori, norm_ano, True)

def yp_summary(df_ori, df_ano):
	print "\nyp-privacy:"

	y = len(df_ori.columns)*.1
	wt_mat = np.zeros(shape=(len(df_ori), len(df_ano)))
	for i in xrange(len(df_ori)):
		wt_mat[i] = [sum(abs(df_ori.iloc[i] - df_ano.iloc[j])) for j in xrange(len(df_ano))]
	row_ind, col_ind = linear_sum_assignment(wt_mat)
	pp = sum(wt_mat[row_ind, col_ind] < y) / len(df_ori)
	prob_star(pp)