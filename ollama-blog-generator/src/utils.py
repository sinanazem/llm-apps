import json
import yaml
import psycopg2
from sqlalchemy import create_engine
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
import os
from loguru import logger

def make_db_connection_psycopg2(database: str, autocommit: bool = False):

    #assert database in list(conn_dict.keys()), "server couldn't be recognized in the config file"

    
    database="blog"
    host="localhost"
    port="5432"
    user="postgres"
    password="matin9862"
    
    conn = psycopg2.connect(user=user, password=password, host=host, dbname=database)
    cursor = conn.cursor()

    if autocommit:
        conn.autocommit = True

    return conn, cursor
