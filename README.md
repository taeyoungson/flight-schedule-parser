# Flight Schedule Parser

`Flight Schedule Parser` is a project built with FastAPI and APScheduler to manage flight schedules. The system provides the following features:

## Features

- **OCR Data Processing and Storage**
  - Accepts OCR data via a POST request and stores it as an event in Google Calendar.

- **Flight Status Monitoring**
  - Daily checks the Google Calendar for upcoming flights and registers a monitoring job for each flight.
  - Monitors flight statuses and sends notifications to users about flight delays, including the delay duration.

- **Weather Notifications for International Flights**
  - Daily checks the Google Calendar for any upcoming flights bound for foreign countries.
  - Searches for weather information of the destination country and sends notifications to users via KakaoTalk or Discord.

## Deployment Environment

- **AWS EC2**: The system is hosted on AWS EC2.

## Technology Stack

- **FastAPI**: API server implementation
- **APScheduler**: Job scheduling for monitoring tasks
- **Google Calendar API**: Storing and retrieving flight schedules
- **KakaoTalk, Discord API**: Sending user notifications
- **AviationStack**: Flight status monitoring
- **OpenAI**: Summarize weather information, recommend clothing based on the user's flight schedule
- **Imgbb**: Image hosting for messaging services

## Examples

### Automatically register flight schedules to calendar
![image](https://github.com/user-attachments/assets/3ba22476-f4ea-4650-9378-33385ce473db)

### Flight monitoring example
![image](https://github.com/user-attachments/assets/5901cb49-b9d6-4b29-8d15-935a560100be)

### AI summarizes weather information around destination city.
![image](https://github.com/user-attachments/assets/c6df6745-c2a7-42da-bbb1-6c87bd01314d)
