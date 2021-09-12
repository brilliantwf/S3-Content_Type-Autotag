import json
import urllib.parse
import boto3
import magic

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        #print (event)
        response = s3.get_object(Bucket=bucket, Key=key)
        body_buffer=response['Body'].read(2048)
        file_mime = magic.from_buffer(body_buffer,mime=True)
        s3.copy_object(Bucket = bucket, Key = key, CopySource = bucket + '/' + key, ContentType = file_mime, MetadataDirective='REPLACE')
        return file_mime
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

