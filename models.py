from pydantic import BaseModel

class transaction(BaseModel):
    account: str
    assetGroup: str
    assetType: str
    date: str
    price: float
    quantity: float
    ticker: str
    type: str


class position(BaseModel):
     ticker: str
     price: float
     quantity: float
     assetGroup: str
     assetType: str
     date: str