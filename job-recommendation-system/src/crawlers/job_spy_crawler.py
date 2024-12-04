import numpy as np
import openai
import psycopg2

from pgvector.psycopg2 import register_vector
from psycopg2.extras import execute_values
from loguru import logger
from jobspy import scrape_jobs

from dotenv import load_dotenv
load_dotenv()

from src.utils import get_embeddings


def etl():
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
        search_term="data",
        location="San Francisco",
        results_wanted=20,
        hours_old=72, # (only Linkedin/Indeed is hour specific, others round up to days old)
        country_indeed='USA',  # only needed for indeed / glassdoor
        # linkedin_fetch_description=True # get full description and direct job url for linkedin (slower)
    )

    logger.info(f"{jobs.shape}")
    

    # Load
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="mypass",
        host="localhost",
        port="5432"
    )
    
    cur = connection.cursor()
    #install pgvector
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector");
    connection.commit()
    
    
    register_vector(connection)
    
    # Create table to store embeddings and metadata
    table_create_command = """
    CREATE TABLE embeddings (
                id bigserial primary key, 
                site text,
                job_url text,
                title text,
                company text,
                location text,
                date_posted text,
                interval text,
                min_amount float,
                max_amount float,
                currency text,
                is_remote text,
                description text,
                company_url text,
                company_logo text,
                embedding vector(1536)
                );
                """
    cur.execute(table_create_command)
    cur.close()
    connection.commit()
    
    #Batch insert embeddings and metadata from dataframe into PostgreSQL database
    register_vector(connection)
    cur = connection.cursor()
    # Prepare the list of tuples to insert
    
    data_list = [
        (
            row['site'],
            row['job_url'],
            row['title'],
            row['company'],
            row['location'],
            row['date_posted'],
            row['interval'],
            row['min_amount'],
            row['max_amount'],
            row['currency'],
            row['is_remote'],
            row['description'],
            row['company_url'],
            row['company_logo'],
            np.array(get_embeddings(row['description']))  # Assuming 'embeddings' is a column with vector data
        )
        for index, row in jobs.iterrows()
    ]

    # Use execute_values to perform batch insertion
    execute_values(
        cur,
        """
        INSERT INTO embeddings (site, job_url, title, company, location, date_posted, interval, min_amount, max_amount, currency, is_remote, description, company_url, company_logo, embedding)
        VALUES %s
        """,
        data_list
    )
    # Commit after we insert all embeddings
    connection.commit()
    