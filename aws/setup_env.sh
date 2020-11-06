#!/bin/bash

curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
unzip awscli-bundle.zip
sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws
python -m pip install boto3

echo "AWS Version" 
aws --version 

mkdir ~/.aws

cp config ~/.aws
cp credentials ~/.aws
