import csv
import time
import pandas as pd
import io
from datetime import datetime


pd.set_option('display.width', 1400)
pd.set_option('display.max_columns', 5)
start_time = time.time()

#start_date = input('Введите дату начала периода в формате дд.мм.гггг Ч:М:С (Пример 24.01.2022 07:00:00): ')
#end_date = input('Введите дату конца периода в формате дд.мм.гггг Ч:М:С (Пример 24.01.2022 07:00:00): ')

#with open("tmpID.csv", encoding='utf-8') as r_file:
#    file_reader = csv.reader(r_file, delimiter = ";")
#    count = sum(1 for row in file_reader)

#print(f'Всего в файле {count} строк.')
file = 'tmpID.csv'
today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
df = pd.read_csv(file, index_col=0, sep=';', names=['1', '2', '3', '4', '5'], on_bad_lines='skip')
df['4'] = pd.to_datetime(df['4'])
newdf = (df['4'] > '13.02.2023 00:00:00') & (df['4'] <= '14.02.2023 00:00:00')
newdf = df.loc[newdf]
total = (df['4'] > '11.01.2023 00:00:00') & (df['4'] <= datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

print('Сегодня:', today)
print('Количество произведенных за выбранный период: ',len(newdf.index))
print('За 2023 год:', len(total.index))
#print(df)


print("Операция выполнена за %s секунд" % (time.time() - start_time))


