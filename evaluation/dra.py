# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common.Base import get_logger, bc_star

sns.set(color_codes=True)

def ranking(tgt_df):
    rank_df = pd.DataFrame(np.zeros((len(tgt_df), len(tgt_df.columns))), columns=list(tgt_df))
    for col_name in list(tgt_df):
        rank_df[col_name] = np.argsort(tgt_df.sort_values(col_name, axis=0).index) + 1
    return rank_df

def find_nearest(array, value):
	idx = (np.abs(array - value)).argmin()
	return idx

def permu_dis(x, Y, rank_Y):
	rank_z = [rank_Y[col_name][find_nearest(Y[col_name], x[i])] for i, col_name in enumerate(list(Y))]
	d_xy = [max(abs(rank_z - rank_Y.iloc[i])) for i in xrange(len(rank_Y))]
	return min(d_xy)

def non_dis_producing(df_ori):
	col_name = list(df_ori)
	non_dis = pd.DataFrame()
	non_dis[col_name[0]] = df_ori[col_name[0]].drop_duplicates()
	non_dis['key'] = np.ones(len(non_dis))
	for i in xrange(1, len(col_name)):
		tmp = pd.DataFrame()
		tmp[col_name[i]] = df_ori[col_name[i]].drop_duplicates()
		tmp['key'] = np.ones(len(tmp))
		non_dis = non_dis.merge(tmp)
	non_dis = non_dis[col_name]
	return non_dis

def dl_test(df_ori, df_ano):
	non_dis = non_dis_producing(df_ori)
	rank_ori = ranking(df_ori)
	rank_non_dis = ranking(non_dis)
	dist = [permu_dis(df_ano.iloc[i], df_ori, rank_ori) for i in xrange(len(df_ano))]
	dist2 = [permu_dis(df_ano.iloc[i], non_dis, rank_non_dis) for i in xrange(len(df_ano))]
	return dist, dist2

def permutataion(tgt_df):
	#if p_tgt directly = tgt_df, tgt_df would be shuffled too when shuffling p_tgt
	#.copy() can solve this problem
	p_tgt = tgt_df.copy()
	for cn in list(tgt_df):
	    np.random.shuffle(p_tgt[cn])
	return p_tgt

def pl_test(df_ori, df_ano):
	p_ano = permutataion(df_ano)
	rank_ano = ranking(df_ano)
	rank_p_ano = ranking(p_ano)
	dist = [permu_dis(df_ori.iloc[i], df_ano, rank_ano) for i in xrange(len(df_ori))]
	dist2 = [permu_dis(df_ori.iloc[i], p_ano, rank_p_ano) for i in xrange(len(df_ori))]
	return dist, dist2

def permu_dis_match(x, Y, rank_Y):
	rank_z = [rank_Y[col_name][find_nearest(Y[col_name], x[i])] for i, col_name in enumerate(list(Y))]
	d_xy = [max(abs(rank_z - rank_Y.iloc[i])) for i in xrange(len(rank_Y))]
	return np.argmin(d_xy)

def ranking_col(col):
    rank_col = np.argsort(np.argsort(col)) + 1
    return rank_col

def ad_test(df_ori, df_ano):
	tgt_col = raw_input("Input the target attribute name: ")
	match_cols = list(df_ori)
	match_cols.remove(tgt_col)

	p_ano = permutataion(df_ano)
	rank_ano = ranking(df_ano)
	rank_p_ano = ranking(p_ano)

	XY_matchs = [permu_dis_match(df_ori.iloc[i], df_ano[match_cols], rank_ano[match_cols]) for i in xrange(len(df_ori))]
	XYp_matchs = [permu_dis_match(df_ori.iloc[i], p_ano[match_cols], rank_p_ano[match_cols]) for i in xrange(len(df_ori))]
	
	rank_xm = ranking_col(df_ori[tgt_col])
	rank_ym = ranking_col(df_ano[tgt_col])
	rank_ypm = ranking_col(p_ano[tgt_col])

	dist = [abs(rank_xm[i] - rank_ym[XY_matchs[i]]) for i in xrange(len(df_ori))]
	dist2 = [abs(rank_xm[i] - rank_ypm[XYp_matchs[i]]) for i in xrange(len(df_ori))]
	return dist, dist2

def sns_plot(dist, dist2, lab1, lab2):
	sns.distplot(dist, kde_kws={"label":lab1})
	sns.distplot(dist2, kde_kws={"label":lab2})
	sns.plt.show()	

def test_option(df_ori, df_ano):
	print "\n1. Dictionary Linkage Test"
	print "2. Permuted Linkage Test"
	print "3. Attribute Disclosure Test"
	opt = raw_input("Enter your choice [1-3]: ")
	if opt == '1':
		dist, dist2 = dl_test(df_ori, df_ano)
		sns_plot(dist, dist2, "ano vs ori", "ano vs non_dis")
	elif opt == '2':
		dist, dist2 = pl_test(df_ori, df_ano)
		sns_plot(dist, dist2, "ori vs ano", "ori vs p_ano")
	elif opt == '3':
		dist, dist2 = ad_test(df_ori, df_ano)
		sns_plot(dist, dist2, "ori vs ano", "ori vs p_ano")
	else:
		print 'No this option.'

def Bhattacharyya(dist, dist2):
	d_min = min(min(dist), min(dist2))
	d_max = max(max(dist), max(dist2))
	dist_pmf = [dist.count(i)/len(dist) for i in xrange(d_min, d_max+1)]
	dist2_pmf = [dist2.count(i)/len(dist2) for i in xrange(d_min, d_max+1)]
	#print dist_pmf
	#print dist2_pmf
	bc_coef = sum([np.sqrt(dist_pmf[i]*dist2_pmf[i]) for i in xrange(d_max-d_min+1)])
	#print bc_coef
	bc_star(bc_coef)

def dra_summary(df_ori, df_ano):
	print "\nDictionary Linkage Test"
	dist, dist2 = dl_test(df_ori, df_ano)
	Bhattacharyya(dist, dist2)
	#sns_plot(dist, dist2, "ano vs ori", "ano vs non_dis")
	print "\nPermuted Linkage Test"
	dist, dist2 = pl_test(df_ori, df_ano)
	Bhattacharyya(dist, dist2)
	#sns_plot(dist, dist2, "ano vs ori", "ano vs non_dis")
	print "\nAttribute Disclosure Test"
	dist, dist2 = ad_test(df_ori, df_ano)
	Bhattacharyya(dist, dist2)
	#sns_plot(dist, dist2, "ano vs ori", "ano vs non_dis")
