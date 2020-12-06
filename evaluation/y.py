# -*- coding: utf-8 -*-
import numpy as np
import logging
from common.Base import get_logger, star

def algorithm(df_ori, df_ano, option, normalization):
	min_ary = np.zeros(len(df_ano))
	opt = {'1': 'min', '2': 'median'}
	for i in xrange(len(df_ano)):
		min_ary[i] = min([sum(abs(df_ano.iloc[i] - df_ori.iloc[j])) for j in xrange(len(df_ori))])
	y = min(min_ary) if option == '1' else np.median(min_ary)
	print 'y = {}'.format(y)
	
	Log = get_logger(__name__)
	Log.info({"y": y, 'option': opt[option], "normalization": normalization})
	logging.shutdown()

def y_privacy(df_ori, df_ano, option):
	print "\nNon-normalization version"
	algorithm(df_ori, df_ano, option, False)

def norm_y_privacy(norm_ori, norm_ano, option):
	print "\nNormalization version"
	algorithm(norm_ori, norm_ano, option, True)

def y_summary(df_ori, df_ano):
	print "\ny-privacy:"

	min_ary = np.zeros(len(df_ano))
	opt = {'1': 'min', '2': 'median'}
	for i in xrange(len(df_ano)):
		min_ary[i] = min([sum(abs(df_ano.iloc[i] - df_ori.iloc[j])) for j in xrange(len(df_ori))])
	y_min = min(min_ary)
	y_median = np.median(min_ary)

	if y_min == 0:
		star(0)
	elif y_median > 0 and y_median <= 1:
		star(1)
	elif y_median > 1 and y_median <= 2:
		star(2)
	elif y_median > 2 and y_median <= 3:
		star(3)
	elif y_median > 3 and y_median <= 4:
		star(4)
	elif y_median > 4:
		star(5)
