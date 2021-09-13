# public_api_crawler
 
 # About
This is a repository which crawls the list of all the api links present in the repository https://github.com/public-apis/public-apis and stores them in a database without using any scraping methods using it's api (Documentation here : https://documenter.getpostman.com/view/4796420/SzmZczsh?version=latest).

# Steps to run code

## Requirements
- python 3.8.1
- requests module of python
- install the required packages using pip if you have python installed (i.e- ```pip install pkg-name``` or ```conda install pkg-name```)
```pip install requests```
- open the directory in terminal and run
```python crawler.py```

# Tables of the database and the schema

Only a single table is created in the database named api_links.db
The schema is
- category (datatype text)
- api (datatype text)
- link (datatype text)

# Features (Points Achieved)

- OOPS Code
- pagination support
- Support for handling authentication requirements & token expiration of server
- work around for rate limited server
- Crawled all API entries for all categories and stored it in a database

# Points didn't achieve

All points achieved

# Further improvements

The code could have been containerized with Docker support if additional time would have been there
