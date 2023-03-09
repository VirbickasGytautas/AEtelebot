#import csv
import time
import pandas as pd
import numpy as np
from datetime import datetime

pd.set_option('display.width', 1400)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
start_time = time.time()

file = r'\\pk-55\CSV\tmpID.csv'
today = datetime.today().strftime('%d.%m.%Y %H:%M:%S')

start_time = time.time()
stic = open('stic/error.webp', 'rb')
uSD = '2023.02.01'
uED = '2023.02.28'

print('С', uSD, 'По', uED)
df = pd.read_csv(file, index_col=0, sep=';', names=['1', '2', '3', '4', '5'], on_bad_lines='skip')
df['4'] = pd.to_datetime(df['4'], format='%d.%m.%Y %H:%M:%S')

#fullnewdf = (df['4'] >= '2023.02.01') & (df['4'] <= '2023.02.28')

pivotTable = pd.pivot_table(df, index=['5'], values=['2'], aggfunc='mean')
#fullnewdf = df.loc[fullnewdf]
#fullnewdf = len(fullnewdf.index)
print(pivotTable)
total = (df['4'] > '2023.01.01 00:00:00') & (df['4'] <= today)
total = len(total.index)
		#TODO Обработка CSV по парт-номерам
		#TODO Обработка нескольких CSV

print(total)


print("Операция выполнена за %s секунд" % (time.time() - start_time))


