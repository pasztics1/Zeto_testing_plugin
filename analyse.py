import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'test_data'))
from test_data_generation import combined_signal, sampling_rate, random_freqs, random_mags, random_phase, sample_count
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from generate_pdf import generate_pdf_report


if len(combined_signal)%2:
    signal_fft = np.fft.fft(combined_signal)[0:(len(combined_signal)+1)/2]
else:
    signal_fft = np.fft.fft(combined_signal)[0:int(1+(len(combined_signal)/2))]

freqs = np.fft.fftfreq(len(combined_signal), 1.0/sampling_rate)

# Selecting the positive frequencies
positive_freq_indices = np.where(freqs >= 0)
positive_freqs = freqs[positive_freq_indices]
fft_positive = signal_fft[positive_freq_indices]

magnitudes = np.abs(fft_positive)/len(signal_fft)
phases = np.angle(fft_positive)+(np.pi/2) #to normalise the lag compared to cos(x)
phases = (phases + np.pi) % (2 * np.pi) - np.pi #getting the phases into the range of [-pi,pi]


#Finding the peaks
threshold = 0.1
peaks, _ = find_peaks(magnitudes, height=threshold)

# Extracting significant frequencies, magnitudes, and phases
significant_freqs = positive_freqs[peaks]
significant_magnitudes = magnitudes[peaks]

significant_phases = phases[peaks]


# Plotting (Magnitude in terms of time)
plt.figure(figsize=(12, 6))

# Magnitude Spectrum (Magnitude in terms of frequency)
plt.subplot(2, 1, 1)
plt.stem(significant_freqs, significant_magnitudes)
plt.title('Magnitude Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')

# Phase Spectrum (Phase in terms of frequency)
plt.subplot(2, 1, 2)
plt.stem(significant_freqs, significant_phases)
plt.title('Phase Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (radians)')

plt.tight_layout()
plt.show()


# Printing results
print(f'The actual frequencies are {random_freqs}, the actual magnitudes are {random_mags}, the actual phases are {random_phase}')

for freq, mag, phase in zip(significant_freqs, significant_magnitudes, significant_phases):
    print(f"Frequency: {freq:.2f} Hz, Magnitude: {mag:.2f}, Phase: {phase:.2f} radians")


#generating pdf
generate_pdf_report(significant_freqs, significant_magnitudes, significant_phases, random_freqs, random_mags, random_phase)

            


