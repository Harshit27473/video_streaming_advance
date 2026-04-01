import json
import boto3
from secret_keys import SecretKeys
 
secret_keys = SecretKeys()
sqs_client= boto3.client("sqs", region_name=secret_keys.REGION_NAME)

def poll_sqs():
    while True: 
        response = sqs_client.receive_message(
            QueueUrl= secret_keys.AWS_SQS_VIDEO_PROCESSING,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
        )
        
        for message in response.get("Messages", []):
            message_body = json.loads(message.get("Body"))

            if (
                "Service" in message_body 
                and "Event" in message_body 
                and message_body.get("Event") == "s3:TestEvent"
             ):
                sqs_client.delete_message( 
                    QueueUrl= secret_keys.AWS_SQS_VIDEO_PROCESSING,
                    ReceiptHandle= message["ReceiptHandle"]
                    )
                continue
            if "Records" in message_body:
                s3_record = message_body["Records"][0]["s3"]
                bucket_name = s3_record["bucket"]["name"]
                s3_key = s3_record["object"]["key"]

                # spin up a docker container

poll_sqs()