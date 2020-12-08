# Tutorial: Automatically distribute videos after uploading them to AWS S3

This tutorial introduces how to use [AWS S3](https://aws.amazon.com/s3) as a storage loaction to upload video. Then the upload will automatically trigger a [AWS MediaConvert](https://aws.amazon.com/mediaconvert/) workflow to converts the video to suitable formats for distributing, which use [AWS Cloudfront](https://aws.amazon.com/cloudfront) to help. 
When use the website [greloupis](https://greloupis-frontend.herokuapp.com/) to upload a video, it will trigger the workflow below.
1. the video will be uploaded to one existed folder in S3 bucket
2. the lambda trigger in S3 will trigger mediaconvert to convert the video to suitable formats, including an Apple HLS adaptive bitrate stream, an MP4 stream and thumbnail images. Then the outputs will be stored to another existed folder in S3 bucket
3. when the converting job finished, another lambda trigger will trigger a workflow to update the url of video in our DB
4. when access the url, cloudfront, which has been connected to S3, will help to distribute the video

## Implementation Instructions

Each of the following sections provide an implementation overview and detailed, step-by-step instructions.

## 1. Create an Amazon S3 bucket to use for uploading videos to be converted

#### Step-by-step instructions 

1. In the AWS Management Console choose **Services** then select **S3** under Storage.

2. Choose **Create Bucket**.

3. Provide a globally unique name for your bucket, here we use the name `vod-watchfolder-ovs-lxb`.

4. Select the Region you've chosen to use for this workshop from the dropdown.

5. Select **Block public access** and and uncheck the **Block all public access** checkbox.  

6. Choose **Create bucket** to create the bucket.

7. From the S3 console select the bucket you just created and go to the Overview page.

8. Select the **Permissions** tab.  

9. Next, click on **Bucket policy** and replace the default json with the following json in the **Bucket policy editor**. The json can also be seen in `transcode/bucket_strategy.json` in our project.
    ```
    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::vod-watchfolder-ovs-lxb/*"
        }
    ]
    }
    ```

10. Next, click on **CORS configruation** and replace the default configuration with the following configuration in the **CORS configuration editor**. The configuration can also be seen in `transcode/bucket_cors` in our project.
    ```
    [
        {
            "AllowedHeaders": [
                "*"
            ],
            "AllowedMethods": [
                "POST",
                "GET",
                "PUT"
            ],
            "AllowedOrigins": [
                "*"
            ],
            "ExposeHeaders": [
                "ETag"
            ]
        }
    ]

    ```
11. Click on the **Save** button

## 2. Create an Amazon S3 bucket to use for storing converted video outputs from MediaConvert

In this step, you will use the AWS console to create an S3 bucket to store video. In order to facilitate https access from anonymous sources inside and outside the amazonaws domain, such as video players on the internet, you will add the following settings to the S3 bucket:

* a bucket policy that enables public read   
* a policy for Cross Origin Resource Sharing (CORS) 

#### Step-by-step instructions 

1. In the AWS Management Console choose **Services** then select **S3** under Storage.

2. Choose **Create Bucket**.

3. Provide a globally unique name for your bucket, here we use the name `vod-xuanbinmediabucket`.

4. Select the Region you've chosen to use for this workshop from the dropdown.

5. Select **Block public access** and and uncheck the **Block all public access** checkbox.  

6. Choose **Create bucket** to create the bucket.

7. From the S3 console select the bucket you just created and go to the Overview page.

8. Select the **Permissions** tab.  

9. Next, click on **Bucket policy** and replace the default json with the following json in the **Bucket policy editor**. The json can also be seen in `transcode/bucket_strategy.json` in our project.
    ```
    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::vod-watchfolder-ovs-lxb/*"
        }
    ]
    }
    ```

10. Next, click on **CORS configruation** and replace the default configuration with the following configuration in the **CORS configuration editor**. The configuration can also be seen in `transcode/bucket_cors` in our project.
    ```
    [
        {
            "AllowedHeaders": [
                "*"
            ],
            "AllowedMethods": [
                "POST",
                "GET",
                "PUT"
            ],
            "AllowedOrigins": [
                "*"
            ],
            "ExposeHeaders": [
                "ETag"
            ]
        }
    ]

    ```
11. Click on the **Save** button

## 3. Create an IAM Role to Pass to MediaConvert

#### Background

MediaConvert will will need to be granted permissions to read and write files from your S3 buckets and generate CloudWatch events as it processes videos.  MediaConvert is granted the permissions it needs by assuming a role that is passed to it along with trancoding jobs. 

Every Lambda function has an IAM role associated with it. This role defines what other AWS services the function is allowed to interact with. For the purposes of this workshop, you'll need to create an IAM role that grants your Lambda function permission to interact with the MediaConvert service.  

#### Step-by-step instructions 

1. From the AWS Management Console, click on **Services** and then select **IAM** in the Security, Identity & Compliance section.

2. Select **Roles** in the left navigation bar and then choose **Create role**.

3. Select **AWS Service** and **MediaConvert** for the role type, choose **MediaConvert** as the use case, then click on the **Next:Permissions** button.

4. Choose **Next:Tags**.

5. Choose **Next:Review**.

6. Enter `MediaConvertRole` for the **Role name**.

7. Choose **Create role**.

8. Type `MediaConvertRole` into the filter box on the Roles page and choose the role you just created. 

9. Save the ARN for use later

10. From the AWS Management Console, click on **Services** and then select **IAM** in the Security, Identity & Compliance section.

11. Select **Roles** in the left navigation bar and then choose **Create role**.

12. Select **AWS Service** and **Lambda** for the role type, then click on the **Next:Permissions** button.

13. Begin typing `AWSLambdaBasicExecutionRole` in the **Filter** text box and check the box next to that role.

15. Choose **Next:Tags**.

16. Choose **Next:Review**.

17. Enter `VODLambdaRole` for the **Role name**.

16. Choose **Create role**.

18. Type `VODLambdaRole` into the filter box on the Roles page and choose the role you just created.

19. On the Permissions tab, expand the **Add Inline Policies** section and choose the **JSON** tab.

20. Copy and paste the following JSON in the **Policy Document Box**.  You will need to edit this policy in the next step to fill in the resources for your application. The configuration can also be seen in `transcode/iam_policy` in our project.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*",
            "Effect": "Allow",
            "Sid": "Logging"
        },
        {
            "Action": [
                "iam:PassRole"
            ],
            "Resource": [
                "ARNforMediaConvertRole"
            ],
            "Effect": "Allow",
            "Sid": "PassRole"
        },
        {
            "Action": [
                "mediaconvert:*"
            ],
            "Resource": [
                "*"
            ],
            "Effect": "Allow",
            "Sid": "MediaConvertService"
        },
        {
            "Action": [
                "s3:*"
            ],
            "Resource": [
                "*"
            ],
            "Effect": "Allow",
            "Sid": "S3Service"
        }
    ]
}
```
1. Replace the ARNforMediaConvertRole tag in the policy with the ARN for the VODMMediaConvertRole you created earlier.

2. Click on the **Review Policy** button.

3. Enter `VODLambdaPolicy` in the **Policy Name** box.

4. Click on the **Create Policy** button.

## 4. Create a lambda Function for converting videos

#### Background

AWS Lambda will run your code in response to events such as a putObject into S3 or an HTTP request. In this step you'll build the core function that will process videos using the MediaConvert python SDK. The lambda function will respond to putObject events in your S3 WatchFolder bucket.  Whenever a video file is added to the /inputs folder, the lambda will start a MediaConvert job.

#### Step-by-step instructions 

1. Choose **Services** then select **Lambda** in the Compute section.

2. Choose **Create a Lambda function**.

3. Choose the **Author from scratch** button.

4. On the **Author from Scratch** panel, enter `VODLambdaConvert` in the **Name** field.

5. Select **Python 3.8** for the **Runtime**.

6. Choose **Use and existing role** from the Role dropdown.

7. Select `VODLambdaRole` from the **Existing Role** dropdown.

8. Click on **Create function**.

9. On the Configuration tab of the VODLambdaConvert page, in the  **function code** panel:  

    1. Create a file for lambda function, which can be seen as `convert.py` in our project.
    2. Create a file for mediaconvert job, which can be seen as `job.json` in our project.


10. On the **Environment Variables** panel of the VODLambdaConvert page, enter the following keys and values:

    1. DestinationBucket = `vod-watchfolder-ovs-lxb` (or whatever you named your S3 MediaBucket bucket)
    1. MediaConvertRole = arn:aws:iam::ACCOUNT NUMBER:role/MediaConvertRole (or whatever you named your role to pass to MediaConvert)
    2. Application = VOD

11. On the  **Basic Settings** panel, enter the following: 
    
    1. Timeout = 2 min

12. Scroll back to the top of the page and click on the **Save** button.

## 5. Create a S3 Event Trigger for your Convert lambda

#### Background

In the previous step, you built a lambda function that will convert a video in response to an S3 PutItem event.  Now it's time to hook up the Lambda trigger to the watchfolder S3 bucket.  We want to run the lambda whenever someone uploads a new object to the S3 bucket, so we will use PutItem operations as our Lambda trigger.

#### Step-by-step instructions

1. In the **Configuration->Designer** panel of the VODLambdaConvert function:
    1. Click on **S3* under **Add triggers**

2. Scroll down to the **Configure triggers** panel:
  
    1. Select `vod-watchfolder-ovs-lxb` or the name you used for the watchfolder bucket you created earlier in this module for the **Bucket**.
    2. Select **All object create events** for the **Event type**.
    3. Leave the rest of the settings as the default and click the **Add** button.


## 6. Create a lambda Event Trigger for updating our url when mediaconvert job finished

#### Background

The lambda above will submit a job to MediaConvert, but it won't wait for the job to complete. In this step, we'll use CloudWatch events to automatically monitor MediaConvert jobs and update the video url in our DB when they finish.

#### Step-by-step instructions

1. Choose **Services** then select **Lambda** in the Compute section.

2. Choose **Events** then click **Rule** tab.

3. Choose **Create rule**

4. Select **Event Pattern** in **Event Source**

5. In **Service Name**, select **MediaConvert**

6. In **Event Pattern Preview**, click **Edit**

7. Enter the following JSON in the box. The configuration can also be seen in `transcode/cloudwatch_event.json` in our project.

    ```
    {
    "source": [
        "aws.mediaconvert"
    ],
    "detail-type": [
        "MediaConvert Job State Change"
    ],
    "detail": {
        "status": [
        "COMPLETE"
        ]
    }
    }
    ```
8. Click **Save**.

## 7. use Cloudfront to distribute the video

#### Background

Amazon CloudFront is a web service that speeds up distribution of your static and dynamic web content, such as .html, .css, .js, and image files, to your users. CloudFront delivers your content through a worldwide network of data centers called edge locations. 

#### Step-by-step instructions

1. Choose **Services** then select **Cloudfront** in the Compute section.

2. Choose **Distribution** in the panel on the left.

3. Choose **Create Distribution**

4. Choose **Web** and click **Get Started** for delivery method

5. Choose the output bucket we named `vod-xuanbinmediabucket` in the **Origin Domain Name** of **Origin Settings**

6. Select **Redirect HTTP to HTTPS** in **Viewer Protocol Policy** of **Default Cache Behavior Settings**

7. Leave the rest of the settings as the default and click the **Create Distribution** button.


