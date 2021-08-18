# Crypto Mining

### Project Overview
* Track earnings from bitcoin mining 
* Ingest data in python
* Push to a local or remote mySQL db
* Build dashboards in Google Data Studio

### Implementation
#### API Data Ingestion
* Pull data from the f2pool.com mining pool, to get earnings data for user account/s
* Pull data from CoinMarketCap to get the price of BTC:USD, to also understand earnings in $
* Pull data from blockcypher.com to get the balance of the btc wallet earning are paid into

#### Database / AWS Hosting
* Python files have an option to store data on a local db, or on AWS RDS
* For the Cloud solution, Python scripts are loaded on an AWS EC2 instance, running once per day via cron to push the data into an RDS instance

#### Reporting
* Connect the RDS db to Google Data Studio for a robust, free reporting tool
* Report is emailed daily

### Future Updates
* Use AWS Lambda instead of EC2 to run the python scripts at lower cost
* Error handling
