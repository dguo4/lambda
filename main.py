import uuid

from fastapi import FastAPI, HTTPException
from mangum import Mangum
import boto3
import uvicorn
import os
from transaction import transaction

app = FastAPI()
handler = Mangum(app)

if __name__ == "__main__":
    os.environ['TRANSACTIONS_TABLE_NAME'] = 'invest_transactions'

@app.get("/")
async def my_app():
    return {"message": "Welcome to my investment app!"}

@app.get("/test1")
async def my_test():
    return {"message": "Test function is working!"}

@app.get("/all_transactions")
async def get_all_transactions():
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['TRANSACTIONS_TABLE_NAME']
    table = dynamodb.Table(table_name)
    response = table.scan()
    data = response['Items']

    return data

@app.post("/add_transaction")
async def add_single_transaction(item: transaction):
    try:
        transaction_id = str(uuid.uuid4())
        new_item = {
            "transaction_id": {"S": transaction_id},
            "account": {"S": item.account},
            "assetGroup": {"S": item.assetGroup},
            "assetType": {"S": item.assetType},
            "date": {"S": item.date},
            "price": {"N": str(item.price)},
            "quantity": {"N": str(item.quantity)},
            "ticker": {"S": item.ticker},
            "type": {"S": item.type}
        }
        dynamodb = boto3.client('dynamodb')
        response = dynamodb.put_item(
            TableName = os.environ['TRANSACTIONS_TABLE_NAME'],
            Item = new_item
        )

        return {"message": "Item added successfully", "item": new_item}

    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail="Failed to add item to DynamoDB")


