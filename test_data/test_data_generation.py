import numpy as np
import pyedflib
import os
import random
import matplotlib.pyplot as plt

# Parameters
frequency = 50  #Hz
sampling_rate = 500  # samples per second
duration = 10  # seconds
magnitude = 100 #µV
signal_name = f'{frequency}hz_{magnitude}uV_sin_wave.edf'
#


def generate_sin_wave(frequency, sampling_rate, duration, magnitude):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    sin_wave = np.sin(2 * np.pi * frequency * t) * magnitude
    return sin_wave

def save_to_edf(signal, sampling_rate):
    n_channels = 1
    signal_length = len(signal)
    file_duration = signal_length / sampling_rate #?

    #EDF writer
    writer = pyedflib.EdfWriter(signal_name, n_channels, file_type=pyedflib.FILETYPE_EDFPLUS) #https://pyedflib.readthedocs.io/en/latest/

    # Channel parameters
    channel_info = {
        'label': signal_name,
        'dimension': 'μV', 
        'sample_rate': sampling_rate,
        'physical_min': np.min(signal),#-1
        'physical_max': np.max(signal), #1
        'digital_min': -32768,
        'digital_max': 32767,
        'transducer': '', 
        'prefilter': ''
    }

    writer.setSignalHeaders([channel_info])

    # Scaling
    digital_signal = np.int16((signal - np.min(signal)) / (np.max(signal) - np.min(signal)) * 65535 - 32768) #16 bit

    writer.writeSamples([digital_signal])
    writer.close()


# Generate and save sin wave
sine_wave = generate_sin_wave(frequency, sampling_rate, duration, magnitude)

'''
# Checking for duplicate filenames
if not os.path.exists(f'{signal_name}.edf'): 
    save_to_edf(sine_wave, sampling_rate)
else:
    i = 1 
    while os.path.exists(f'{signal_name}_{i}.edf'):
        i += 1
    save_to_edf(sine_wave, sampling_rate)
'''

##Generating sample arrays 
sample_count = 10 #The nr. of signals that will be generated

sampling = np.array(np.arange(0, duration, 1/sampling_rate))
signals = np.zeros((sample_count,len(sampling)))
random_freqs = np.random.randint(1, 10, sample_count)
random_mags = np.random.randint(1, 30, sample_count)

for i in range(sample_count):
    signals[i] = generate_sin_wave(random_freqs[i], sampling_rate, duration, random_mags[i])
    
   

combined_signal = np.sum(signals, axis = 0)

save_to_edf(combined_signal,sampling_rate)


#Plotting 
plt.figure(figsize=(10, 6))

plt.plot(sampling, combined_signal, color='black', label='Summed Signal')

plt.title('Generated Signals')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude μV')
plt.legend()
plt.grid(True)
plt.show()
