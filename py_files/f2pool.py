# -*- coding: utf-8 -*-
#### THIS SCRIPT PULLS ACCOUNT DATA FROM THE F2POOL API FOR BITCOIN EARNINGS
#### IT THEN ADDS MINOR TRANSFORMATIONS, AND INSERTS TO A LOCAL OR CLOUD DATABASE
#### API doc # https://www.f2pool.com/developer/api?lang=en_US

import json
import requests
import pandas as pd
import csv
from datetime import date, datetime as dt, timedelta as td
import sqlalchemy
from dotenv import load_dotenv
import os

load_dotenv()
account1 = os.environ.get("f2pool_account1") 
account2 = os.environ.get("f2pool_account2") 
localuser = os.environ.get("localdb_user") 
localpass = os.environ.get("localdb_pass")
# if pushing to cloud db instead: 
# rdsuser = os.environ.get("rdsdb_user") # rdspass = os.environ.get("rdsdb_pass") # rdsdb = os.environ.get("rdsdb")

url = "https://api.f2pool.com/bitcoin/anikir?multi_account=achaudhrymb&multi_account=anikir"
                                
response = requests.get(url).json()

def db_insert(account):

    parse_json = {}

    for i in response.items():
        for key,pair in response[account].items():
            parse_json[key] = pair

    df = pd.DataFrame([parse_json])

    df.insert(0,'account',account) # add account column
    df.insert(0,'date',date.today() - td(days=1)) # add date column
    df.drop(['hashrate_history','hashrate_history_stale','payout_history','payout_history_fee','last','hashes_last_day','ori_hashes_last_day','ori_value_last_day','user_payout','value_change','value_today','value_last_day','workers'], axis=1, inplace=True)
    # df.to_csv('newtest.csv')

    ### DB INSERT ###
    engine_insert = sqlalchemy.create_engine(f'mysql+pymysql://{localuser}:{localpass}@127.0.0.1:3306/btc')
    # aws_insert = sqlalchemy.create_engine(f'mysql+pymysql://{rdsuser}:{rdspass}@{rdsdb}:3306/btc') # if pushing to AWS db instead
    df.to_sql('trash', engine_insert, if_exists='append', index=False)

db_insert(account1)
db_insert(account2)
