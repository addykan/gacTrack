# from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/create-user/{gradeScopeUsername}-{gradeScopePassword}") # not secure
def createUser(gradeScopeUsername, gradeScopePassword):
    return {"gsUsername": gradeScopeUsername, "gsPassword" : gradeScopePassword}