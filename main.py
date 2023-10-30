from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pymongo import MongoClient

conn = MongoClient("mongodb+srv://miaHappy:6adL7Gi3VA7DNndf@cluster0.pks73ha.mongodb.net/?retryWrites=true&w=majority")

app = FastAPI()
handler = Mangum(app)

def transactionEntity(item) -> dict:
    return {
        "id": str(item['_id']),
        "date": item['date'],
        "account": item['account'],
        "ticker": item['ticker'],
        "price": item['price'],
        "quantity": item['quantity'],
        "assetGroup": item['assetGroup'],
        "assetType": item['assetType'],
        "type": item['type']
    }

def transactionsEntity(entity) -> list:
    return [transactionEntity(item) for item in entity]

@app.get("/")
async def my_app():
    return {"message": "Welcome to my investment app!"}

@app.get("/test1")
async def my_test():
    return {"message": "Test function is working!"}

@app.get("/all_transactions")
async def get_all_transactions():
    return transactionsEntity(list(conn.investment.transactions.find()))