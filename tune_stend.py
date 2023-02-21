import time
import pandas as pd
import numpy as np
from datetime import datetime
import os
import csv

#Name File like  '-tune_7.13.7_48ff6c068670555550440467_2021-07-17-04-29.zip'
#Name File like '+ tune 7.13.7 55ff6e064856725220091767 2022-10-05-13-38 PK-41.zip'
start_time = time.time()
content = os.listdir('//pk-41/stend/epsgranta_ipmstend_new/.arch')
#content = os.listdir('//FS2/file_server/Отдел качества')

#with open("output.txt", "w") as a:
#    for path, subdirs, files in os.walk(r'//FS2/file_server/Отдел качества'):
#       for filename in files:
#         f = os.path.join(path, filename)
#         a.write(str(f) + os.linesep)

print(content)
print("Операция выполнена за %s секунд" % (time.time() - start_time))

