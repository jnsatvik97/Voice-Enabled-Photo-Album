import json
import base64
import boto3

S3 = boto3.client('s3')

def lambda_handler(event, context):
    key = str(event['file_name'])
    image = event['img']
    image = image[image.find(",")+1:]
    dec = base64.b64decode(image + "===")
    # img_base64 = event['img']
    print(dec)
    # dec = base64.b64decode(img_base64)
    # print(dec)
    rs = S3.put_object(
        Bucket='photo-bucket-rn2490',
        Key=key,
        ContentType='image/jpeg',
        Body=dec,
        ACL='public-read'
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
