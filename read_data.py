#cd C:\Users\Surface\Desktop\zeto\eeg_testing_plugin
import numpy as np

with open('example_eeg.txt', 'r') as file:
    lines = file.readlines()

data_lines = lines[2:]

cleaned_data = []

for line in data_lines:
    values = line.split()
    values = [float(val) for val in values]
    cleaned_data.append(values)

data_array = np.array(cleaned_data)

column_names = lines[1].split()
data_dict = {column_names[i]: data_array[:, i] for i in range(len(column_names))}

sampling_rate = 1/data_dict['time[s]'][1]
print(sampling_rate)



