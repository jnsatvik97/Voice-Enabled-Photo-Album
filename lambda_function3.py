import json
import boto3
import base64
import uuid
import urllib
import time

BUCKET_URL = 'https://audio-bucket-kp2844.s3.amazonaws.com/'
TRANSCRIBE = boto3.client('transcribe')

def lambda_handler(event, context):
    file_name = event['file_name']
    job_name = file_name.split('.')[0]
    job_uri = '{0}{1}'.format(BUCKET_URL, file_name)
    new_job = False
    try:
        curr_job = TRANSCRIBE.get_transcription_job(TranscriptionJobName=job_name)
    except:
        new_job = True
    if not new_job and not curr_job.get('TranscriptionJob'):
        new_job = True
    if not new_job:
        if curr_job['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            response = urllib.request.urlopen(curr_job['TranscriptionJob']['Transcript']['TranscriptFileUri'])
            data = json.loads(response.read())
            text = data['results']['transcripts'][0]['transcript']
            print(text)
            return {
                'status': curr_job['TranscriptionJob']['TranscriptionJobStatus'],
                'result': text
            }
        else:
            return {
                'status': curr_job['TranscriptionJob']['TranscriptionJobStatus']
            }
    else:
        TRANSCRIBE.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat='wav',
            LanguageCode='en-US'
        )
        status = TRANSCRIBE.get_transcription_job(TranscriptionJobName=job_name)
        return {
            'status': status['TranscriptionJob']['TranscriptionJobStatus']
        } 
