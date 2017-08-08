# -*- coding: utf-8 -*-
import os
import logging
import pandas as pd
from logging.handlers import TimedRotatingFileHandler
import common.constant as c

def load_df_ori():
	while True:
		try:
			file_path = raw_input("Input the file path of original dataset: ")
			df_ori = pd.read_csv(file_path, sep=",")
			break
		except:
			print "Fail to read original dataset, plz try again."
	return df_ori

def load_df_ano():
	while True:
		try:
			file_path = raw_input("Input the file path of anonymized dataset: ")
			df_ano = pd.read_csv(file_path, sep=",")
			break
		except:
			print "Fail to read anonymized dataset, plz try again."
	return df_ano

def load_domain():
	while True:
		try:
			file_path = raw_input("Input the file path of domain: ")
			with open(file_path, "r") as f:
				domain = f.read()
			domain = domain.split(" ")
			break
		except:
			print "Fail to read domain, plz try again."
	return domain

def normalize(tgt_df, df_ori, domain):
	result = pd.DataFrame()
	for idx, col_name in enumerate(list(df_ori)):
		if domain[idx] == 'N':
			col_min = min(df_ori[col_name])
			col_max = max(df_ori[col_name])
			result[col_name] = (tgt_df[col_name] - col_min)/(col_max - col_min)
		else:
			result[col_name] = tgt_df[col_name]
	return result

def check_log(file_path):
	if not os.path.exists(os.path.dirname(file_path)):
		os.makedirs(os.path.dirname(file_path))

	with open(file_path, "a") as my_file:
		pass

def get_logger(name):
	formatter = logging.Formatter("%(asctime)s - %(name)s \t %(levelname)s \t %(message)s")
	handler = TimedRotatingFileHandler(c.LOG_FILE_PATH, when="midnight")
	handler.setFormatter(formatter)
	logger = logging.getLogger(name)
	logger.addHandler(handler)
	logger.propagate = False
	return logger

def Bhattacharyya_distance(p, q):
	pass

def star(num):
	if num != 0 and num <= 5:
		print u"\u2605"*1 + u"\u0020\u2605"*(num-1) + u"\u0020\u2606"*(5-num)
	else:
		print u"\u2606"*1 + u"\u0020\u2606"*4

def prob_star(p):
	if p == 0:
		star(5)
	elif p > 0 and p <= .2:
		star(4)
	elif p > .2 and p <= .4:
		star(3)
	elif p > .4 and p <= .6:
		star(2)
	elif p > .6 and p <= .8:
		star(1)
	elif p > .8 and p <= 1.:
		star(0)

def bc_star(p):
	if p == 0:
		star(0)
	elif p > 0 and p <= .2:
		star(1)
	elif p > .2 and p <= .4:
		star(2)
	elif p > .4 and p <= .6:
		star(3)
	elif p > .6 and p <= .8:
		star(4)
	elif p > .8 and p <= 1.:
		star(5)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s \t %(levelname)s \t %(message)s')