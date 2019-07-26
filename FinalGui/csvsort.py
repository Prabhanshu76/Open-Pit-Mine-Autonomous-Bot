import pandas as pd

class csv_sort():
	def sort_val(self):	
		"""
		Function Used to sort dataset in descending order for Z coordinate
		"""
		data = pd.read_csv('trainData2.csv')
		data.sort_values("Z", axis=0, ascending=False, inplace=True, na_position='first')
		data.to_csv('trainData2.csv',index = False)



   