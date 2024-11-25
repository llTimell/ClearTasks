from fastapi import APIRouter
import boto3
from pydantic import BaseModel
from config import AWS_S3_BUCKET_NAME, AWS_SNS_TOPIC_ARN, AWS_REGION

tasks_router = APIRouter()

s3_client = boto3.client('s3', region_name= AWS_REGION) #cloud storage s3
sns_client = boto3.client('sns', region_name= AWS_REGION) #notification service sns


#define the class/ table struct for the task
class Task(BaseModel):
    title: str
    description: str
    deadline: str
    assigned_to : str


#creating the task router and utalizing the sns and s3 cloud services
@tasks_router.post("/create")
def create_task(task: Task):
    #upload task to s3
    s3_client.put_object(
        Bucket = AWS_S3_BUCKET_NAME,
        key=f"tasks/{task.title}.json",
        Body = task.json()
    )


#Now sns cloud service should send notification
    sns_client.publish(
    TopicArn= AWS_SNS_TOPIC_ARN,
    Message = f"new task created: {task.title}",
    Subject = "new Task Notification"
)


    return {"task created and notification sent successfully"}