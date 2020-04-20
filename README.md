# mysql-data-etl-example
api generated database proof of concept

# Database design choice

This database utilizes 3 tables in order to provide relevant business information
in an accessible, updatable, relevant format with minimal duplication of data

The three tables are as follows:

businesses
```
id (integer)
name (string)
rating (float)
wiki_url (string)
parking (boolean)
open_weekends (boolean)
location_id (integer) [foreign key pointing to locations table]
most_recent_review_id (integer) [foreign key pointing to users table]
created_at (timestamp)
```

locations
[this table was created because there are multiple businesses in single locations
 thus a separate table with relationship to businesses prevents data duplication]
```
id (integer)
location (string)
created_at (timestamp)
```

users
[this table was created because there are single users in reviewing multiple businesses
 thus a separate table with relationship to businesses prevents data duplication]
```
id (integer)
yelp_user_id (string)
user_url (string) [chosen so that a user can view a reviewers average ratings]
created_at (timestamp)
```

with these tables a data analyst could easily determine bay area businesses
with parking space open during the weekends, a wikipedia page, and a good review.
in addition information on most recent reviewers of the businesses could be fetched
using the users table reference

# Some tables that could be added
Categories, Reviews, & Hours tables could all be added in addition to the base tables
at the cost of added complexity and benefit of richer information. However this database
was kept to the use case

# Ensuring correctness

To ensure relevance users and reviews would be updated at a set cadence, with
orphaned users and locations being removed for data store protection

businesses too would be updated with checks at a slower rate

triggers and constraints set on database to ensure data is valid

tests would be created and run on db updates to ensure call and data integrity

# Monitoring

Monitoring that could be added to this database:
```
metrics on usage
metrics on db changes
metrics on frequency of table writes for optimization
alerts for any errors // data integrity issues
```

# Running code
This code was tested on Ubuntu 18.04

Prereqs:
Install MySQL from https://dev.mysql.com/downloads/ using cluster version 8.0
Install Python3 along with Python3-pip
Make sure to install the libraries below as well
```
python3-dev      
build-essential
libmysqlclient-dev
default-libmysqlclient-dev
libssl-dev
ibffi-dev      
libxml2-dev
libxslt1-dev
zlib1g-dev
```
Next python3-pip install requirements.txt file

An API key will need to be generated from https://www.yelp.com/developers

1. Run mysql from the command line (mysql -u root -p for ubuntu users) and
   initialize the database by running source /PATHTODIR/sql/initialize_tables.sql

2. Quit out of the mysql command line and edit the /PATHTODIR/etl/etl.py file filling
   in MySQL host, user, and password. Replace api_key with the api key you generated
   from yelp

3. To fill the database run python3 etl.py: this will call yelp for all businesses
   found in California. You may edit location in the yelpapi call for different locations

4. The Database can then be queried to return information on businesses in California

# Samples
3 Sample files have been including for a dataset of 100 California businesses to show
a small scale example of what this etl job will generate
