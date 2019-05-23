import pandas as pd
import sqlite3
from fb_fc_analyzer import FB_FC_Analyzer
from log_user_category_analyzer import log_user_category_analyzer
from log_consume_event_analyze import log_consume_event_analyzer
import json
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from log_cleanser import Log_Cleanser
from log_get_item_from_each_category import category_ratio_by_consumed_item

def main():
	## First, Cleansing Log Data.
	#log_cleanser = Log_Cleanser("../data/serverlog_collection/third/", "../data/serverlog_collection/fourth/", "../data/cleansed_log/")
	#log_cleanser.all_log_cleansing()
	"""log_cleanser.merge_file()"""

	## Second, Check user category ratio
	log_dump = pd.read_csv("../data/cleansed_log/log_dump.csv")
	ex1 = log_dump.loc[log_dump['date'] < '2017-02-16',]
	print(ex1.shape)

	ex2 = log_dump.loc[log_dump['date'] > '2017-03-31',]
	print(ex2.shape)
	#print(log_dump.shape)
	#user_category_analyzer = log_user_category_analyzer(log_dump)

	
	# get distibution of user category
	#user_game_type_df = user_category_analyzer.determine_each_users_game_type()
	#distribution_of_user_category = user_category_analyzer.pp_cal_distribution_of_each_category()

	# get count of logs related to each category.
	#log_count_of_category = user_category_analyzer.count_each_category_logs()
	
	## visualize
	#user_category_analyzer.vs_user_category(pd.read_csv("../data/pp_data/category_distribution.csv"), pd.read_csv("../data/pp_data/category_log_count.csv"))
	"""analyzer = FB_FC_Analyzer()
	
	## compare worn time on fitbit only and fitcraft
	analyzer.compare_worn_time_fb_and_fc()

	## compare step counts on fitbit only and fitcraft
	analyzer.compare_step_counts_fb_and_fc()"""


	## get consumed item
	#consume_event_analyzer = log_consume_event_analyzer()
	#consume_event_analyzer.compare_consume_count()
	#consumed_item_log_path = "../data/ex3+ex4_consumed_item_df.csv"
	#consumed_item_df = pd.read_csv(consumed_item_log_path)
	#consume_event_analyzer.vs_consumed_item("../data/pp_data/consumed_item_count.csv")
	#user_list = pd.read_csv("../data/pp_data/user_list.csv")
	#consume_event_analyzer.pp_distribution_of_category_by_consumed_item(consumed_item_df, user_list)
	#distribution_of_category_by_consumed_item = pd.read_csv("../data/pp_data/distribution_of_category_by_consumed_item.csv")
	#consume_event_analyzer.cal_consumed_fitfood_ratio()

	"""newtask = category_ratio_by_consumed_item("../data/ex3+ex4_consumed_item_df.csv", "../data/pp_data/user_list.csv")
	print(newtask.get_category_ratio_by_consumed_item())"""



if __name__ == "__main__":
	main()