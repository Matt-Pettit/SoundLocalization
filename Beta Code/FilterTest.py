import wave
from scipy.signal import butter, lfilter
import numpy as np
from multiprocessing import Process
import time
def gcc_phat(sig, refsig, fs=1, max_tau=0.1, interp=16):
    '''
    This function computes the offset between the signal sig and the reference signal refsig
    using the Generalized Cross Correlation - Phase Transform (GCC-PHAT)method.
    '''
    sig = np.array(sig)
    refsig = np.array(refsig)
    print(type(sig))
    print(type(refsig))
    # make sure the length for the FFT is larger or equal than len(sig) + len(refsig)
    n = sig.shape[0] + refsig.shape[0]

    # Generalized Cross Correlation Phase Transform
    SIG = np.fft.rfft(sig, n=n)
    REFSIG = np.fft.rfft(refsig, n=n)
    R = SIG * np.conj(REFSIG)

    cc = np.fft.irfft(R / np.abs(R), n=(interp * n))

    max_shift = int(interp * n / 2)
    if max_tau:
        max_shift = np.minimum(int(interp * fs * max_tau), max_shift)

    cc = np.concatenate((cc[-max_shift:], cc[:max_shift+1]))

    # find max cross correlation index
    shift = np.argmax(np.abs(cc)) - max_shift

    tau = shift / float(interp * fs)
    
    return tau

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def threadfunc(right_channel,left_channel,sr):
    fs = sr
    lowcut = 200
    highcut = 20000

    left_channel = butter_bandpass_filter(left_channel, lowcut, highcut, fs, order=6)
    right_channel = butter_bandpass_filter(right_channel, lowcut, highcut, fs, order=6)
    left_channel = butter_bandpass_filter(left_channel, lowcut, highcut, fs, order=6)
    right_channel = butter_bandpass_filter(right_channel, lowcut, highcut, fs, order=6)
    print("Filtered:")
    print(343*1000* gcc_phat(right_channel,left_channel,sr))


file_path = "file_stereo2.wav"


"""Read stereo WAV file and return left and right channel data"""
wav_file = wave.open(file_path, 'rb')
sr = wav_file.getframerate()
num_frames = wav_file.getnframes()
num_channels = wav_file.getnchannels()
sample_width = wav_file.getsampwidth()

if num_channels != 2:
    raise ValueError("Input file is not stereo.")

data = wav_file.readframes(num_frames)
wav_file.close()

if sample_width == 2:
    data = np.frombuffer(data, dtype=np.int16)
elif sample_width == 4:
    data = np.frombuffer(data, dtype=np.int32)

left_channel = data[::2]  # Assuming 16-bit or 32-bit stereo data
right_channel = data[1::2]  # Assuming 16-bit or 32-bit stereo data

print("len", len(left_channel))
t = time.time()
    
thread1 = Process(target=threadfunc, args=(right_channel,left_channel,sr,))
thread2 = Process(target=threadfunc, args=(right_channel,left_channel,sr,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()
elapsedmulti = time.time() - t


t = time.time()
################################################################
for i in range(2):
    fs = sr
    lowcut = 200
    highcut = 20000
    #print("Nonfiltered:")
    #print(343*1000* gcc_phat(right_channel,left_channel,sr))
    left_channel = butter_bandpass_filter(left_channel, lowcut, highcut, fs, order=6)
    right_channel = butter_bandpass_filter(right_channel, lowcut, highcut, fs, order=6)
    left_channel = butter_bandpass_filter(left_channel, lowcut, highcut, fs, order=6)
    right_channel = butter_bandpass_filter(right_channel, lowcut, highcut, fs, order=6)
    #print("Filtered:")
    print(343*1000* gcc_phat(right_channel,left_channel,sr))
################################################################
elapsedsingle = time.time() - t



# Define output file name
output_file_path = "file_stereo2filtered.wav"

# Set the parameters for the output WAV file
output_sr = sr  # Sample rate
output_sample_width = sample_width
output_num_channels = 2  # Stereo

# Create a new WAV file for writing
output_wav_file = wave.open(output_file_path, 'wb')
output_wav_file.setnchannels(output_num_channels)
output_wav_file.setsampwidth(output_sample_width)
output_wav_file.setframerate(output_sr)

# Combine the left and right channel data into stereo data
stereo_data = np.empty(len(left_channel) + len(right_channel), dtype=data.dtype)
stereo_data[::2] = left_channel
stereo_data[1::2] = right_channel

# Write the stereo data to the output WAV file
output_wav_file.writeframes(stereo_data.tobytes())

# Close the output WAV file
output_wav_file.close()

print(f"Filtered stereo WAV file written to {output_file_path}")


print("Multicore")
print("Runtime:",elapsedmulti)
print("Serial")
print("Runtime:",elapsedsingle)