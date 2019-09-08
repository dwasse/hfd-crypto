This is a Python library for connecting with high frequency market data endpoints and storing/acessing data with postgresql. 

Data is stored both in raw message format for replay purposes and is also indexed by field for more efficient historical analysis.

##Requirements

You will need to install `postgresql` and the pip package `psycopg2`.

On ubuntu:
```
sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev
pip3 install psycopg2
service postgresql start
```
Then, you will need to create the hfd database:
```
sudo -u postgres -i
psql
CREATE DATABASE hfd;
\q
```
Run dataManager.py to start the data processing. Set configurations in `config.py`.
