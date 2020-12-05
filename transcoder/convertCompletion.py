import json
import urllib3
import os


def lambda_handler(event, context):
    # print(event)
    videoID = os.path.splitext(event['detail']['userMetadata']['videoID'])[0]
    print(videoID)
    url = 'https://greloupis-backend.herokuapp.com/video/aws'
    # url = 'https://www.baidu.com'
    body = {"video_id": videoID,
            "aws_auth_key": "bf9e5788a7f59072e26712bdfacdfd30c0941d836e9340de9503ca579aa765716ae9521ae429d76876b818b00c34096582ac4c7784eaf2c1febdafd667134101"}
    headers = {'content-type': "application/json",
               'Authorization': 'Bearer bf9e5788a7f59072e26712bdfacdfd30c0941d836e9340de9503ca579aa765716ae9521ae429d76876b818b00c34096582ac4c7784eaf2c1febdafd667134101'}
    http = urllib3.PoolManager()

    response = http.request('POST',
                            url,
                            body=json.dumps(body),
                            headers=headers,
                            retries=False)
    print(response.data)
    return {
        'statusCode': 200,
        'body': response.data
    }
