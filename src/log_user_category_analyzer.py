from random import *
import pandas as pd
import time
import matplotlib.pyplot as plt
import datetime
import glob
import re
import ast
import json
from collections import OrderedDict
import numpy as np

class log_user_category_analyzer:
	"""def __init__(self, cl_file_path):
		self.log_dump = pd.read_csv(cl_file_path+"log_dump.csv")
		self.cl_file_path = glob.glob(cl_file_path+"*.csv")
		self.all_file_path_list = glob.glob("../data/serverlog_collection/third/"+"*.log")+glob.glob("../data/serverlog_collection/fourth/"+"*.log")"""

	def __init__(self, all_log_dump):
		self.log_dump = all_log_dump
		
	def determine_each_users_game_type(self):
		result = list()
		hunter_event = ['PlayerDeathEvent', 'PlayerPickupItemEvent', 'EntityDeathEvent']
		architect_event = ['BlockPlaceEvent', 'CraftItemEvent']
		miner_event = ['BlockBreakEvent', 'PlayerItemHeldEvent']

		# get user list(without duplicate) for experiment.
		unique_user_list = self.log_dump['user'].drop_duplicates().tolist()

		# collect each user's log related to hunter, miner, architect event and record count of log about each category
		for user in unique_user_list:
			print("User : ", user)
			event_count_by_user_category = {'user':user, 'hunter' : 0,'miner' : 0, 'architect' : 0}

			log_by_user = self.log_dump.loc[self.log_dump['user'] == user, ]

			for h_event in hunter_event:
				h_log_from_user = log_by_user.loc[log_by_user['event_name'] == h_event,]
				event_count_by_user_category['hunter'] += h_log_from_user.shape[0]

			for m_event in miner_event:
				m_log_from_user = log_by_user.loc[log_by_user['event_name'] == m_event,]
				event_count_by_user_category['miner'] += m_log_from_user.shape[0]

			for a_event in architect_event:
				a_log_from_user = log_by_user.loc[log_by_user['event_name'] == a_event,]
				event_count_by_user_category['architect'] += a_log_from_user.shape[0]


			max_log_count = max([event_count_by_user_category['hunter'], event_count_by_user_category['miner'], event_count_by_user_category['architect']])

			# Determine user's game type
			if max_log_count == event_count_by_user_category['hunter']:
				event_count_by_user_category['user_category'] = 'hunter'
			elif max_log_count == event_count_by_user_category['miner']:
				event_count_by_user_category['user_category'] = 'miner'
			elif max_log_count == event_count_by_user_category['architect']:
				event_count_by_user_category['user_category'] = 'architect'	

			result.append(event_count_by_user_category)
		resultDF = pd.DataFrame(result)
		resultDF.to_csv("../data/pp_data/user_list.csv")

		# row of result : {'user': user, 'hunter': x, 'miner':y, 'architecture':z, 'user_category':'hunter/miner/architect'}
		return result


	def pp_cal_distribution_of_each_category(self, category_by_user_list):
		data_for_vs = pd.DataFrame()
		category_by_user_df = pd.DataFrame(category_by_user_list)
		category_list = ['hunter', 'miner', 'architect']

		for category in category_list:
			tmpDF = category_by_user_df.loc[category_by_user_df['user_category'] == category,]
			data_for_vs = data_for_vs.append({'user_category':category, 'count_of_category':tmpDF.shape[0]},ignore_index=True)

		data_for_vs.to_csv("../data/pp_data/category_distribution.csv")
		return data_for_vs

	
	# count logs related to hunter, miner, architecture
	def count_each_category_logs(self):
		result = pd.DataFrame()
		hunter_event = ['PlayerDeathEvent', 'PlayerPickupItemEvent', 'EntityDeathEvent']
		architect_event = ['BlockPlaceEvent', 'CraftItemEvent']
		miner_event = ['BlockBreakEvent', 'PlayerItemHeldEvent']

		event_count_by_user_category = {'hunter' : 0,'miner' : 0, 'architect' : 0}
		
		for h_event in hunter_event:
			h_log = self.log_dump.loc[self.log_dump['event_name'] == h_event,]
			event_count_by_user_category['hunter'] += h_log.shape[0]

		for m_event in miner_event:
			m_log = self.log_dump.loc[self.log_dump['event_name'] == m_event,]
			event_count_by_user_category['miner'] += m_log.shape[0]

		for a_event in architect_event:
			a_log = self.log_dump.loc[self.log_dump['event_name'] == a_event,]
			event_count_by_user_category['architect'] += a_log.shape[0]

		for key, val in event_count_by_user_category.items():
			result = result.append({'user_category':key, 'count_of_log':val},ignore_index = True)

		result['ratio'] = result['count_of_log']/(result['count_of_log'].sum())*100
		result.to_csv("../data/pp_data/category_log_count.csv")
		return result

	def vs_user_category(self, category_distribution_by_user_df, category_log_ratio):
		y_label = ('User Category', 'Log Count')
		#y_pos = np.arange(len(y_label))
		y_pos = np.array([0,0.8])

		fig = plt.figure(figsize=(14,3))
		ax = fig.add_subplot(111, adjustable='box')
		fig.subplots_adjust(bottom = 0.3)
		patch_handles = []

		category_distribution_by_user_df =category_distribution_by_user_df.to_dict('records')
		category_log_ratio =category_log_ratio.to_dict('records')
		color_list = ['#efa146', '#60b2a0', '#886b68']

		data = np.array([[0.525,0.32],[0.44,0.435],[0.035,0.245]])
		print(data)
		left = np.zeros(2)
		for i, d in enumerate(data):
			print(i, d)
			print("y_pos : ", y_pos)
			patch_handles.append(ax.barh(y_pos, d,height=0.5, color=color_list[i%len(color_list)], align='center', left=left))
			left += d

		category_list = ('Hunter', 'Miner', 'Architect')
		percentages = np.array([[0.525,0.44,0.035],[0.32,0.435,0.245]])
		for j in range(len(patch_handles)):
			for i, patch in enumerate(patch_handles[j].get_children()):
				bl = patch.get_xy()
				x = 0.5*patch.get_width() + bl[0]
				y = 0.5*patch.get_height() + bl[1]
				ax.text(x,y, " %.2lf" % (percentages[i,j]), ha='center', fontsize = 11)
				#ax.legend(patch, handles=category_list)

		
		ax.set_yticks(y_pos)
		ax.set_xlabel('Ratio', fontsize = 12)
		ax.set_yticklabels(y_label, fontsize = 12)
		anchor_vals = (0.5, -0.3)
		ax.legend(category_list,loc ="upper center", bbox_to_anchor = anchor_vals, prop = {'size': 15}, ncol = 3)

		plt.show()

	def vs_user_category_v2(self, category_distribution_by_user_df, category_log_ratio):
		category_distribution_by_user_df['ratio'] = category_distribution_by_user_df['count_of_category']/(category_distribution_by_user_df['count_of_category'].sum())
		print(category_distribution_by_user_df)
		print(category_log_ratio)

		category_distribution_by_user_df.plot(kind='barh', stacked = True)