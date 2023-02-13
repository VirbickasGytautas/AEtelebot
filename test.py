import pandas as pd
import csv
import datetime

#start_date = datetime.strptime(input('Введите дату в формате дд.мм.гггг: '), '%d.%m.%Y')

with open("tmpID.csv", encoding='utf-8') as r_file:
    file_reader = csv.reader(r_file, delimiter = ";")
    count = 0

    for row in file_reader:
        count == 0
        count += 1
    datetime_object = datetime.datetime.now()
    print(datetime_object)
    print(f'Всего в файле {count} строк.')