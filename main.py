#importing libraries to run script

import pyaudio
import math
import struct
import wave
import time
import os

#this is where your audio files will be stored. Please change this to meet your liking.
directory = r'C:\Users\dunka\Documents\GitHub\audioproject\directory'

#Some variables to work with

FORMAT = pyaudio.paInt16

#customize number of channels
CHANNELS = 1

SHORT_NORMALIZE = (1.0/32768.0)

chunk = 1024

RATE = 16000

swidth = 2

#customize this value based on background noise. The higher the value, the louder the sound must be to be considered a sound.
maxSoundVal = 50

#Interval AFTER sound finishes that script waits. Don't make this zero.
pauseInterval = 1

class SoundRecorder:

    #calculates current audio level

    @staticmethod
    def calculator(frame):
        vals = len(frame) / swidth
        format = "%dh" % (vals)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        calculator = math.pow(sum_squares / vals, 0.5)

        return calculator * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)

    #function responsible for listening to sound
    def listenForSound(self):
        print('Python listening script initiated!')
        while True:
            input = self.stream.read(chunk)
            current_sound_level = self.calculator(input)
            print(current_sound_level)
            if current_sound_level > maxSoundVal:
                self.recordSound()

    #function responsible for recording sound
    def recordSound(self):
        print('Noise sensed, recording is beginning. To stop the recording, stop noise.')
        currentSoundLevel = []
        current = time.time()
        end = time.time() + pauseInterval

        while current <= end:
            data = self.stream.read(chunk)
            print(data)
            if self.calculator(data) >= maxSoundVal: end = time.time() + pauseInterval

            current = time.time()
            currentSoundLevel.append(data)
        self.save(b''.join(currentSoundLevel))

    #function responsible for uploading sound files
    def save(self, recording):
        n_files = len(os.listdir(directory))

        filename = os.path.join(directory, '{}.wav'.format(n_files))

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        print('Written to file: {}'.format(filename))
        print('Returning to listening')

a = SoundRecorder()

a.listenForSound()