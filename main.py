from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

# http://127.0.0.1:8000/docs#/default/hello__get
@app.get("/")
async def hello():
    return {'message': 'Hello, this is Datong'}