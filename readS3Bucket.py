from boto3.session import Session
import boto3
import scipy.io.wavfile as sciwav
from pydub import AudioSegment
import math
import os
import shutil
from io import BytesIO
from unsilence import Unsilence


def getEvents(audio):
    step = math.floor(len(audio)/3)
    events = []
    for x in range(0, len(audio), step):
        if not x+step > len(audio):
            events.append(audio[x:x+step])
    return events

def getSamples(sound):
    samples = []
    step = 5000 # 5 seconds in milliseconds
    for x in range(0, len(sound), step):
        if not x+step > len(sound):
            samples.append(sound[x:x+step])
    return samples

def uploadDirectory(path,bucket,foldername):
        for root,dirs,files in os.walk(path):

            for file in files:
                bucket.upload_file(os.path.join(root,file),f'{foldername}/{file}')
                #s3C.upload_file(os.path.join(root,file),bucketname,file)

def createFolder(name):
    try: 
        os.mkdir(name) 
    except OSError as error: 
        shutil.rmtree(name)
        os.mkdir(name) 

ACCESS_KEY = ""
SECRET_KEY = ""

bucket_name = 'audiopipelinetestbucket'

events_bucket_name = 'audiopipelineeventstest'

session = Session(aws_access_key_id=ACCESS_KEY,
              aws_secret_access_key=SECRET_KEY)

s3 = session.resource('s3')

files_bucket = s3.Bucket(bucket_name)

events_bucket = s3.Bucket(events_bucket_name)


#u = Unsilence(filepath)
#u.detect_silence()
#u.render_media(output_filepath, silent_speed=100, audio_only=True)

createFolder(f'./{bucket_name}_temp')
createFolder(f'./{bucket_name}_silence')
createFolder(f'./{bucket_name}')
for s3_file in files_bucket.objects.all():
    print(s3_file.key)
    object = s3.Object(bucket_name, s3_file.key)
    result = object.get()['Body'].read()
    wrapper = BytesIO(result)
    sound = AudioSegment.from_wav(wrapper)
    sound = sound.set_channels(1)
    sound.export(f'./{bucket_name}_temp/{s3_file.key}', format="wav")
    u = Unsilence(f'./{bucket_name}_temp/{s3_file.key}')
    u.detect_silence()
    u.render_media(f'./{bucket_name}_silence/silence_{s3_file.key}', silent_speed=100, audio_only=True)
    sound = AudioSegment.from_wav(f'./{bucket_name}_silence/silence_{s3_file.key}')
    #events = getEvents(sound)
    samples = getSamples(sound)
    for i in range(0,len(samples)):
        samples[i].export(f'./{bucket_name}/{i}_{s3_file.key}', format="wav")
    #wav_file = sciwav.read(wrapper)
    #print(type(wav_file))
uploadDirectory(f'./{bucket_name}',events_bucket,bucket_name)
shutil.rmtree(f'./{bucket_name}_temp')
shutil.rmtree(f'./{bucket_name}_silence')
shutil.rmtree(f'./{bucket_name}')
