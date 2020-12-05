import json
import urllib3
import os


def lambda_handler(event, context):
    # print(event)
    videoID = os.path.splitext(event['detail']['userMetadata']['videoID'])[0]
    print(videoID)
    AWS_AUTH_KEY = os.environ.get('AWS_AUTH_KEY')
    print(AWS_AUTH_KEY)
    url = 'https://greloupis-backend.herokuapp.com/video/aws'
    body = {"video_id": videoID,
            "aws_auth_key": AWS_AUTH_KEY}
    http = urllib3.PoolManager()

    response = http.request('POST',
                            url,
                            body=json.dumps(body),
                            retries=False)
    print(response.data)
    return {
        'statusCode': 200,
        'body': response.data
    }
