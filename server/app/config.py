import os
from dotenv import load_dotenv



load_dotenv()

#Necesary AWS config
AWS_Key_id = os.getenv("AKIAVFIWIPKO7SCJSX6Z")
AWS_secret_Access = os.getenv("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")
Aws_region = os.getenv("eu-north-1")


#Cognito Config
awsCognito_ID = os.getenv("6imqlel587fibau1hjo4dgshh9")
awsCognito_UserPool = os.getenv("eu-north-1_hZhRJfSrm")

# s3 Database Config
S3_bucket_identifier = os.getenv("cleartasks-bucket")

# SNS Config

SNS_topic = os.getenv("arn:aws:sns:eu-north-1:354918365853:cleartasks-notifications")
