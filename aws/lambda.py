import json
import boto3
import os

glue = boto3.client('glue')

CRAWLER_NAME = os.environ['CRAWLER_NAME']  # Set in Lambda environment variable

def lambda_handler(event, context):
    try:
        # Extract bucket and object key
        print("AD is testing Lambda Function")
        print("Event created: ")
        print(event)
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
    
        print(f"New file detected:")
        print(f"Bucket = {bucket}")
        print(f"Key = {key}")


        print(f"ABout to run Glue Crawler : {CRAWLER_NAME}")

        # Optional: Only trigger for specific file types
        if not key.endswith(('.csv')):
            print("File type not supported. Skipping crawler trigger.")
            return

        # Check crawler state (avoid concurrent run error)
        crawler_info = glue.get_crawler(Name=CRAWLER_NAME)
        crawler_state = crawler_info['Crawler']['State']

        print(f"Current crawler state: {crawler_state}")

        if crawler_state == 'READY':
            response = glue.start_crawler(Name=CRAWLER_NAME)
            print(f"Crawler {CRAWLER_NAME} started successfully.")
        else:
            print(f"Crawler is currently in state: {crawler_state}. Skipping trigger.")

        return {
            'statusCode': 200,
            'body': json.dumps('Crawler trigger process completed')
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        raise e
