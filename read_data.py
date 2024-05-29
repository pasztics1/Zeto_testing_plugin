#cd C:\Users\Surface\Desktop\zeto\eeg_testing_plugin
import numpy as np
import os 
current_dir = os.path.dirname(__file__)
file_name = '7point8hzsinetest.txt'
file_path = os.path.join(current_dir, 'test_data', file_name)

with open(file_path, 'r') as file:
    lines = file.readlines()

data_lines = lines[1:]

cleaned_data = []

for line in data_lines:
    values = line.split()
    values = [float(val) for val in values]
    cleaned_data.append(values)

data_array = np.array(cleaned_data)

column_names = lines[0].split()
column_names = [column_names[i].split('[')[0] for i in range(len(column_names))] #stripping the metric units from the names (since they are redundant),
                                                                                 #the times are in seconds, and the signal is mesured in microvolts-

print(column_names)
data_dict = {column_names[i]: data_array[:, i] for i in range(len(column_names))}

sampling_rate = 1/data_dict['time'][1]



