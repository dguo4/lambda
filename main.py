import logging

from fastapi import FastAPI
from mangum import Mangum
import pandas as pd
import os
from models import transaction, position
import transactions_utils
import positions_utils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
handler = Mangum(app)

if __name__ == "__main__":
    logger.info("Start debug ...")
    os.environ['TRANSACTIONS_TABLE_NAME'] = 'invest_transactions'
    os.environ['POSITIONS_TABLE_NAME'] = 'invest_positions'

@app.get("/")
async def my_app():
    logger.info("Accessed the root endpoint")
    return {"message": "Welcome to my investment app!"}

@app.get("/all_transactions")
async def get_all_transactions():
    logger.info("get all transactions ... ")
    return transactions_utils.get_all_transaction()

@app.get("/all_positions")
async def get_all_positions():
    logger.info("get all positions ... ")
    return positions_utils.get_all_positions()

@app.post("/add_transaction")
async def add_single_transaction(item: transaction):
    # add new transaction to transactions table
    transactions_utils.add_new_transaction(item)

    # get all transactions
    all_transactions_data = transactions_utils.get_all_transaction()
    new_all_transactions_df = pd.DataFrame(all_transactions_data)

    # pivot transactions to position
    new_positions_df = positions_utils.transfer_transactions_to_position(new_all_transactions_df)

    # add all new positions by ticker to position table
    for t in new_positions_df['ticker'].unique().tolist():
        single_new_position_df = new_positions_df.loc[new_positions_df['ticker'] == t]
        position_item = {
            "ticker": single_new_position_df['ticker'].values[0],
            "price": single_new_position_df['price'].values[0],
            "quantity": single_new_position_df['quantity'].values[0],
            "assetGroup":single_new_position_df['assetGroup'].values[0],
            "assetType": single_new_position_df['assetType'].values[0],
            "date": item.date
        }
        positions_utils.add_position(position_item)

    return {"message": "Item added successfully"}


