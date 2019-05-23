import sqlite3

class DB_controller:
	def __init__(self, data_path):
		self.connection = sqlite3.connect(data_path)
		self.cursor = self.connection.cursor()

	def showTables(self):
		sql = "select * from sqlite_master where type='table';"
		self.cursor.execute(sql)
		rows = self.cursor.fetchall()
		for i in rows:
			print(i)

	def get_max_timestamp(self, tableName):
		sql = "select max(datetime) from "+tableName
		self.cursor.execute(sql)
		rows = self.cursor.fetchall()
		return rows[0][0]

	def get_min_timestamp(self, tableName):
		sql = "select min(datetime) from "+tableName
		self.cursor.execute(sql)
		rows = self.cursor.fetchall()
		return rows[0][0]

	def get_distinct_user_list(self, tableName, columnName):
		sql = "select distinct "+columnName+" from "+tableName
		self.cursor.execute(sql)
		rows = self.cursor.fetchall()
		return rows

	def get_value_by_user(self, tableName, user):
		sql = "select * from "+tableName+" where user = '"+user+"'"
		self.cursor.execute(sql)
		rows = self.cursor.fetchall()
		return rows

