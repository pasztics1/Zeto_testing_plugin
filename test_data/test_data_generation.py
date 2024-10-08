import numpy as np
import pyedflib
import os
import matplotlib.pyplot as plt

# Parameters; Use if a specific simple sin wave is needed. Save this instead of the random genearated one.
frequency = 50  #Hz
sampling_rate = 500  # samples per second
duration = 10  # seconds
magnitude = 100 #µV
signal_name = f'{frequency}hz_{magnitude}uV_sin_wave.edf'
plotting = False
#


def generate_sin_wave(frequency, sampling_rate, duration, magnitude, phase):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    sin_wave = np.sin(2 * np.pi * frequency * t + phase) * magnitude
    return sin_wave

def save_to_edf(signal, sampling_rate):
    n_channels = 1

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



##Generating sample arrays 
sample_count = 10 #The nr. of signals that will be generated #The frequencies are hardcoded atm

sampling = np.array(np.arange(0, duration, 1.0/sampling_rate))
signals = np.zeros((sample_count,len(sampling)))


#random -- "given"
random_freqs = np.array([1,2,3,4,5,6,7,8,9,10])

#random_freqs = np.random.randint(1, 10, sample_count)
random_mags = np.random.randint(1, 30, sample_count)

random_phase = np.random.uniform(-np.pi,np.pi, sample_count)
print(random_phase)


for i in range(sample_count):
    signals[i] = generate_sin_wave(random_freqs[i], sampling_rate, duration, random_mags[i], random_phase[i])
    
combined_signal = np.sum(signals, axis = 0)


# Checking for duplicate filenames
if not os.path.exists(f'{signal_name}.edf'): 
    save_to_edf(combined_signal, sampling_rate)
else:
    i = 1 
    while os.path.exists(f'{signal_name}_{i}.edf'):
        i += 1
    save_to_edf(combined_signal, sampling_rate)


save_to_edf(combined_signal,sampling_rate)



#Plotting 
if plotting:
    plt.figure(figsize=(10, 6))

    plt.plot(sampling, combined_signal, color='black', label='Summed Signal')

    plt.title('Generated Signals')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude μV')
    plt.legend()
    plt.grid(True)
    plt.show()
