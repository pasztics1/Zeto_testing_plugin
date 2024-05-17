import numpy as np
import pyedflib
import os

# Parameters
frequency = 50  #Hz
sampling_rate = 500  # samples per second
duration = 10  # seconds
magnitude = 100 #µV
signal_name = f'{frequency}hz_{magnitude}uV_sin_wave.edf'
#


def generate_sin_wave(frequency, sampling_rate, duration, magnitude):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False) 
    sin_wave = np.sin(2 * np.pi * frequency * t)*magnitude
    return t, sin_wave

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
        'physical_min': -1*magnitude,
        'physical_max': 1*magnitude,
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
t, sine_wave = generate_sin_wave(frequency, sampling_rate, duration, magnitude)


# Checking for duplicate filenames
if not os.path.exists(f'{signal_name}.edf'): 
    save_to_edf(sine_wave, sampling_rate)
else:
    i = 1 
    while os.path.exists(f'{signal_name}_{i}.edf'):
        i += 1
    save_to_edf(sine_wave, sampling_rate)
