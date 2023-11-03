import boto3
import uuid
import os
from models import transaction
from fastapi import HTTPException

# os.environ['TRANSACTIONS_TABLE_NAME'] = 'invest_transactions'
# os.environ['POSITIONS_TABLE_NAME'] = 'invest_positions'

def add_new_transaction(item: transaction):
    dynamodb_client = boto3.client('dynamodb')

    # add one new record to transactions table
    try:
        transaction_id = str(uuid.uuid4())
        new_transaction_item = {
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

        response = dynamodb_client.put_item(
            TableName=os.environ['TRANSACTIONS_TABLE_NAME'],
            Item=new_transaction_item
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

def get_all_transaction():
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['TRANSACTIONS_TABLE_NAME']
    table = dynamodb.Table(table_name)
    response = table.scan()
    data = response['Items']
    return data