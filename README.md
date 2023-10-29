# lambda

Using below command to create requirements.txt file.

pip freeze > requirements.txt

## Windows：
Below commands are needed to create the zip file for Lambda:

1. pip3 install -t dependencies -r requirements.txt
2. Compress-Archive -Path .\dependencies\* -DestinationPath .\aws_lambda_artifact.zip
3. Compress-Archive -Path  .\main.py  -Update .\aws_lambda_artifact.zip

## Unix:
Below commands are needed to create the zip file for Lambda:

1. pip3 install -t dependencies -r requirements.txt
2. (cd dependencies; zip ../aws_lambda_artifact.zip -r .)
3. zip aws_lambda_artifact.zip -u main.py