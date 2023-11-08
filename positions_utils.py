import boto3
import uuid
import os
from fastapi import HTTPException

# os.environ['TRANSACTIONS_TABLE_NAME'] = 'invest_transactions'
# os.environ['POSITIONS_TABLE_NAME'] = 'invest_positions'

def add_position(item):
    dynamodb_client = boto3.client('dynamodb')

    try:
        position_id = str(uuid.uuid4())
        new_position_item = {
            "position_id": {"S": position_id},
            "ticker": {"S": item['ticker']},
            "price": {"N": str(item['price'])},
            "quantity": {"N": str(item['quantity'])},
            "assetGroup": {"S": item['assetGroup']},
            "assetType": {"S": item['assetType']},
            "date": {"S": item['date']}
        }
        response = dynamodb_client.put_item(
            TableName=os.environ['POSITIONS_TABLE_NAME'],
            Item=new_position_item
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

def get_all_positions():
    # get all positions (before adding single transaction)
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['POSITIONS_TABLE_NAME']
    table = dynamodb.Table(table_name)
    response = table.scan()
    data = response['Items']

    return data

def transfer_transactions_to_position(transactions_df):
    transactions_df = transactions_df.loc[:,['date', 'ticker', 'price', 'quantity', 'assetGroup', 'assetType']]
    positions_df = (transactions_df.groupby(['ticker', 'assetGroup', 'assetType']).
                    agg({'price': 'mean', 'quantity': 'sum'}).reset_index())
    return positions_df