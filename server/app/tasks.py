from fastapi import APIRouter
import boto3
from pydantic import BaseModel
from config import S3_bucket_identifier, SNS_topic, Aws_region

tasks_router = APIRouter()

s3_client = boto3.client('s3', region_name= Aws_region) #cloud storage s3
sns_client = boto3.client('sns', region_name= Aws_region) #notification service sns


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
        Bucket = S3_bucket_identifier,
        key=f"tasks/{task.title}.json",
        Body = task.json()
    )


#Now sns cloud service should send notification
    sns_client.publish(
    TopicArn= SNS_topic,
    Message = f"new task created: {task.title}",
    Subject = "new Task Notification"
)


    return {"task created and notification sent successfully"}