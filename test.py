import os
import datetime

time = os.path.getmtime("media/app.py")

print(time)
print(datetime.datetime.fromtimestamp(time))
