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

class log_consume_event_analyzer:
	def __init__(self):
		self.all_file_path_list = glob.glob("../data/serverlog_collection/third/"+"*.log")+glob.glob("../data/serverlog_collection/fourth/"+"*.log")

	def get_consumed_item(self):
		resultDF = pd.DataFrame()
		print(self.all_file_path_list)
		for file_path in self.all_file_path_list:
			result_by_day = self.pp_consumed_item_from_one_day_log(file_path)
			resultDF = resultDF.append(result_by_day, ignore_index = True)

		resultDF.to_csv("../data/ex3+ex4_consumed_item_df.csv")
		return resultDF

	# preprocess : file_path is path of one day log file. get count of each item for one day
	def pp_consumed_item_from_one_day_log(self, file_path):
		splited_file_path = file_path.split("/")
		file_name = splited_file_path[len(splited_file_path)-1]
		date = file_name.split("-")[0]
		date = datetime.datetime.strptime(date, "%Y%m%d").date()

		resultDF = pd.DataFrame()
		reg_expre = re.compile('^\[[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\] \[Server thread/INFO\]: ')
		data_reg_expre = re.compile('^\{\"event\":')

		f = open(file_path, 'r')
		test_count = 0

		while True:
			log_line = f.readline()

			if not log_line:
				break
			
			if reg_expre.match(log_line) is None:
				continue
			else:
				log_data = log_line[33:]
				splited_log_line = log_line.split()
				time = splited_log_line[0]

				if data_reg_expre.match(log_data) is None:
					splited_log_data = log_data.split(',')

					if len(splited_log_data) > 3:
						user = splited_log_data[0]
						event_name = splited_log_data[1]
						item = splited_log_data[2]

						if self.is_valid(user, event_name, item) and event_name == "PlayerItemConsumeEvent":
							tmp_dict = {'date':date,'time':time,'user':user, 'event_name':event_name, 'item':item}
							print(tmp_dict)
							resultDF = resultDF.append(tmp_dict, ignore_index = True)
				else:
					log_dict = ast.literal_eval(log_line[33:])
					event_value = log_dict['event']
					for i in event_value:
						user = ''
						event_name = ''
						item = ''

						if 'item' in i.keys():
							item = i['item']
						if 'type' in i.keys():
							event_name = i['type']
						if 'name' in i.keys():
							user = i['name']

						if event_name == "PlayerItemConsumeEvent":
							tmp_dict = {'date':date,'time':time,'user':user, 'event_name':event_name, 'item':item}
							print(tmp_dict)
							resultDF = resultDF.append(tmp_dict, ignore_index = True)

		f.close()

		return resultDF

	## check one line log is valid
	def is_valid(self,user_value, event_value, item_value):
		event_list = ['PlayerDeathEvent', 'PlayerPickupItemEvent', 'EntityDeathEvent', 'BlockPlaceEvent', 'CraftItemEvent','BlockBreakEvent', 'PlayerItemHeldEvent']
		if "com.mojang.authlib" in user_value or "Disconnecting" in user_value or " " in user_value or "CommandBlock at" in user_value:
			return False
		if event_value not in event_list:
			return False
		return True

	def pp_consumed_item(self):
		resultDict = []
		consumed_item_log= pd.read_csv("../data/ex3+ex4_consumed_item_df.csv")

		unique_consumed_item_list = consumed_item_log['item'].drop_duplicates().tolist()

		for i in unique_consumed_item_list:
			tmpDF = consumed_item_log.loc[consumed_item_log['item'] == i,]
			resultDict.append({'item':i, 'count':tmpDF.shape[0]})

		return resultDict

	def vs_consumed_item(self, consumed_item_count_log_path):
		consumed_item_count = pd.read_csv(consumed_item_count_log_path)
		sampled_item_list =["FitSteak", "FitBread", "FitChicken","COOKED_BEEF", "BREAD", "COOKED_CHICKEN", "GRILLED_PORK"]
		consumed_item_ratio_df = pd.read_csv("../data/pp_data/sampled_item_user_ratio.csv")
		consumed_item_ratio_list = consumed_item_ratio_df.to_dict('records')

		data_for_vs=[{'item':"FitSteak", 'count':564}, {'item':"FitBread", 'count':270}, {'item':"FitChicken", 'count':79}, {'item':"COOKED_BEEF", 'count':163}, {'item':"COOKED_CHICKEN", 'count':381}, {'item':"BREAD", 'count':268}, {'item':"GRILLED_PORK", 'count':182}]

		color_list = ['#a9d98f','#f4e0ae','#7a8485', '#c94c44', '#336e78', '#92769e', '#3c721a']
		category_color = ['#efa146', '#60b2a0', '#886b68']
		category_list = ['Miner', 'Hunter', 'Architect']

		fig = plt.figure(figsize=(12,3))
		chart_ax = fig.add_subplot(111)
		fig.subplots_adjust(bottom = 0.2)
		chart_ax.axis('off')

		left_pos = 0
		left_pos_2 = 0

		ratio_list = []
		total_count_num = 0

		for i in data_for_vs:
			total_count_num += i['count']

		for i in data_for_vs:
			ratio_list.append(i['count']/total_count_num)

		print("-----------------------------------------------------------------")
		chart_ax.barh([0], 0, 1, align='center', color='white', ecolor='black', label=None)
		for i in range(0, len(sampled_item_list)):
			y_pos = 0
			seg_data = ''
			for j in data_for_vs:
				if j['item'] == sampled_item_list[i]:
					seg_data = j
					break
			print(seg_data)
			seg_val = ratio_list[i]
			if "Fit" in seg_data['item']:
				barh = chart_ax.barh([y_pos],[seg_val],height = 0.2, label = sampled_item_list[i],left = left_pos, align='center', edgecolor=['black', 'black'], linewidth=0.5, color = color_list[i])
			else:
				barh = chart_ax.barh([y_pos],[seg_val],height = 0.2, label = sampled_item_list[i],left = left_pos, align='center', edgecolor=['black', 'black'], linewidth=0.5, color = color_list[i], hatch = '//')
			left_pos += seg_val

			## attach text
			patch = barh.get_children()[0]
			bah_position = patch.get_xy()
			x_pos = bah_position[0]+0.5*patch.get_width()
			y_pos = bah_position[1]+0.5*patch.get_height()
			chart_ax.text(x_pos,y_pos, " %.2lf" % (ratio_list[i]), ha='center', fontsize = 10)

		chart_ax.set_yticks([1])
		chart_ax.invert_yaxis()
		chart_ax.set_xlabel('Ratio', fontsize = 12)
		plt.tight_layout()

		
		anchor_vals = (0.45, 0.4)

		plt.legend(loc = "upper center",bbox_to_anchor=anchor_vals, ncol=7, prop = {'size': 10})

		plt.show()

	def compare_consume_count(self):
		data=[{'item':"FitSteak", 'count':564}, {'item':"FitBread", 'count':270}, {'item':"FitChicken", 'count':79}, {'item':"COOKED_BEEF", 'count':163}, {'item':"COOKED_CHICKEN", 'count':381}, {'item':"BREAD", 'count':268}, {'item':"GRILLED_PORK", 'count':182}]

		fitfood_count = 0
		basicfood_count = 0

		for i in data:
			if "Fit" in i['item']:
				fitfood_count += i['count']
			else:
				basicfood_count += i['count']

		print(fitfood_count)
		print(basicfood_count)

	def pp_distribution_of_category_by_consumed_item(self, consume_event_log_df, user_list):
		resultDict = []
		sampled_item_list =["FitSteak", "FitBread", "FitChicken","COOKED_BEEF", "BREAD", "COOKED_CHICKEN", "GRILLED_PORK"]
		sample_item_log= pd.DataFrame()

		for item in sampled_item_list:
			tmpDF = pd.DataFrame()
			if item == "FitSteak":
				tmpDF1 = consume_event_log_df.loc[consume_event_log_df['item'] == item,]
				tmpDF2 = consume_event_log_df.loc[consume_event_log_df['item'] == 'fitSteak',]
				tmpDF = tmpDF1.append(tmpDF2, ignore_index = True)
			elif item == "FitChicken":
				tmpDF1 = consume_event_log_df.loc[consume_event_log_df['item'] == item,]
				tmpDF2 = consume_event_log_df.loc[consume_event_log_df['item'] == 'fitChicken',]
				tmpDF = tmpDF1.append(tmpDF2, ignore_index = True)
			else:
				tmpDF = consume_event_log_df.loc[consume_event_log_df['item'] == item,]
			sample_item_log = sample_item_log.append(tmpDF, ignore_index = True)

		merge_by_user = pd.merge(sample_item_log, user_list, on='user')
		hunter_count = merge_by_user.loc[merge_by_user['user_category'] == 'hunter',].shape[0]
		miner_count = merge_by_user.loc[merge_by_user['user_category'] == 'miner',].shape[0]
		architect_count = merge_by_user.loc[merge_by_user['user_category'] == 'architect',].shape[0]

		resultDict = [{'category':'hunter', 'count':hunter_count},{'category':'miner', 'count':miner_count},{'category':'architect', 'count':architect_count}]
		resultDF = pd.DataFrame(resultDict)
		resultDF['category_ratio'] = resultDF['count']/resultDF['count'].sum()
		resultDF.to_csv("../data/pp_data/distribution_of_category_by_consumed_item.csv")

		return resultDict

	def vs_distribution_of_category_by_consumed_item(self, distribution_of_category_by_consumed_item):
		category_color = ['#efa146', '#60b2a0', '#886b68']
		category_list = ['hunter', 'miner', 'architect']
		label_list = ['Hunter', 'Miner', 'Architect']

		fig = plt.figure(figsize=(12,3))
		chart_ax = fig.add_subplot(111)
		fig.subplots_adjust(bottom = 0.2)
		chart_ax.axis('off')
		chart_ax.barh([0], 0, 1, align='center', color='white', ecolor='black', label=None)
		distribution_of_category_by_consumed_item = distribution_of_category_by_consumed_item.to_dict('records')
		print(distribution_of_category_by_consumed_item)
		left_pos = 0
		for i in range(0, len(category_list)):
			y_pos = 0
			seg_data = ''
			for j in distribution_of_category_by_consumed_item:
				if j['category'] == category_list[i]:
					seg_data = j

			print(seg_data)
			seg_val = seg_data['category_ratio']

			barh = chart_ax.barh([y_pos],[seg_val],height = 0.2, label = label_list[i],left = left_pos, align='center', edgecolor=['black', 'black'], linewidth=0.5, color = category_color[i])

			left_pos += seg_val

			## attach text
			patch = barh.get_children()[0]
			bah_position = patch.get_xy()
			x_pos = bah_position[0]+0.5*patch.get_width()
			y_pos = bah_position[1]+0.5*patch.get_height()
			chart_ax.text(x_pos,y_pos, " %.2lf" % (seg_val), ha='center', fontsize = 8)

		chart_ax.set_yticks([1])
		chart_ax.invert_yaxis()
		chart_ax.set_xlabel('Ratio', fontsize = 12)
		plt.tight_layout()

		
		anchor_vals = (0.5, 0.4)

		plt.legend(loc = "upper center",bbox_to_anchor=anchor_vals, ncol=7, prop = {'size': 10})

		plt.show()

		return 1

	def cal_consumed_fitfood_ratio(self):
		data = pd.read_csv("../data/pp_data/consumed_item_count.csv")
		data = data.to_dict('records')
		food_list = ['WHEAT', 'FitSteak', 'FitChicken', 'COOKED_RABBIT', 'PUMPKIN_PIE', 'fitChicken','fitRabbit','FitBread','COOKED_BEEF','ROTTEN_FLESH','BREAD','GRILLED_PORK','COOKED_CHICKEN','fitSteak','COOKED_FISH','POTATO_ITEM','MELON','POTION','RAW_CHICKEN','BEETROOT','MUTTON','CHORUS_FRUIT','BAKED_POTATO','APPLE','CARROT_ITEM','MUSHROOM_SOUP','COOKED_MUTTON','PORK','RAW_BEEF','COOKIE','BEETROOT_SOUP','GOLDEN_APPLE']

		total_food_consume_count = 0
		fitfood_consume_count = 0
		for food in food_list:
			for row in data:
				if row['item'] == food:
					if "Fit" in food or "fit" in food:
						fitfood_consume_count += row['count']
					total_food_consume_count += row['count']
					break

		print("fitfood ratio : ", fitfood_consume_count/total_food_consume_count*100)
				

