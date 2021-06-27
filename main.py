#importing libraries to run script

import pyaudio
import math
import struct
import wave
import time
import os
import sys
import argparse
import logging
import boto3
from botocore.exceptions import ClientError
import pathlib as path

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--path", help="Enter the desired directory", type=str)
parser.add_argument("-f", "--filename", help="Enter the desired file name", type=str)
parser.add_argument("-d", "--device_name", help="Enter the desired device name", type=str)
parser.add_argument("-s", "--stream_id", help="Enter the desired stream id", type=str)
parser.add_argument("-a", "--aws_profile", help="Enter the desired aws profile", type=str)
parser.add_argument("-r", "--rate", help="Enter the desired rate", type=int)

args = parser.parse_args()
directory = args.path if args.path else r'\tmp'
file_name = args.filename if args.filename else ''
device_name = args.device_name if args.device_name else ''
stream_id = args.stream_id if args.stream_id else ''
aws_profile = args.aws_profile if args.aws_profile else ''
input_rate = args.rate if args.rate else ''

directory.encode('unicode_escape')
file_name.encode('unicode_escape')
device_name.encode('unicode_escape')
stream_id.encode('unicode_escape')
aws_profile.encode('unicode_escape')
input_rate.encode('unicode_escape')

#this is where your audio files will be stored. Please change this to meet your liking.
#directory = r'C:\Users\dunka\Documents\GitHub\audioproject\directory'

#Some variables to work with

FORMAT = pyaudio.paInt16

#customize number of channels
CHANNELS = 1

SHORT_NORMALIZE = (1.0/32768.0)

sts = boto3.client('sts')
if not sts.get_caller_identity():
    sys.exit("Improper AWS credentials entered!")


#logic to check for validity of environ variables. if not met, results in defaults

if(os.getenv('chunk') == None or isinstance(os.getenv('chunk'), int)):
    chunk = 1024
else:
    chunk = int(os.getenv('chunk'))
if(os.getenv('RATE') == None or isinstance(os.getenv('RATE'), int)):
    if input_rate:
        RATE = input_rate
    RATE = 16000
else:
    RATE = int(os.getenv('RATE'))

if(os.getenv('directory') == None or isinstance(os.getenv('directory'), int)):
    directory = directory
else:
    directory = os.getenv('directory')

if(not os.path.isdir(directory)): 
    sys.exit('Specified directory does not exist!')
else:
    if os.access(directory, os.W_OK) is not True:
        sys.exit('Specified directory is not writable!')

if(os.getenv('stream_id') == None or isinstance(os.getenv('stream_id'), int)):
    stream_id = stream_id
else:
    stream_id = os.getenv('stream_id')

if device_name == '':
    if(os.getenv('device_name') == None or isinstance(os.getenv('device_name'), int)):
        sys.exit('Device Name Not Found! Please specify device name.')
    else: 
        device_name = os.getenv('device_name')

if stream_id == '':
    if(os.getenv('stream_id') == None or isinstance(os.getenv('stream_id'), int)):
        sys.exit('Stream ID Not Found! Please specify stream id.')
    else: 
        stream_id = os.getenv('stream_id')

if aws_profile == '':
    try:
        aws_profile = os.getenv('aws_profile')
    except:
        pass
    


swidth = 2

#customize this value based on background noise. The higher the value, the louder the sound must be to be considered a sound.
maxSoundVal = 10

#Interval AFTER sound finishes that script waits. Don't make this zero.
pauseInterval = 1

#Amazon S3 Bucket to store recordings
bucketName = 'python-recording-bucket'

class SoundRecorder:

    #calculates current audio level

    @staticmethod
    def calculator(audio):
        
        vals = len(audio) / swidth
        calc_format = "%dh" % (vals)
        shorts_ex = struct.unpack(calc_format, audio)

        counter = 0.0
        for sample in shorts_ex:
            n = sample * SHORT_NORMALIZE
            counter += n * n
        calculator = math.pow(counter / vals, 0.5)

        return calculator * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        global device_name
        global device_id
        device_id = 0
        
        for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device ID:", i, " - ", self.p.get_device_info_by_host_api_device_index(0, i).get('name'))

        for i in range(0, numdevices):
            audio_names = []
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                if(self.p.get_device_info_by_host_api_device_index(0, i).get('name') == device_name):
                    device_id = i

        if device_id == 0:
            sys.exit("Audio device not found! Please modify device_name variable.")

        self.stream = self.p.open(format=FORMAT,
                                input_device_index=device_id,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                output=True,
                                frames_per_buffer=chunk)

    def upload_file(self, file_name, bucket, object_name):
        """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file

        if aws_profile:
            try:
                session = boto3.Session(profile_name=aws_profile)
                s3_client = session.client('s3')
            except:
                print("Selected AWS Profile is not valid! Trying default profile.")
        else:
            try:
                s3_client = boto3.client('s3')
            except:
                sys.exit("Default profile is not valid!")

        try:
            from datetime import date
            global stream_id
            file_prefix = stream_id + '/' + date.today().strftime('%Y/%m/%d')
            response = s3_client.upload_file(file_name, bucket, '{}.mp3'.format(file_prefix + '/' + object_name), ExtraArgs={'ACL':'public-read'})
            
        except ClientError as e:
            pass
        return True

    #function responsible for listening to sound
    def listenForSound(self):
        print('Python listening script initiated!')
        while True:
            if not(self.p.get_device_info_by_host_api_device_index(0, device_id).get('name')):
                sys.exit("Audio device disconnected. Please reconnect!")

            input = self.stream.read(chunk, exception_on_overflow = False)
            current_sound_level = self.calculator(input)
            if current_sound_level > maxSoundVal:
                start_time = int(time.time())
                self.recordSound(start_time)

    #function responsible for recording sound
    def recordSound(self, start_time):
        print('Noise sensed, recording is beginning. To stop the recording, stop noise.')
        currentSoundLevel = []
        current = time.time()
        end = time.time() + pauseInterval

        while current <= end:
            data = self.stream.read(chunk, exception_on_overflow = False)
            if self.calculator(data) >= maxSoundVal: end = time.time() + pauseInterval
            current = time.time()
            currentSoundLevel.append(data)
        duration = start_time - int(time.time())
        self.save(b''.join(currentSoundLevel), duration)

    #function that checks if any files are still remaining in a directory. If it is, send it to s3.
    def checkForRemaining(self, directory):
        dirname = path.Path(directory).glob("*.mp3")
        paths = []

        for file in dirname:
            paths.append(str(file))

        if paths:
            for file in paths:
                try:
                    if '\\' in file:         
                        self.upload_file(file, bucketName, file.split("\\")[-1].replace('.mp3',''))
                        os.remove(file)
                    if '/' in file:
                        self.upload_file(file, bucketName, file.split("/")[-1].replace('.mp3',''))
                        os.remove(file)
                except:
                    pass
                
    #function responsible for uploading sound files
    def save(self, recording, duration):
        try:
            global file_name 
            name_of_file = file_name
            if name_of_file == '':
                name_of_file = str(int(time.time())) + '' + str(duration)
            else:
                name_of_file = name_of_file + '-' + str(int(time.time())) + '-' + str(duration)
                    
            filename = os.path.join(directory, '{}.mp3'.format(name_of_file))
            wf = wave.open(filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(recording)
            self.checkForRemaining(directory)
            self.upload_file(filename, bucketName, name_of_file)
            delete_name = name_of_file
            name_of_file = file_name
            wf.close()
            os.remove(filename)
            print('Written to file: {}'.format(filename))
            print('Returning to listening')
        except:
            pass
            

a = SoundRecorder()

a.listenForSound()

