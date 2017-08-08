# -*- coding: utf-8 -*-
import pandas as pd
import evaluation.yp as yp
import evaluation.y as y
import evaluation.p as p
import evaluation.dra as dra
import evaluation.idt as idt
import common.constant as c
from common.Base import normalize, check_log, load_df_ori, load_df_ano, load_domain

class Menu(object):
	def __init__(self):
		self.df_ori = load_df_ori()
		self.df_ano = load_df_ano()
		self.domain = load_domain()
		self.norm_ori = normalize(self.df_ori, self.df_ori, self.domain)
		self.norm_ano = normalize(self.df_ano, self.df_ori, self.domain)

	def print_menu(self):
		print 30 * "-" , "MENU" , 30 * "-"
		print "1. yp-privacy"
		print "2. y-privacy"
		print "3. p-privacy"
		print "4. Disclosure Risk Assessment via Record Linkage by a Maximum-Knowledge Attacker"
		print "5. Simple Identity Disclosure Test"
		print "6. Summary"
		print "7. Exit"
		print 67 * "-"

	def start_menu(self):
		while 1:
			self.print_menu()
			choice = input("Enter your choice [1-7]: ")
			if choice==1:     
				yp.yp_privacy(self.df_ori, self.df_ano)
				yp.norm_yp_privacy(self.norm_ori, self.norm_ano)
			elif choice==2:
				print "\n1. min"
				print "2. median"
				opt = raw_input("Enter your choice [1-2]: ")
				y.y_privacy(self.df_ori, self.df_ano, opt)
				y.norm_y_privacy(self.norm_ori, self.norm_ano, opt)
			elif choice==3:
				p.p_privacy(self.df_ori, self.df_ano)
			elif choice==4:
				dra.test_option(self.df_ori, self.df_ano)
			elif choice==5:
				idt.pq_test(self.df_ori, self.df_ano)
			elif choice==6:
				yp.yp_summary(self.norm_ori, self.norm_ano)
				y.y_summary(self.norm_ori, self.norm_ano)
				p.p_summary(self.df_ori, self.df_ano)
				dra.dra_summary(self.df_ori, self.df_ano)
				idt.pq_summary(self.df_ori, self.df_ano)
			elif choice==7:
				break
			else:
				raw_input("No this option. Enter any key to try again.")



if __name__ == '__main__':
	check_log(c.LOG_FILE_PATH)
	menu = Menu()
	menu.start_menu()
