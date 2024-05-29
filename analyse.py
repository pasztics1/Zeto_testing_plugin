import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from generate_pdf import generate_pdf_report

TESTING = False


def analyse(original_signal, sampling_rate,plotting=False):
    if len(original_signal)%2:
        signal_fft = np.fft.fft(original_signal)[0:(len(original_signal)+1)/2]
    else:
        signal_fft = np.fft.fft(original_signal)[0:int(1+(len(original_signal)/2))]

    freqs = np.fft.fftfreq(len(original_signal), 1.0/sampling_rate)

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
    global significant_freqs, significant_magnitudes, significant_phases
    significant_freqs = positive_freqs[peaks]
    significant_magnitudes = magnitudes[peaks]

    significant_phases = phases[peaks]

    if plotting:
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





if TESTING:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'test_data'))
    from test_data_generation import combined_signal, sampling_rate, random_freqs, random_mags, random_phase
    analyse(combined_signal,sampling_rate)
    # Printing results
    print(f'The actual frequencies are {random_freqs}, the actual magnitudes are {random_mags}, the actual phases are {random_phase}')

    for freq, mag, phase in zip(significant_freqs, significant_magnitudes, significant_phases):
        print(f"Frequency: {freq:.2f} Hz, Magnitude: {mag:.2f}, Phase: {phase:.2f} radians")
        
    #generating pdf
    generate_test_pdf_report(significant_freqs, significant_magnitudes, significant_phases, random_freqs, random_mags, random_phase)
    


else:
    from read_data import data_dict, sampling_rate, column_names, file_name #data dict is a dictionary that contains the electrodes' signal in collumns differentiated by their name as the key.
    analisis = np.zeros((3, 19), dtype=object)
    for i in range(1, 20):  # hardcoded, since there are always 19 electrodes
        analyse(data_dict[column_names[i]], sampling_rate)
        analisis[0, i-1] = significant_freqs
        analisis[1, i-1] = significant_magnitudes
        analisis[2, i-1] = significant_phases
    
    generate_pdf_report(analisis[0,:], analisis[1,:], analisis[2,:], report_file_name=f"{file_name.split('.')[0]}-report.pdf") #meta_capture_id majd, valamint majd osszebb lehet vonni a kodot, de lehet mar igy is tomor.