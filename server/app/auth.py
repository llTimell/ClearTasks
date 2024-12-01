from fastapi import APIRouter, HTTPException
import boto3 #used to interact with AWS
from pydantic import BaseModel, EmailStr
from app.config import awsCognito_ID, Aws_region


auth_router = APIRouter()


class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    username : str
    password : str




@auth_router.post("/register")
def register(user: UserRegister):
    cognito_client = boto3.client('cognito-idp', region_name=Aws_region)
    try:
        cognito_client.sign_up(
            ClientId=awsCognito_ID,
            Username=user.username,
            Password=user.password,
            UserAttributes=[
                {"Name": "email", "Value": user.email},
            ],
        )
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Registration failed")
    
    

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

