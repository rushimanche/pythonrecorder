# pythonrecorder
This is a python script that will listen for sound and save it if it hears sound

Setup guide:

1) Clone repo. Use a GH client or just press the green button, download the ZIP, and unzip it.
2) Make sure you have Python 3 installed to your computer
3) Install all necessary dependencies by running pip install pyaudio, pip install math, pip install struct, pip install wave, pip install time, pip install os. If pyaudio is giving you trouble, try this: run pip install pipwin and then run  pipwin install pyaudio
4) Go to the folder with pythonrecorder and modify the directory variable to the place where you want audio files to be stored. I recommend just making a directory folder within pythonrecorder like I did.
5) run python main.py in terminal.
6) The script is now listening. Please play some form of audio to the microphone to test it.
7) Pro tip: modify the maxSoundVal variable if you want your minimum sound threshold to be higher or lower. The higher it is, the more nuianced the script be in identifying your sound. If your sound is going to be loud, you can increase the variable to the hundreds for your desired value.

Setting Filename Using Command Line:

python main.py -f'your desired filename'

To prevent constant rewriting of the same name, a mechanism was implemented to append UNIX date time to filename. If this feature is not wanted, please remove this line: file_name = file_name + str(int(time.time()))

If filename is not provided, it will default to UNIX date time.

Setting Path Using Command Line:

python main.py -f'your desired path'

If filename is not provided, it will default to /tmp

