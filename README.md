# API Amazon Clone
> An amazon clone API made with django framework and django API rest framework with Unit & Integration testing.  

## Table of contents
* [Technologies](#technologies)
* [Setup](#Setup)
* [Postman](#Postman)
* [Features](#features)
* [User Credentials](#user-credentials)
* [TODO](#todo)

## Technologies
* Python 3.9  
* Django 2.2.19  
* Pytest 6.2.4  
* DRF 3.12.4  
* DRF-Simple JWT 4.7.2  

## Setup
The first thing to do is to clone the repository:  
`$ git clone https://github.com/OmarFateh/api-Amazon-Clone.git`    
Setup project environment with virtualenv and pip.  
`$ virtualenv project-env`  
Activate the virtual environment  
`$ source project-env/Scripts/activate`  
Install all dependencies  
`$ pip install -r requirements.txt`  
Run the server  
`py manage.py runserver`  

## Postman
- via workspace: https://go.postman.co/workspace/My-Workspace~b19b37d5-b4db-4853-858b-40297e82123b/collection/12238256-46356be9-b980-4b3b-adc0-dabbeb9cb36a  
- via JSON link: https://www.getpostman.com/collections/fc9743c62816b67a2c2b  
## Features
* Authentication: Registration, login(with email), logout, activate account, change and reset password.  
* Multiple user types (Admin - Merchant - Customer)  
* Multiple payments and addresses for each customer  
* Product variants with multiple attributes  

## User Credentials
* Admin: - email--> omarfateh1@gmail.com  - password-->admin1600  
* Merchant: - email--> omarfateh@gmail.com  - password-->admin1600  
* Customer: - email--> omarfateh0@gmail.com  - password-->admin1600

## TODO
* Implement Live Customer Support Chat.
* Implement Recommendation System.