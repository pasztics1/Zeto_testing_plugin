from reportlab.pdfgen import canvas
import numpy as np
from test_data_generation import sample_count

def failure_detection(given_freqs, given_mags, given_phase, measured_freqs, measured_mags, measured_phase, sample_count=sample_count, threshold=0.1):
    failure_result = np.empty((0,), dtype=object)  # Initialize an empty array of object type
    for i in range(sample_count):
        messages = []
        if abs(given_freqs[i] - measured_freqs[i]) > threshold:
            messages.append(f"The {i+1}th element's frequency was inaccurately measured.")
        if abs(given_mags[i] - measured_mags[i]) > threshold:
            messages.append(f"The {i+1}th element's magnitude was inaccurately measured.")
        if abs(given_phase[i] - measured_phase[i]) > threshold:
            messages.append(f"The {i+1}th element's phase was inaccurately measured.")
            print(f'Inaccuracy of {abs(given_phase[i] - measured_phase[i])}')
        if messages:
            failure_result = np.append(failure_result, [messages])
            
    return failure_result




def generate_pdf_report(significant_freqs, significant_magnitudes, significant_phases, random_freqs, random_mags, random_phase):
    report_file_name = 'report-' + '12345' + '.pdf'#meta.capture_id
    c = canvas.Canvas(report_file_name)

    # Header information
    c.drawString(100, 750, 'Subject name: ' + 'Example Example')
    c.drawString(100, 730, 'Study recorded: ' + '00:00:00')
    
    # Actual signals
    c.drawString(100, 700, 'Actual Frequencies: ' + ', '.join(f"{freq:.2f}" for freq in random_freqs))
    c.drawString(100, 680, 'Actual Magnitudes: ' + ', '.join(f"{mag:.2f}" for mag in random_mags))
    c.drawString(100, 660, 'Actual Phases: ' + ', '.join(f"{phase:.2f}" for phase in random_phase))

    # Measured signals
    c.drawString(100, 630, 'Measured Frequencies, Magnitudes, and Phases:')
    y = 610
    for freq, mag, phase in zip(significant_freqs, significant_magnitudes, significant_phases):
        c.drawString(100, y, f"Frequency: {freq:.2f} Hz, Magnitude: {mag:.2f}, Phase: {phase:.2f} radians")
        y -= 20

    # Failure detection results
    c.drawString(100, y - 20, 'Failure Detection Results:')
    y -= 40
    failure_results = failure_detection(random_freqs, random_mags, random_phase, significant_freqs, significant_magnitudes, significant_phases)
    if len(failure_results) == 0:
        c.drawString(100, y, f"All tests passed, no faliure detected!")
        y -= 20
        
    for messages in failure_results:
        for message in messages:
            c.drawString(100, y, message)
            y -= 20
            if y < 40:
                c.showPage()
                y = 750

    c.save()
    return report_file_name