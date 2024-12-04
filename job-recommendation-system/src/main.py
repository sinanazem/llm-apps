import json
import psycopg2
import pymupdf4llm
import numpy as np

from src.retrive import get_top3_similar_docs
from src.crawlers.job_spy_crawler import etl
from pathlib import Path


BASE_DIR = Path(".").resolve()

# 1 Resume 
file_path = BASE_DIR / "data/matinsajadi.pdf"
md_text = pymupdf4llm.to_markdown(file_path)

# 2 Retrival Similar Jobs
connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="mypass",
    host="localhost",
    port="5432"
)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)



if __name__ == "__main__":
    
    #etl()
    
    res = get_top3_similar_docs(md_text, conn=connection)

    with open("output.json", "w") as f:
        json.dump(res, f, cls=NumpyEncoder, indent=4)


        