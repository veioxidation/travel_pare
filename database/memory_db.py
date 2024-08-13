import os

from pathlib import Path
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from dotenv import load_dotenv
load_dotenv(os.path.join(Path(__file__).parent.parent, ".env"))

database_name = 'langchain'
schema_name = "travel_pare"
__user = os.getenv("POSTGRES_USER")
__password = os.getenv("POSTGRES_PASSWORD")
if not __user or not __password:
    raise ValueError("Please set the POSTGRES_USER and POSTGRES_PASSWORD environment variables.")

DB_URI = f'postgresql://{__user}:{__password}@localhost:5432/{database_name}?sslmode=disable&options=-csearch_path%3D{schema_name}'


connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
    "row_factory": dict_row,
}


pool = ConnectionPool(
    # Example configuration
    conninfo=DB_URI,
    max_size=20,
    kwargs=connection_kwargs
)