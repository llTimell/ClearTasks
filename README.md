# ClearTasks
CNG 495 Term Project -  ClearTasks Task Management System - 2550911 - 2487080

Repository Structure:
The ClearTasks/ folder is the root directory of the project -> it has the following:
1- Client folder, the React frontend implementation. 
    1-a. public folder-> just holds static files
    2-b. src folder-> contains the core application codes:
       - componenets: for various UI components - Has the frontend code files for the login, registeration, adminDashboard, and userDashboard.
       - services/api.js: API service for backend integration
       - App.js: main entry point
      

2- server folder contains the backend code written in FastAPI -> it has the following:
  2-a. .env: stores the AWS credentials and other configuration details. "Hidden from the repository for security reasons"
  2-b. app folder:
    - main.py: The starting point for the FastAPI application - here we will define the routes.
    - auth.py: Handles authentication - integrating with AWS Cognito for user management.
    - tasks.py: Manages task-related functionality, such as task creation, updates, and tracking.
    - config.py: Stores configuration details, including AWS settings for services like S3 and SNS. The requirements.txt file lists all the necessary Python dependencies required for the backend - will use .env.


3- docs folder contains documentation --> which has the proposal + progress report +  final report.
