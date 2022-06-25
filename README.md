<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>


  <p align="center">
    PythonRecorder
    <br />
  </p>
</div>


This project is designed to be used in police and fire departments to help them manage their transmissions on radios and access every message that an unit sends out. It uses a python script that continuously listens to an audio source and records any transmission that comes through to help departments keep track of communications on specific channels. The designed AWS pipeline will store all transmissions in AWS S3 buckets and log data into a RDS  database. The scheduling feature means that it can always run on any computer without need for user input and will automatically update AWS.


## Getting Started


1. Clone repo. Use a GH client or just press the green button, download the ZIP, and unzip it.
2) Make sure you have Python 3 installed to your computer
3) Install all necessary dependencies by running pip install pyaudio, pip install math, pip install struct, pip install wave, pip install time, pip install os. If pyaudio is giving you trouble, try this: run pip install pipwin and then run  pipwin install pyaudio
4) Go to the folder with pythonrecorder and modify the directory variable to the place where you want audio files to be stored. I recommend just making a directory folder within pythonrecorder like I did.
5) run python main.py in terminal.
6) The script is now listening. Please play some form of audio to the microphone to test it.
7) Pro tip: modify the maxSoundVal variable if you want your minimum sound threshold to be higher or lower. The higher it is, the more nuianced the script be in identifying your sound. If your sound is going to be loud, you can increase the variable to the hundreds for your desired value.
 







