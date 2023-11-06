# lambda

## How to create AWS Lambda zip file locally?
using below command to run the project
```powershell
uvicorn main:app --reload
```

Using below command to create requirements.txt file.
```powershell
pip freeze > requirements.txt
```

### Windows：
Below commands are needed to create the zip file for Lambda:

```powershell 
pip3 install -t dependencies -r requirements.txt 
```

```powershell 
Compress-Archive -Path .\dependencies\* -DestinationPath .\aws_lambda_artifact.zip 
```

```powershell 
Compress-Archive -Path  .\main.py  -Update .\aws_lambda_artifact.zip 
```

### Unix:
Below commands are needed to create the zip file for Lambda:

```bash 
pip3 install -t dependencies -r requirements.txt 
```

```bash
(cd dependencies; zip ../aws_lambda_artifact.zip -r .)
```

```bash
zip aws_lambda_artifact.zip -u main.py
```

## Endpoint Summary
Two sections: 

1. Transactions:
    
    /all_transactions: pull all transactions
    
    /add_transaction: add new transaction. Please note, adding new transaction will automically add a new position with transaction date

2. Positions:

    /all_positions: pull all positions