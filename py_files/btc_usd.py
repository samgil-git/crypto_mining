#### THIS SCRIPT PULLS THE PRICE OF BITCOIN FROM COINMARKETCAP API
#### IT THEN ADDS MINOR TRANSFORMATIONS, AND INSERTS TO A LOCAL OR CLOUD DATABASE
#### API doc https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyQuotesLatest

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
from datetime import date, datetime as dt, timedelta as td
import sqlalchemy
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("coinmarketcap")
localuser = os.environ.get("localdb_user") 
localpass = os.environ.get("localdb_pass") 
# if pushing to cloud db instead: 
# rdsuser = os.environ.get("rdsdb_user") # rdspass = os.environ.get("rdsdb_pass") # rdsdb = os.environ.get("rdsdb")

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  #'start':'1', # if iterating through multiple coins
  #'limit':'5000',
  'id':'1', # only care about BTC -- safer to reference the ID
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api_key,
}

session = Session()
session.headers.update(headers)

response = session.get(url, params=parameters)
data = response.json()
#print(data.keys())  # status, data

parse_json = {}

for i in data.items():
    for key,pair in data['data']['1'].items():
        parse_json[key] = pair

df = pd.DataFrame([parse_json])
df.insert(0,'date',date.today()) # add date inserted column
df.insert(1,'price_usd',df['quote'][0]['USD']['price']) # add the nested usd price
df.drop(['tags','date_added','platform','quote'], axis=1, inplace=True) # remove unneeded

##### LOCAL DB ####
engine_insert = sqlalchemy.create_engine(f'mysql+pymysql://{localuser}:{localpass}@127.0.0.1:3306/btc')
df.to_sql('btc_price', engine_insert, if_exists='append', index=False)

##### AWS RDS ####
# aws_insert = sqlalchemy.create_engine(f'mysql+pymysql://{rdsuser}:{rdspass}@{rdsdb}:3306/btc') # if pushing to AWS db instead
# df.to_sql('btc_price', aws_insert, if_exists='append', index=False)