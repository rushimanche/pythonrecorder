<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">PythonRecorder</h3>

</div>

## About the Project

This project is designed to be used in police and fire departments to help them manage their transmissions on radios and access every message that an unit sends out. It uses a python script that continuously listens to an audio source and records any transmission that comes through to help departments keep track of communications on specific channels. The designed AWS pipeline will store all transmissions in AWS S3 buckets and log data into a RDS  database. The scheduling feature means that it can always run on any computer without need for user input and will automatically update AWS.

## Getting Started
1. Clone repo. Use a GH client or just press the green button, download the ZIP, and unzip it.
2) Make sure you have Python 3 installed to your computer
3) Install all necessary dependencies by running pip install pyaudio, pip install math, pip install struct, pip install wave, pip install time, pip install os. If pyaudio is giving you trouble, try this: run pip install pipwin and then run  pipwin install pyaudio
4) Go to the folder with pythonrecorder and modify the directory variable to the place where you want audio files to be stored. I recommend just making a directory folder within pythonrecorder like I did.
5) run python main.py in terminal.
6) The script is now listening. Please play some form of audio to the microphone to test it.
7) Pro tip: modify the maxSoundVal variable if you want your minimum sound threshold to be higher or lower. The higher it is, the more nuianced the script be in identifying your sound. If your sound is going to be loud, you can increase the variable to the hundreds for your desired value.

## Setting Filename Using Command Line:
```sh
python main.py -f'your desired filename'
```
To prevent constant rewriting of the same name, a mechanism was implemented to append UNIX date time to filename. If this feature is not wanted, please remove this line: ```shfile_name = file_name + str(int(time.time()))```

If filename is not provided, it will default to UNIX date time.

## Setting Path Using Command Line:
```sh
python main.py -f'your desired path'
```
If filename is not provided, it will default to /tmp

