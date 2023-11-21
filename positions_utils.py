import boto3
from boto3.dynamodb.conditions import Attr
import uuid
import os

import pandas as pd
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
    transactions_df = transactions_df.loc[:, ['date', 'ticker', 'price', 'quantity', 'assetGroup', 'assetType']]
    positions_list = []
    for ticker in transactions_df['ticker'].unique().tolist():
        transactions_dff = transactions_df.loc[transactions_df['ticker'] == ticker, :]
        position_record = {
            'ticker': ticker,
            'assetGroup': transactions_dff['assetGroup'].unique().tolist()[0],
            'assetType': transactions_dff['assetType'].unique().tolist()[0],
            # we are using weighted average price
            'price': (transactions_dff['price'] * transactions_dff['quantity']).sum() / transactions_dff['quantity'].sum(),
            'quantity': transactions_dff['quantity'].sum()
        }
        positions_list.append(position_record)

    return pd.DataFrame(positions_list)

def delete_positions_by_date(date):
    # get all positions (before adding single transaction)
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['POSITIONS_TABLE_NAME']
    table = dynamodb.Table(table_name)

    # Step 1: Scan or Query to Identify Records
    response = table.scan(
        FilterExpression=Attr('date').eq(date)
    )

    # Extract the items to be deleted
    items_to_delete = response.get('Items', [])

    # Step 2: BatchWrite to Delete Identified Records
    with table.batch_writer() as batch:
        for item in items_to_delete:
            batch.delete_item(
                Key={
                    'position_id': item['position_id']
                }
            )

    return None
