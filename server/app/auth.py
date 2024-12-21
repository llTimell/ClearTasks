from fastapi import APIRouter, HTTPException
import boto3
from pydantic import BaseModel, EmailStr
from app.config import awsCognito_ID, Aws_region, awsCognito_AppClientSecret
import logging
import base64
import hashlib
import hmac

#for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

auth_router = APIRouter()


#classes defintions caused lots of issues bc they werent matching userpool attributes
class UserRegister(BaseModel):
    username: str 
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str


def calculate_secret_hash(username, client_id, client_secret):
    message = username + client_id
    secret_hash = hmac.new(
        key=bytes(client_secret, 'utf-8'),
        msg=bytes(message, 'utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(secret_hash).decode()




#registeration endpoint
@auth_router.post("/register")
def register(user: UserRegister):
    logger.debug(f"Received registration request for username: {user.username}, email: {user.email}")
    
    cognito_client = boto3.client('cognito-idp', region_name=Aws_region)
    
    try:
        # calculating SecretHash for the registration request
        secret_hash = calculate_secret_hash(user.username, awsCognito_ID, awsCognito_AppClientSecret)
        logger.debug(f"Calculated SecretHash: {secret_hash}")
        
        # perform the sign-up with the required attributes
        response = cognito_client.sign_up(
            ClientId=awsCognito_ID,
            SecretHash=secret_hash,
            Username=user.username,  
            Password=user.password,
            UserAttributes=[
                {"Name": "email", "Value": user.email},
            ],
        )
        
        # add the user to a group 
        cognito_client.admin_add_user_to_group(
            UserPoolId="eu-north-1_cIHd4QsIg",  #
            Username=user.username,
            GroupName="NormalUser"  # NormalUser is the deffault ---> CAN BE CHOSEN IN AWS account under Groups tab
        )

        logger.debug(f"Cognito response: {response}")
        return {"message": "user registered successfully"}
    
    except Exception as e:
        logger.error(f"error during registration: {str(e)}")
        raise HTTPException(status_code=400, detail=f"registratione failed: {str(e)}")




@auth_router.post("/login")
def login(user: UserLogin):
    try:
        cognito_client = boto3.client('cognito-idp', region_name=Aws_region)
        secret_hash = calculate_secret_hash(user.username, awsCognito_ID, awsCognito_AppClientSecret)
        
        # initiate user authentication thro cognito
        response = cognito_client.initiate_auth(
            ClientId=awsCognito_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": user.username,
                "PASSWORD": user.password,
                "SECRET_HASH": secret_hash
            }
        )
        
        # return the access token if authentication successful
        logger.debug(f"Authentication successful for user: {user.username}")
        return {
            "access_token": response["AuthenticationResult"]["AccessToken"],
            "id_token": response["AuthenticationResult"]["IdToken"],
            "refresh_token": response["AuthenticationResult"]["RefreshToken"]
        }
    
    except cognito_client.exceptions.NotAuthorizedException:
        logger.error("Invalid username or password.")
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    
    except cognito_client.exceptions.UserNotConfirmedException:
        logger.error("User account is not confirmed.")
        raise HTTPException(status_code=403, detail="User account is not confirmed.")
    
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during login.")




