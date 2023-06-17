#!/usr/bin/python3
# File = ManaaDB.py

import psycopg2 as pg
from os import environ
from dotenv import load_dotenv
load_dotenv();

conn_pg = pg.connect(
    database = environ["DB_NAME"], # Database Name
    host = environ["DB_HOST"], # Database Host
    user = environ["DB_USER"], # Database user
    password = environ["DB_USER_PASSWORD"] # Database password
)
conn_pg.autocommit = True

