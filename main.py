from fastapi import FastAPI, HTTPException
from mangum import Mangum
import boto3
import uvicorn

app = FastAPI()
handler = Mangum(app)

@app.get("/")
async def my_app():
    return {"message": "Welcome to my investment app!"}

@app.get("/test1")
async def my_test():
    return {"message": "Test function is working!"}

@app.get("/all_transactions")
async def get_all_transactions():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('invest_transactions')
    response = table.scan()
    data = response['Items']

    return data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

