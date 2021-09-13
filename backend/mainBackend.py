# from typing import Optional

from fastapi import FastAPI
import os, motor
from dotenv import load_dotenv

load_dotenv()

# Courtesy of 15-112
def readFile(path):
    with open(path, "rt", encoding='UTF-8') as f:
        return f.read()

connectionString = os.getenv('MONGODB_URL')

app = FastAPI()
credentials = eval(readFile('.users')) 
# dictionary where key is an email, value is user object

@app.get("/")
def read_root():
    return {"Hello": "World"}


class User(object):

    def __init__(self, email, **kwargs):
        self.email = email
        self.credentials = kwargs
        #{'gradescope' : password, 'autolab' : 'password', 'canvas' : 'password}
    
    def __hash__(self):
        return hash(self.email)
    
    def getCredentials(self):
        return self.credentials
    
    def getCredential(self, account):
        return self.credentials.get(account, None)
    
    def __repr__(self):
        return f'User({self.email}, {self.credentials})'


@app.get("/create-user/{email}&{gradeScopeUsername}&{gradeScopePassword}") # not secure
def createUser(email, gradescopeUsername, gradeScopePassword):
    # search for email
        # if it exists, then add to the dict
        # if not, then create a new email
    newUser = credentials.get(email, User(email, gradescopeUsername = gradescopeUsername, gradescopePassword = gradescopePassword))
    credentials[email] = newUser
    return f'New user successfully created with email {newUser.email}'


@app.get("/get-assignments/{service}-{email}")
def getGradescopeInfo(service, email):
    userCredentials = credentials.get(email, None)
    
    if userCredentials == None:
        return "No user exists with this email"
    
    servicePassword = userCredentials.getCredential(service)
    if servicePassword == None:
        return 'No user credentials exist for this service.'
    
    # call gradescope scraper with email and password
    # process info and return it
    
    
    
    
