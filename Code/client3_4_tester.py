import requests
import numpy as np
import time
def generate_random_array(length):
    """Generates a random array of the given length.

    Args:
      length: The length of the array to generate.

    Returns:
      A random array of the given length.
    """

    array = np.random.rand(length)
    return array

while True:
    try:
        # Make a GET request to the first URL
        response = requests.get('http://192.168.0.105:5000/whentorecord/pi3_4')
        # Print the response
        print(response.text)
        time.sleep(3.5)
        # Make a GET request to the second URL
        # Generate a random array of length 1000
        array = generate_random_array(144000)
        # Create a JSON object containing the array
        json_data = {'arrayleft': array.tolist(),"arrayright":  array.tolist(), "name": "pi3_4"}
        # Send a POST request to the Flask app
        print("Sending")
        response = requests.post('http://192.168.0.105:5000/recording', json=json_data)
        # Print the response status code
        print(response.text)
    except:
      continue