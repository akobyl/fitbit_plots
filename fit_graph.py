import json
import matplotlib.pyplot as plt
import os
from datetime import datetime
import pandas as pd

FITBIT_DIRECTORY = "" # Place fitbit folder location here, it should contain all your json files
STEPS_PREFIX = "steps"

step_data = []

for file in [f for f in os.listdir(FITBIT_DIRECTORY) if f.startswith(STEPS_PREFIX)]:
    print(f'Parsing {file}')

    with open(os.path.join(FITBIT_DIRECTORY, file)) as json_file:
        data = json.load(json_file)

        for data_point in data:
            # dateTime is in format '08/14/19 22:23:00'
            time = datetime.strptime(data_point['dateTime'], '%m/%d/%y %H:%M:%S')
            steps = int(data_point['value'])

            step_data.append({'datetime': time, 'steps': steps})

df = pd.DataFrame(step_data)
df.index = df['datetime']

# Create a column of the time stripping the date out to plot time of day data
df['time'] = pd.to_datetime(df['datetime'], format='%H:%M').dt.time

plt.figure()

# Create a list of every day in the dataset, sorted by year, month, day
day_list = [group[1] for group in df.groupby([df.index.year, df.index.month, df.index.day])]

for day in day_list:
    plt.title('Daily Cumulative Steps')
    plt.plot(day['time'].astype('O'), day['steps'].cumsum())


# plt.title('Cumulative Steps')
# plt.plot(df['datetime'].astype('O'), df['steps'].cumsum())
plt.show()
print("done")
