import os 
import requests
import boto3
from dotenv import load_dotenv


load_dotenv("../docker_envs/aws.env")


def upload_to_s3(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name with path. If not specified, file_name is used
    """
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    if object_name is None:
        object_name = file_name

    s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
    
    s3_client.upload_file(file_name, bucket, object_name)



upload_to_s3('../data/raw_data/player_data.json', 'eredivisie-insights', 'data/raw_data/player_data/player_data.json')
upload_to_s3('../data/raw_data/team_data.json', 'eredivisie-insights', 'data/raw_data/team_data/team_data.json')