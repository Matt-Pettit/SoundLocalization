from flask import Flask, Response, request
import threading
import numpy as np
import sympy as sp
app = Flask(__name__)

global connectedwhen1
connectedwhen1 = False
global connectedwhen2
connectedwhen2 = False

global connectedrecord1
connectedrecord1 = False
global connectedrecord2
connectedrecord2 = False   


import random
sem = threading.Semaphore()

global pi1_2_latest_L,pi1_2_latest_R
pi1_2_latest_L = []
pi1_2_latest_R = []

global pi3_4_latest_L,pi3_4_latest_R
pi3_4_latest_L = []
pi3_4_latest_R = []

global host_list
host_list = []

def find_position(tau1_2, tau3_4):
    # Define symbolic variables
    xt, yt = sp.symbols('xt yt')

    # Define microphone positions and speed of sound
    mic1posx, mic1posy = 0, 250
    mic2posx, mic2posy = 800, 250
    mic3posx, mic3posy = 400, 0
    mic4posx, mic4posy = 400, 500
    c = 343 * 10**3

    # Define range equations
    range1 = sp.sqrt((xt - mic2posx)**2 + (yt - mic2posy)**2) - sp.sqrt((xt - mic1posx)**2 + (yt - mic1posy)**2) - c * tau1_2
    range2 = sp.sqrt((xt - mic3posx)**2 + (yt - mic3posy)**2) - sp.sqrt((xt - mic4posx)**2 + (yt - mic4posy)**2) - c * tau3_4

    # Using Simultaneous Equations, find the intersection of the parabolas
    solution = sp.solve([range1, range2], [xt, yt])

    # Print the symbolic solution
    print(f"Symbolic solution: {solution}")

    # Extract the values from the solution
    xt_sol = float(solution[0][0])
    yt_sol = float(solution[0][1])


    return xt_sol, yt_sol


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


def write_values_to_file(x, y):
    file_path = "data.txt"
    try:
        with open(file_path, 'w') as file:
            # Write the values as a comma-separated string to the file
            file.write(f"{x},{y}\n")
        print(f"Values ({x}, {y}) successfully written to '{file_path}'.")
    except Exception as e:
        print(f"Error writing values to '{file_path}': {str(e)}")



@app.route('/whentorecord/<Pi_name>')
def hello(Pi_name):
    global connectedwhen1  # Specify that you want to modify the global variable
    global connectedwhen2  # Specify that you want to modify the global variable

    global connectedrecord1  # Specify that you want to modify the global variable
    global connectedrecord2  # Specify that you want to modify the global variable
    global host_list





    host_list.append(Pi_name)

    if connectedrecord1:
        return("")

    if not connectedwhen1:
        connectedwhen1 = True
        while not connectedwhen2:
            continue
        connectedwhen2 = False
        host_list = []
        return (Pi_name+" Record now")
    else:
        connectedwhen2 = True
        connectedwhen1 = False
        host_list = []
        return (Pi_name+" Record now")

@app.route('/recording', methods=['POST'])
def post_array():
    global connectedwhen1  # Specify that you want to modify the global variable
    global connectedwhen2  # Specify that you want to modify the global variable


    global connectedrecord1  # Specify that you want to modify the global variable
    global connectedrecord2  # Specify that you want to modify the global variable
    global host_list


    global pi1_2_latest_L, pi1_2_latest_R
    global pi3_4_latest_L, pi3_4_latest_R

    if connectedwhen1:
        return("")
    # Get the JSON data from the request
    json_data = request.get_json()

    # Get the array from the JSON data
    arrayleft = json_data['arrayleft']
    arrayright = json_data['arrayright']
    Pi_name = json_data['name']
    # Print the array to the screen
    print(Pi_name+" data sample:" + str(arrayleft[500]))
    print(Pi_name+" data length:" + str(len(arrayleft)))
    print(Pi_name+" data length:" + str(len(arrayright)))

    if not connectedrecord1:
        # now for difficult part
        
        sem.acquire()
        #print("Running Record 1")
        connectedrecord1 = True
        while not connectedrecord2:
            continue
        connectedrecord2 = False

        # d = 1_2 left = mic2
        # b = 1_2 right = mic1
        # c = 3_4 left = mic3
        # a = 3_4 right = mic4
        if (Pi_name == "pi1_2"):
            pi1_2_latest_L, pi1_2_latest_R = np.array(arrayleft),np.array(arrayright)

        if (Pi_name == "pi3_4"):
            pi3_4_latest_L, pi3_4_latest_R = np.array(arrayleft),np.array(arrayright)

        sem.release()
        #

        host_list = []
        return (Pi_name+" Recording accepted")
    else:


        connectedrecord2 = True
        connectedrecord1 = False

        # now for difficult part
        sem.acquire()
        if (Pi_name == "pi1_2"):
            pi1_2_latest_L, pi1_2_latest_R = np.array(arrayleft),np.array(arrayright)

        if (Pi_name == "pi3_4"):
            pi3_4_  latest_L, pi3_4_latest_R = np.array(arrayleft),np.array(arrayright)

        # process both values
        pi1_2_latest_L = pi1_2_latest_L[3200:]
        pi1_2_latest_R = pi1_2_latest_R[3200:]

        pi1_2_tau = gcc_phat(pi1_2_latest_L,pi1_2_latest_R,48000)


        pi3_4_latest_L = pi3_4_latest_L[3200:]
        pi3_4_latest_R = pi3_4_latest_R[3200:]

        pi3_4_tau = gcc_phat(pi3_4_latest_L,pi3_4_latest_R,48000)
        sem.release()
        #
        print("Tau Values:")
        print(pi1_2_tau)
        print(pi3_4_tau)

        print("1_2",pi1_2_tau * 343 * 1000 , " mm")
        print("3_4",pi3_4_tau * 343 * 1000 , " mm")

        #pi1_2_tau= -9.236758582810206e-05  # Replace with your desired value
        #pi3_4_tau = 3.411956478479591e-04 
        #print(pi3_4_tau * 343 * 1000 , " mm")
        xt,yt = find_position(pi1_2_tau, pi3_4_tau)
        xt_string, yt_string = str(xt),str(yt)
        write_values_to_file(xt_string,yt_string)
        host_list = []
        return (Pi_name+" Recording accepted")

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






if __name__ == '__main__':
    app.run(debug=True, threaded=True, host="0.0.0.0")
