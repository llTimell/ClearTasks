from fastapi import APIRouter, HTTPException
import boto3 #used to interact with AWS
from pydantic import BaseModel
from config import awsCognito_ID, Aws_region


auth_router = APIRouter()

class UserLogin(BaseModel):
    username : str
    password : str

@auth_router.post("/login")
def login(user: UserLogin):
    cognito_client = boto3.client('cognito-idp', region_name= Aws_region)  #COGNITO CLOUD SERVICE CLIENT
    try: #will call the cloud service, cognito, to authenticate user
        response = cognito_client.initiate_auth(ClientId=awsCognito_ID,
                                                AuthFlow= "USER_PASSWORD_AUTH",
                                                AuthParameters = {
                                                    "USERNAME": user.username,
                                                    "PASSWORD": user.password} )
        #if auth successful return the access token
        return {"token" : response["AuthenticationResult"]["AccessToken"]}


    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

