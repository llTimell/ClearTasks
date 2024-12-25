from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import boto3
import json
from app.config import S3_bucket_identifier, SNS_topic, Aws_region
import logging

tasks_router = APIRouter()
logger = logging.getLogger("uvicorn.error")

#we will need s3 to store the tasks and sns to send "assigned user" the notification
s3_client = boto3.client('s3', region_name=Aws_region)
sns_client = boto3.client('sns', region_name=Aws_region)

class Task(BaseModel):
    title: str
    description: str
    deadline: str
    assigned_to: str
    created_by: str
    priority: str  # e.g., "High", "Medium", "Low"



#helper function to get all tasks from S3 bucket
def get_all_tasks_from_s3():
    try:
        response = s3_client.list_objects_v2(Bucket=S3_bucket_identifier, Prefix="tasks/")
        tasks = []
        if "Contents" in response:
            for obj in response["Contents"]:
                task_obj = s3_client.get_object(Bucket=S3_bucket_identifier, Key=obj["Key"])
                task_content = task_obj["Body"].read().decode("utf-8")
                logger.debug(f"Task Content: {task_content}")  # log the content to inspect
                if not task_content:
                    logger.error(f"Empty task content found for object: {obj['Key']}")
                    continue  # Skip empty tasks
                task_data = json.loads(task_content)
                tasks.append(task_data)
        return tasks
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving tasks: {str(e)}")


#admin creates the tasks
@tasks_router.post("/create")
def create_task(task: Task):
    try:
        #upload task to S3
        s3_client.put_object(
            Bucket=S3_bucket_identifier,
            Key=f"tasks/{task.title}.json",
            Body=task.json(),
        )
       
        #send SNS notification
        sns_client.publish(
            TopicArn=SNS_topic,
            Message=f"New task created: {task.title}\nAssigned to: {task.assigned_to}\nDeadline: {task.deadline}",
            Subject="New Task Notification",
        )
        
        return {"message": "Task created and notification sent successfully"}
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")


#get all tasks
@tasks_router.get("/")
def get_tasks():
    try:
        # list objects in the "tasks" folder in S3
        response = s3_client.list_objects_v2(
            Bucket=S3_bucket_identifier,
            Prefix="tasks/"
        )

        # check if there are any tasks in the folder
        if "Contents" not in response:
            return {"message": "No tasks found."}

        tasks = []
        for obj in response["Contents"]:
            # get the object (task file) from S3
            task_object = s3_client.get_object(
                Bucket=S3_bucket_identifier,
                Key=obj["Key"]
            )
            # read and parse the task JSON content
            task_content = task_object["Body"].read().decode("utf-8")
            logger.debug(f"Task Content: {task_content}")  # log the content to inspect

            if not task_content:
                logger.error(f"Empty task content found for object: {obj['Key']}")
                continue  # skip empty tasks

            task_data = json.loads(task_content)
            tasks.append(task_data)

        return {"tasks": tasks}
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}")
        return {"error": f"Error fetching task  s: {str(e)}"}


@tasks_router.delete("/tasks/delete/{title}")
def delete_task(title: str):
    try:
        key = f"tasks/{title}.json"

    
        response = s3_client.list_objects_v2(Bucket=S3_bucket_identifier, Prefix=key)
        if "Contents" not in response:
            
            raise HTTPException(status_code=404, detail=f"Task '{title}' not found in S3")

        # Delete the object
        s3_client.delete_object(Bucket=S3_bucket_identifier, Key=key)
        
        return {"message": f"Task '{title}' deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")





#user updates the task status
@tasks_router.put("/tasks/update/{title}")
def update_task_status(title: str, status: str):
    try:
        key = f"tasks/{title}.json"

        task_obj = s3_client.get_object(Bucket=S3_bucket_identifier, Key=key)
        task_data = json.loads(task_obj["Body"].read().decode("utf-8"))
        task_data["status"] = status

        s3_client.put_object(Bucket=S3_bucket_identifier, Key=key, Body=json.dumps(task_data))

        return {"message": f"Task '{title}' updated to status '{status}'"}
    
    except s3_client.exceptions.NoSuchKey:
        
        raise HTTPException(status_code=404, detail=f"Task '{title}' not found.")

    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")