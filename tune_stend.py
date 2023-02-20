import time
import pandas as pd
import numpy as np
from datetime import datetime
import os
import csv

start_time = time.time()
content = os.listdir('//pk-41/stend/epsgranta_ipmstend_new/.arch')
print(content)
print(len(content))
print("Операция выполнена за %s секунд" % (time.time() - start_time))

