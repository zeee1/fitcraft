import pandas as pd

class category_ratio_by_consumed_item:
	def __init__(self, consumed_item_log_path, user_list):
		self.consumed_item_df = pd.read_csv(consumed_item_log_path)
		self.user_list = pd.read_csv(user_list)
		self.total_consume_event_count = self.consumed_item_df.shape[0]

	def get_category_ratio_by_consumed_item(self):
		result = []
		sampled_item_list =["FitSteak", "FitBread", "FitChicken","COOKED_BEEF", "BREAD", "COOKED_CHICKEN", "GRILLED_PORK"]

		for sampled_item in sampled_item_list:
			tmp_dict = {'item':sampled_item, 'hunter':0,'miner':0,'architect':0, 'total_count':0}
			tmpDF= pd.DataFrame()
			if sampled_item == "FitSteak":
				tmpDF1 = self.consumed_item_df.loc[self.consumed_item_df['item'] == sampled_item, ]
				tmpDF2 = self.consumed_item_df.loc[self.consumed_item_df['item'] == "fitSteak", ]
				tmpDF = tmpDF1.append(tmpDF2, ignore_index = True)
			elif sampled_item == "FitChicken":
				tmpDF1 = self.consumed_item_df.loc[self.consumed_item_df['item'] == sampled_item, ]
				tmpDF2 = self.consumed_item_df.loc[self.consumed_item_df['item'] == "fitChicken", ]
				tmpDF = tmpDF1.append(tmpDF2, ignore_index = True)
			else:
				tmpDF = self.consumed_item_df.loc[self.consumed_item_df['item'] == sampled_item, ]
			merge_by_user = pd.merge(tmpDF, self.user_list, on='user')
			count_by_category = merge_by_user.groupby(['user_category']).count()
			rand_series = count_by_category['date']
			index_list = rand_series.index.values.tolist()
			tmp_dict['total_count'] = tmpDF.shape[0]

			if 'hunter' in index_list:
				tmp_dict['hunter'] = rand_series['hunter']
			if 'miner' in index_list:
				tmp_dict['miner'] = rand_series['miner']
			if 'architect' in index_list:
				tmp_dict['architect'] = rand_series['architect']

			tmp_dict['hunter_ratio'] = tmp_dict['hunter']/(tmp_dict['hunter']+tmp_dict['architect']+tmp_dict['miner'])
			tmp_dict['miner_ratio'] = tmp_dict['miner']/(tmp_dict['hunter']+tmp_dict['architect']+tmp_dict['miner'])
			tmp_dict['architect_ratio'] = tmp_dict['architect']/(tmp_dict['hunter']+tmp_dict['architect']+tmp_dict['miner'])
			tmp_dict['all_item_consumed_ratio'] = tmp_dict['total_count']/self.total_consume_event_count

			result.append(tmp_dict)


		resultDF = pd.DataFrame(result)
		resultDF['sampled_item_consumed_ratio'] = resultDF['total_count']/(resultDF['total_count'].sum())
		resultDF.to_csv("../data/pp_data/sampled_item_user_ratio.csv")

		return resultDF

	def consumed_item_count(self):
		result = pd.DataFrame()
		unique_consume_item_list = self.consumed_item_df['item'].drop_duplicates().tolist()

		for item in unique_consume_item_list:
			tmpDF = self.consumed_item_df.loc[self.consumed_item_df['item'] == item, ]
			count_of_consumed = tmpDF.shape[0]
			result = result.append({'item':item, 'count':count_of_consumed}, ignore_index = True)

		result.to_csv("../data/pp_data/consumed_item_count.csv")
