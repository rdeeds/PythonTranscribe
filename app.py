import boto3
import botocore, time
from tools import randalphnum
from filesstuff import create_file
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION, S3BUCKETWHERESOUNDFILEIS, S3BUCKETWHEREJSONFILEGOES



s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


def create_bucket(bname):
    response = s3.create_bucket(
        Bucket=bname)
    return response


def delete_bucket(bname):
    response = s3.delete_bucket(
        Bucket=bname
    )
    return response


def list_buckets():
    # Call S3 to list current buckets
    response = s3.list_buckets()
    # Get a list of all bucket names from the response
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    # Return the bucket list
    return buckets


def upload_s3(filename, targetfilename, bucket=S3BUCKETWHERESOUNDFILEIS):
    a = s3.upload_file(filename, bucket, targetfilename)
    return 'https://s3.amazonaws.com/{}/{}'.format(bucket, targetfilename)


def start_trans(fileurl, jobname):
    client = boto3.client('transcribe', aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)
    response = client.start_transcription_job(
        TranscriptionJobName=jobname,
        LanguageCode='en-US',
        MediaFormat='wav',
        Media={
            'MediaFileUri': fileurl
        },
        OutputBucketName=S3BUCKETWHEREJSONFILEGOES,
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 8
        }
    )

    print('RESPONSE:\n', response)


def get_file_s3(bucket, filename):   #goes and gets
    s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    gotit = 0

    while gotit == 0:  #going to S3 and seeing if the file exists
        try:
            s3.Bucket(bucket).download_file(filename, './jsonfilesfromtranscribe/'+filename)
            gotit = 1
            print('WORKS!!!!')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
                gotit = 0
            else:
                gotit = 0

                raise
            time.sleep(5)


def trans_step_1(localfilename):
    awsfilename = randalphnum(10)
    url = upload_s3(localfilename, awsfilename + '.wav')  # moves sound file to s3 from local
    start_trans(url, awsfilename)  # starts the transcription
    get_file_s3(S3BUCKETWHEREJSONFILEGOES, awsfilename + '.json')  # goes and gets the json file
    create_file(awsfilename + '.json', awsfilename)
    #rem_file(localfilename) #uncomment out to remove the json files





trans_step_1('./test_audio/DigitalBroker10.wav')
