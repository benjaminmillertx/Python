Advanced SETI Detection Code
Written by Benjamin Miller.


import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import stft
from sklearn.ensemble import RandomForestClassifier

# Generate synthetic radio signal data
def generate_radio_signal(duration, sampling_rate, noise_level=0.1, signal_freq=None):
    time = np.linspace(0, duration, int(sampling_rate * duration))
    noise = np.random.normal(0, noise_level, len(time))  # Gaussian noise

    # Simulate cosmic background noise (low-frequency noise)
    cosmic_noise = np.sin(2 * np.pi * np.random.uniform(0.1, 1) * time)

    # Add artificial signal if signal frequency is provided
    signal = noise + cosmic_noise
    if signal_freq:
        artificial_signal = np.sin(2 * np.pi * signal_freq * time)
        signal += artificial_signal

    return time, signal

# Function to analyze signal using Fourier Transform
def analyze_signal(signal, sampling_rate):
    n = len(signal)
    freq = np.fft.fftfreq(n, d=1/sampling_rate)
    fft_values = fft(signal)
    
    # Only take the positive frequencies
    positive_freq = freq[:n//2]
    positive_fft_values = np.abs(fft_values[:n//2])
    
    return positive_freq, positive_fft_values

# Calculate Signal-to-Noise Ratio (SNR)
def calculate_snr(signal, noise_level):
    signal_power = np.mean(signal**2)
    noise_power = noise_level**2
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

# Perform Time-Frequency Analysis (STFT)
def time_frequency_analysis(signal, sampling_rate):
    f, t, Zxx = stft(signal, fs=sampling_rate, nperseg=256)
    plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
    plt.title('Time-Frequency Analysis (STFT)')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()

# Plot the original signal and its frequency spectrum
def plot_signal(time, signal, freq, fft_values, title):
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(time, signal)
    plt.title(f"{title} - Time Domain Signal")
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')

    plt.subplot(1, 2, 2)
    plt.plot(freq, fft_values)
    plt.title(f"{title} - Frequency Domain Signal")
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Magnitude')

    plt.tight_layout()
    plt.show()

# Machine Learning Classifier
def train_ml_model():
    # Generate labeled data (artificial vs. natural signals) for training
    X = []
    y = []
    for _ in range(100):
        # Natural signal (no artificial component)
        time, natural_signal = generate_radio_signal(5.0, 1000, 0.1)
        freq, fft_values = analyze_signal(natural_signal, 1000)
        X.append(fft_values)
        y.append(0)  # Label 0 for natural

        # Artificial signal (with embedded frequency)
        signal_freq = np.random.uniform(10, 50)  # Random artificial frequency
        time, artificial_signal = generate_radio_signal(5.0, 1000, 0.1, signal_freq)
        freq, fft_values = analyze_signal(artificial_signal, 1000)
        X.append(fft_values)
        y.append(1)  # Label 1 for artificial

    # Train a Random Forest Classifier
    clf = RandomForestClassifier()
    clf.fit(X, y)
    return clf

# Generate and analyze a test signal
def test_signal_detection(clf):
    # Generate a new signal with a random artificial component
    signal_freq = np.random.uniform(10, 50)
    time, test_signal = generate_radio_signal(5.0, 1000, 0.1, signal_freq)
    freq, fft_values = analyze_signal(test_signal, 1000)

    # Predict if the signal is artificial or natural
    prediction = clf.predict([fft_values])
    if prediction == 1:
        print("Artificial signal detected!")
    else:
        print("No artificial signal detected.")
    
    # Time-frequency analysis for advanced visualization
    time_frequency_analysis(test_signal, 1000)
    plot_signal(time, test_signal, freq, fft_values, "Test Signal")

# Main process
if __name__ == "__main__":
    # Train a machine learning model for signal classification
    clf = train_ml_model()

    # Test the model on a new signal
    test_signal_detection(clf)

Key Advanced Features:

    Cosmic Noise Simulation:
        In addition to Gaussian noise, we simulate low-frequency noise representing cosmic background radiation.

    Signal-to-Noise Ratio (SNR):
        We calculate the SNR to assess how strong a potential signal is relative to background noise.

    Time-Frequency Analysis (STFT):
        The Short-Time Fourier Transform (STFT) allows us to analyze how the frequency content of the signal evolves over time, which can be useful for detecting short bursts or varying signals.

    Machine Learning Classifier:
        A Random Forest classifier is trained on synthetic signals to distinguish between natural and artificial signals. It can be improved with more sophisticated datasets, but this gives a basic implementation of ML in SETI detection.

    Enhanced Visualization:
        Time-frequency visualization (STFT) provides a better understanding of signal behavior over time, and standard FFT analysis gives insight into the frequency domain.

How to Use:

    Training:
        The script first trains a machine learning model to classify signals (natural vs. artificial) using randomly generated examples.

    Detection:
        A test signal is generated with a random artificial frequency component, and the model attempts to detect whether the signal is artificial or not.

    Visualization:
        The signal is plotted both in the time domain and the frequency domain, and the STFT visualizes changes in frequency over time.

This more advanced approach includes real-world concepts like SNR, time-frequency analysis, and machine learning, making it more applicable to real-world signal detection challenges like SETI.
