# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import pandas as pd
from common.Base import get_logger, prob_star

def load_p():
	file_path = raw_input("\nInput the file path of p: ")
	p = None
	with open(file_path, 'r') as f:
		p = f.read()
	p = p.split(' ')
	p = [int(pi) for pi in p]
	return p

def m1(df_ori):
	print "method 1"
	q1 = [i+1 for i in xrange(len(df_ori))]
	return q1

def m2(df_ori, df_ano):
	print "\nmethod 2"
	tgt_clmns = raw_input("Input the target attributes(split by space): ")
	tgt_clmns = tgt_clmns.split(' ')
	sort_ori = df_ori.sort_values(tgt_clmns, axis=0)
	sort_ano = df_ano.sort_values(tgt_clmns, axis=0)
	match = pd.DataFrame({'ori_index' : list(sort_ori.index), 'ano_index' : list(sort_ano.index)})
	q2 = list(match.sort_values('ori_index', axis=0)['ano_index'])
	q2 = map(lambda x: x+1, q2)
	return q2

def m3(df_ori, df_ano):
	print "\nmethod 3"
	tgt_clmn = raw_input("Input the target attribute: ")
	q3 = list(np.zeros(len(df_ano)))
	for i in xrange(len(df_ano)):
		q3[i] = (np.abs(df_ori[tgt_clmn] - df_ano[tgt_clmn][i])).argmin()+1
	return q3

def pq_match(p, q):
	count = 0
	for i in xrange(len(p)):
		if p[i] == q[i]:
			count += 1
	return count / len(p)

def pq_test(df_ori, df_ano):
	p = load_p()
	q1 = m1(df_ori)
	print "method 1 risk: {}%".format(pq_match(p, q1)*100)
	q2 = m2(df_ori, df_ano)
	print "method 2 risk: {}%".format(pq_match(p, q2)*100)
	q3 = m3(df_ori, df_ano)
	print "method 3 risk: {}%".format(pq_match(p, q3)*100)

def pq_summary(df_ori, df_ano):
	print "\nIdentity Disclosure Test:"
	p = load_p()
	q1 = m1(df_ori)
	prob_star(pq_match(p, q1))
	q2 = m2(df_ori, df_ano)
	prob_star(pq_match(p, q2))
	q3 = m3(df_ori, df_ano)
	prob_star(pq_match(p, q3))