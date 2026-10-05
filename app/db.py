import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()   # reads the .env file in the project root


def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "impactdb"),
        user=os.getenv("DB_USER", "impact"),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor,
    )
    return conn