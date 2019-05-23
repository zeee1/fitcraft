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

class Log_Cleanser:
	def __init__(self, third_dirPath, forth_dirPath, cleansed_log_path):
		self.third_dirPath = third_dirPath
		self.forth_dirPath = forth_dirPath
		self.third_file_path_list = glob.glob(third_dirPath+"*.log")
		self.forth_file_path_list = glob.glob(forth_dirPath+"*.log")
		self.all_file_path_list = self.third_file_path_list+self.forth_file_path_list
		self.cl_dir_path = cleansed_log_path

	def log_cleansing(self, origin_file_path, new_file_path):
		result = []

		splited_file_path = origin_file_path.split("/")
		file_name = splited_file_path[len(splited_file_path)-1]
		date = file_name.split("-")[0]
		date = datetime.datetime.strptime(date, "%Y%m%d").date()

		reg_expre = re.compile('^\[[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\] \[Server thread/INFO\]: ')
		data_reg_expre = re.compile('^\{\"event\":')

		f = open(origin_file_path, 'r')

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

						if self.is_valid(user, event_name, item):
							tmp_dict = {'date':date,'time':time,'user':user, 'event_name':event_name, 'item':item}
							result.append(tmp_dict)
				else:
					log_dict = ast.literal_eval(log_data)
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

						tmp_dict = {'date':date,'time':time,'user':user, 'event_name':event_name, 'item':item}
						result.append(tmp_dict)

		resultdf = pd.DataFrame(result)
		resultdf.to_csv(new_file_path)

	def all_log_cleansing(self):
		new_file_dir = "../data/cleansed_log/"
		
		for file_path in self.all_file_path_list:
			print(file_path)
			splited_file_path = file_path.split("/")
			file_name = splited_file_path[len(splited_file_path)-1]
			splited_file_name = file_name.split(".")
			file_name = splited_file_name[0]+".csv"
			new_file_path = new_file_dir+file_name
			self.log_cleansing(file_path, new_file_path)
		
	def is_valid(self,user_value, event_value, item_value):
		# remove at least error log
		if "com.mojang.authlib" in user_value or "Disconnecting" in user_value or " " in user_value or "CommandBlock at" in user_value:
			return False
		return True

	# merge all day's log to one data frame and save it file
	def merge_file(self):
		cl_file_path_list = glob.glob(self.cl_dir_path+"*.csv")
		log_dump = pd.DataFrame()
		for file_path in cl_file_path_list:
			tmpDF = pd.read_csv(file_path)
			log_dump = log_dump.append(tmpDF, ignore_index = True)

		log_dump.to_csv("../data/cleansed_log/log_dump.csv")