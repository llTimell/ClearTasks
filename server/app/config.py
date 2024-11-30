import os
from dotenv import load_dotenv



load_dotenv()

#Necesary AWS config
AWS_Key_id = os.getenv("AWS_ACCESS_KEY_ID")
AWS_secret_Access = os.getenv("AWS_SECRET_ACCESS_KEY")
Aws_region = os.getenv("AWS_REGION")


#Cognito Config
awsCognito_ID = os.getenv("AWS_COGNITO_CLIENT_ID")
awsCognito_UserPool = os.getenv("AWS_COGNITO_USER_POOL_ID")

# s3 Database Config
S3_bucket_identifier = os.getenv("AWS_S3_BUCKET_NAME")

# SNS Config

SNS_topic = os.getenv("AWS_SNS_TOPIC_ARN")
#End of My part