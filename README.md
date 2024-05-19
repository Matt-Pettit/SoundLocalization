# Acoustic Signal Triangulation System 🔊📡
This repository contains the code, simulations, and documentation for an acoustic signal triangulation system designed to locate the position of a sound source within an A1 rectangular grid. The system utilizes Time Difference of Arrival (TDoA) techniques and consists of four microphone breakout boards, two Raspberry Pi microcontrollers, and a graphical user interface (GUI) for displaying results. 🎤🌐

## 🔥 Features
- Audio Signal Capture and Processing: The system captures and processes audio signals from the microphones, ensuring synchronized sampling and accurate time-stamping. 🎚️💻
- Time Delay Computation: Algorithms are implemented to calculate the time delay between pairs of microphones, enabling the determination of the sound source's location. ⏱️🔢
- Sound Localization: Using the computed time delays, the system triangulates the 2D coordinates of the sound source within the A1 grid. 🗺️📍
- Wireless Communication: The Raspberry Pis communicate with each other wirelessly, allowing for efficient data transfer and synchronization. 📶💻
- Graphical User Interface (GUI): A user-friendly GUI provides real-time visualization of the detected sound source's position on a digital grid representation. 👨‍💻🖥️

## 📈 Results
Through extensive simulations and real-world testing, the acoustic signal triangulation system has demonstrated impressive accuracy and precision in localizing sound sources. Here are some key results:
- Time Difference of Arrival (TDoA) Computation: The system achieved an average accuracy of 96.55% in calculating the time delays between microphone pairs, with a standard deviation of 3.33 microseconds. ⏱️💯
- Sound Localization: The calculated sound positions had an average accuracy of 96.25% compared to the actual positions, with an average error of 20.74 millimeters. 🗺️📍
- Real-Time Performance: The system exhibited real-time capabilities, with processing times below 2 seconds for time delay computation and sound localization. ⚡️💨

## 🚀 Getting Started
To get started with this project, follow these steps:
- Clone the repository: git clone https://github.com/quetojenkins/EEE3097S_EngineeringDesign_SoundTriangulationProject.git 📥
- Install the required dependencies (listed in the requirements.txt file). 📦
- Set up the hardware components (Raspberry Pis, microphones, and grid). 🔩
- Run the appropriate scripts to capture audio, compute time delays, localize the sound source, and display the results on the GUI. 🏃‍♂️


## 🤝 Contributors:
- Holly Lewis
- Queto Jenkins
- Matt Pettit

## 📜 License
This project is licensed under the MIT License. ©️
