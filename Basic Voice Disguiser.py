import numpy as np
import soundfile as sf
from scipy.signal import resample

def pitch_shift(audio, sample_rate, n_steps):
    """
    Shift the pitch of the audio signal.
    :param audio: Input audio signal (numpy array)
    :param sample_rate: Sampling rate of the audio
    :param n_steps: Number of semitones to shift the pitch
    :return: Pitch-shifted audio signal
    """
    # Calculate the new sample rate
    new_sample_rate = sample_rate * (2 ** (n_steps / 12.0))
    
    # Resample the audio to the new sample rate
    num_samples = int(len(audio) * new_sample_rate / sample_rate)
    pitch_shifted_audio = resample(audio, num_samples)
    
    return pitch_shifted_audio

def main():
    # Load the original audio file
    input_file = 'input.wav'
    output_file = 'output.wav'
    
    audio, sample_rate = sf.read(input_file)
    
    # Shift the pitch - this example shifts up by 4 semitones
    pitch_shifted_audio = pitch_shift(audio, sample_rate, 4)
    
    # Save the modified audio
    sf.write(output_file, pitch_shifted_audio, sample_rate)
    print("Pitch shifted audio saved as", output_file)

if __name__ == '__main__':
    main()
