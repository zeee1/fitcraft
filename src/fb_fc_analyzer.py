from DB_controller import DB_controller
from random import *
import pandas as pd
import sqlite3
import time
import matplotlib.pyplot as plt
import datetime

#######################################################
#	* Data
#	- Duration : 2017-01-20 ~ 2017-02-15 and 2017-04-01 ~ 2017 05 04
#	- Type C : fitcraft
#	- Type D : fitbit only
#######################################################

class FB_FC_Analyzer:
	def __init__(self):
		#self.db_contoller = DB_controller("./fitcraft.db")
		self.db_connection = sqlite3.connect("./fitcraft.db")

	# get_sample_user : sample some user and get their data
	def get_sample_user(self,tableName, num_of_user):
		sql = "select user from "+tableName+" order by random() limit "+str(num_of_user)
		sampled_user = pd.read_sql(sql, self.db_connection, index_col = None)
		return sampled_user

	def get_change_of_hearts_by_user(self):
		sampled_user = self.get_sample_user("hearts",3)['user'].tolist()
		print(sampled_user)
		for user in sampled_user:
			#heart_data_by_user = self.db_contoller.get_value_by_user('hearts', user[0])
			#print(heart_data_by_user)
			user_df = pd.read_sql("select * from hearts where user = '"+user+"'", self.db_connection, index_col = None)
			print(user_df)

	# get_userData_by_type : get user data on each type(A,B,C,D,E,F...)
	def get_userData_by_type(self,tableName, typeOfUser):
		sql = "select * from "+tableName+" where user like '"+typeOfUser+"%'"
		data_by_userType = pd.read_sql(sql, self.db_connection, index_col = None)
		return data_by_userType

	# get_common_datetime_by_user : 
	def get_common_datetime_by_user(self, data_by_userType):
		min_time_list = []
		max_time_list = []

		unique_user_list = data_by_userType['user'].drop_duplicates().tolist()

		for user in unique_user_list:
			data_by_user = data_by_userType.loc[data_by_userType['user'] == user,]
			min_time_list.append(min(data_by_user['datetime']))
			max_time_list.append(max(data_by_user['datetime']))

		return (max(min_time_list), min(max_time_list))

	# Visualize two pandas series by Boxplot
	def vs_boxplot_cmp_two_series(self, pd_series_1, pd_series_2, x_label_list, ylabel_txt, graph_title):
		fig = plt.figure()
		ax = fig.add_subplot(111)

		ax.boxplot([pd_series_1, pd_series_2])
		ax.set_xticklabels(x_label_list, fontsize = 12)
		ax.set_ylabel(ylabel_txt, fontsize = 12)
		ax.set_title(graph_title, fontsize = 13)
		#ax.set_ylim(0, 30000)
		plt.show()

	# Preprocess daily steps on fitcraft or fitbit
	def pp_daily_average_steps(self, fb_data, fc_data):
		# result
		fb_daily_step_count = pd.DataFrame()
		fc_daily_step_count = pd.DataFrame()

		# get unique user list
		unique_fb_user_list = fb_data['user'].drop_duplicates().tolist()
		unique_fc_user_list = fc_data['user'].drop_duplicates().tolist()

		# fb - get daily step counts 
		for user in unique_fb_user_list:
			# get data by each user
			user_data = fb_data.loc[fb_data['user'] == user, ]
			user_data['dt'] = pd.to_datetime(user_data['datetime'], unit = 's')
			user_data['date'] = user_data['dt'].dt.date

			start_date = user_data['date'].min()
			end_date = user_data['date'].max()
			index_date = start_date

			while index_date <= end_date:
				data_on_index_date = user_data.loc[user_data['date'] == index_date, ]

				# remove rows that heart value == 0
				valid_data_on_index_date= data_on_index_date.loc[data_on_index_date['value'] != 0, ]
				daily_step_counts = valid_data_on_index_date['value'].sum()

				fb_daily_step_count = fb_daily_step_count.append({'date':index_date, 'user':user, "step_counts" : daily_step_counts}, ignore_index=True)
				
				index_date += datetime.timedelta(days=1)
		
		# fc - get daily step counts
		for user in unique_fc_user_list:
			# get data by each user
			user_data = fc_data.loc[fc_data['user'] == user, ]
			user_data['dt'] = pd.to_datetime(user_data['datetime'], unit = 's')
			user_data['date'] = user_data['dt'].dt.date

			start_date = user_data['date'].min()
			end_date = user_data['date'].max()
			index_date = start_date

			# get each user's daily step counts
			while index_date <= end_date:
				data_on_index_date = user_data.loc[user_data['date'] == index_date, ]

				valid_data_on_index_date= data_on_index_date.loc[data_on_index_date['value'] != 0, ]
				daily_step_counts = valid_data_on_index_date['value'].sum()

				fc_daily_step_count = fc_daily_step_count.append({'date':index_date, 'user':user, "step_counts" : daily_step_counts}, ignore_index=True)
				
				index_date += datetime.timedelta(days=1)

		return (fb_daily_step_count, fc_daily_step_count)


	def compare_step_counts_fb_and_fc(self):
		ex3_fc = self.get_userData_by_type('steps', 'C')
		ex4_fc = self.get_userData_by_type('steps', 'E')
		ex3_fb = self.get_userData_by_type('steps', 'D')
		ex4_fb = self.get_userData_by_type('steps', 'F')

		fitcraft_data = ex3_fc.append(ex4_fc, ignore_index=True)
		fitbit_data = ex3_fb.append(ex4_fb, ignore_index=True)

		daily_step_counts_on_fb_and_fc = self.pp_daily_average_steps(fitbit_data, fitcraft_data)
		print(daily_step_counts_on_fb_and_fc[1])
		print("only fb average: ", daily_step_counts_on_fb_and_fc[0]['step_counts'].mean())
		print("only fb std : ", daily_step_counts_on_fb_and_fc[0]['step_counts'].std())
		print("fitcraft : ", daily_step_counts_on_fb_and_fc[1]['step_counts'].mean())
		print("fitcraft std: ", daily_step_counts_on_fb_and_fc[1]['step_counts'].std())

		self.vs_boxplot_cmp_two_series(daily_step_counts_on_fb_and_fc[0]['step_counts'], daily_step_counts_on_fb_and_fc[1]['step_counts'], ['Fitbit only', 'Fitcraft'], 'Step count', 'Daily Step Count')

	# Data Preprocess - get daily worn time of each user 
	def pp_worn_time(self, fb_data, fc_data):
		# result
		fb_daily_worn_time = pd.DataFrame()
		fc_daily_worn_time = pd.DataFrame()

		# get unique user list
		unique_fb_user_list = fb_data['user'].drop_duplicates().tolist()
		unique_fc_user_list = fc_data['user'].drop_duplicates().tolist()
		print(unique_fb_user_list)	
		print(unique_fc_user_list)

		# fb - get daily worn time 
		for user in unique_fb_user_list:
			# get data by each user
			user_data = fb_data.loc[fb_data['user'] == user, ]
			user_data['dt'] = pd.to_datetime(user_data['datetime'], unit = 's')
			user_data['date'] = user_data['dt'].dt.date

			start_date = user_data['date'].min()
			end_date = user_data['date'].max()
			index_date = start_date

			while index_date <= end_date:
				data_on_index_date = user_data.loc[user_data['date'] == index_date, ]

				# remove rows that heart value == 0
				valid_data_on_index_date= data_on_index_date.loc[data_on_index_date['value'] != 0, ]
				worn_minute_count = valid_data_on_index_date.shape[0]

				fb_daily_worn_time = fb_daily_worn_time.append({'date':index_date, 'user':user, "worn_minutes" : worn_minute_count}, ignore_index=True)
				
				index_date += datetime.timedelta(days=1)
		
		# fc - get daily worn time 
		for user in unique_fc_user_list:
			# get data by each user
			user_data = fc_data.loc[fc_data['user'] == user, ]
			user_data['dt'] = pd.to_datetime(user_data['datetime'], unit = 's')
			user_data['date'] = user_data['dt'].dt.date

			start_date = user_data['date'].min()
			end_date = user_data['date'].max()
			index_date = start_date

			# get each user's daily worn time
			while index_date <= end_date:
				data_on_index_date = user_data.loc[user_data['date'] == index_date, ]

				valid_data_on_index_date= data_on_index_date.loc[data_on_index_date['value'] != 0, ]
				worn_minute_count = valid_data_on_index_date.shape[0]

				fc_daily_worn_time = fc_daily_worn_time.append({'date':index_date, 'user':user, "worn_minutes" : worn_minute_count}, ignore_index=True)
				
				index_date += datetime.timedelta(days=1)

		return (fb_daily_worn_time, fc_daily_worn_time)


	def compare_worn_time_fb_and_fc(self):
		# get fb data and fc data from hearts -> if value in hearts table == 0, user didn't wear fitbit
		ex3_fc = self.get_userData_by_type('hearts', 'C')
		ex4_fc = self.get_userData_by_type('hearts', 'E')
		ex3_fb = self.get_userData_by_type('hearts', 'D')
		ex4_fb = self.get_userData_by_type('hearts', 'F')

		fitcraft_data = ex3_fc.append(ex4_fc,ignore_index=True)
		fitbit_data = ex3_fb.append(ex4_fb,ignore_index=True)
		
		# preprocess each data(fitbit data, fitcraft data)
		daily_worn_time_on_fb_and_fc = self.pp_worn_time(fitbit_data, fitcraft_data)
		print(daily_worn_time_on_fb_and_fc[0]['worn_minutes'].mean())
		print(daily_worn_time_on_fb_and_fc[0]['worn_minutes'].std())
		print(daily_worn_time_on_fb_and_fc[1]['worn_minutes'].mean())
		print(daily_worn_time_on_fb_and_fc[1]['worn_minutes'].std())
		self.vs_boxplot_cmp_two_series(daily_worn_time_on_fb_and_fc[0]['worn_minutes'], daily_worn_time_on_fb_and_fc[1]['worn_minutes'], ['Fitbit only', 'Fitcraft'], 'Worn time(minute)', 'Daily Worn Time')

	#