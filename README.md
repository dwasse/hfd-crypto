This is a Python library for connecting with high frequency market data endpoints (via websocket/FIX) and storing/acessing data with postgresql. Websocket connections auto-reconnect on close.

Data is stored both in raw message format for replay purposes and is also indexed by field for more efficient querying. 

## Requirements

You will need to install `postgresql` and the pip package `psycopg2`.

On ubuntu:
```
./setup.sh
```
Then, you will need to create the hfd database:
```
sudo -u postgres psql
> CREATE DATABASE hfd;
> CREATE USER "user" WITH ENCRYPTED PASSWORD 'password';
> \q
```
Run dataManager.py to start the data processing. Set configurations in `config.py`.

## To do

-BitMEX, Bitfinex, Kraken, FTX, BitMax, and other derivative exchange support
