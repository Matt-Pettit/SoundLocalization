import requests
import subprocess
import wave
import numpy as np
def record(counter):
    # Define the command and its parameters
    base_command = "arecord -d 3 -D plughw:0 -c2 -r 48000 -f S32_LE -t wav -V stereo -v file_stereo"+str(counter)+".wav"
    file_path = "file_stereo"+str(counter)+".wav"
    subprocess.run(base_command, shell=True)

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

    return left_channel.tolist(), right_channel.tolist()
count = 0
while True:
    # Make a GET request to the first URL
    response = requests.get('http://192.168.1.123:5000/whentorecord/pi1_2')
    # Print the response
    print(response.text)
    # Make a GET request to the second URL

    arrayleft, arrayright = record(count)
    print(len(arrayleft))
    json_data = {'arrayleft': arrayleft, 'arrayright': arrayright, "name": "pi1_2"}
    # Send a POST request to the Flask app
    response = requests.post('http://192.168.1.123:5000/recording', json=json_data)
    # Print the response status code
    print(response.text)
    count += 1
