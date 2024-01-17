from prefect_aws import AwsCredentials
from prefect_aws.s3 import S3Bucket
import os 
from prefect import flow, task
import requests

# from dotenv import load_dotenv


# aws_credentials = AwsCredentials(
#     aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
#     aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
#     )



@task(name="Get PL Data",log_prints=True)
def get_team_info():
    uri = 'http://api.football-data.org/v4/competitions/PL'
    AUTH_TOKEN = os.getenv('AUTH_TOKEN')
    print(type(AUTH_TOKEN))
    headers = { 'X-Auth-Token': AUTH_TOKEN}
    response = requests.get(uri, headers=headers)
    print(response.json())

@flow(name="get API data")
def get_data():
    get_team_info()


if __name__ == "__main__":
    get_data()