# -*- coding: utf-8 -*-
#### THIS SCRIPT PULLS THE BALANCE OF A BTC WALLET FROM BLOCKCYPHER API
#### IT THEN ADDS MINOR TRANSFORMATIONS, AND INSERTS TO A LOCAL OR CLOUD DATABASE
#### API doc https://www.blockcypher.com/dev/bitcoin/#restful-resources 

import json
import requests
import pandas as pd
import csv
from datetime import date, datetime as dt, timedelta as td
import sqlalchemy
from dotenv import load_dotenv
import os

load_dotenv()
localuser = os.environ.get("localdb_user") 
localpass = os.environ.get("localdb_pass")
# if pushing to cloud db instead: 
# rdsuser = os.environ.get("rdsdb_user") # rdspass = os.environ.get("rdsdb_pass") # rdsdb = os.environ.get("rdsdb")

url = "https://api.blockcypher.com/v1/btc/main/addrs/bc1qczh02ccjmaz52cu85s2hc9sc8yajr4evn32ley"
                                                                 
response = requests.get(url).json()

parse_json = {}

for i in response.items():
    for key,pair in response.items():
        parse_json[key] = pair

df = pd.DataFrame([parse_json])

df.insert(0,'date',date.today()) # add date column
df.drop(['txrefs','tx_url'], axis=1, inplace=True)

##### LOCAL DB ####
engine_insert = sqlalchemy.create_engine(f'mysql+pymysql://{localuser}:{localpass}@127.0.0.1:3306/btc')
# aws_insert = sqlalchemy.create_engine(f'mysql+pymysql://{rdsuser}:{rdspass}@{rdsdb}:3306/btc') # if pushing to AWS db instead

df.to_sql('btc_wallet', engine_insert, if_exists='append', index=False)