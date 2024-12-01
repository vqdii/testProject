import pandas as pd
from LaptopFinder import LaptopFinder

#df=pd.read_csv('laptops.csv', index_col='laptop_id', sep=',')
#print(df.query('laptop_id < 10'))
#print(df['company'])
#print(df.info())
#print(df.head/tail(3))
#print(df[['company', 'inches']])
#print(df.loc[[5,10,15],['company', 'inches']])


finder = LaptopFinder('games_data.csv','laptops.csv')
finder.find_suitable_laptops("Dota 2")

