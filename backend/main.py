from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

import psycopg2
import requests
import os

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from algam import get_topics as get_social_media_topics
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://algam.vercel.app", "http://localhost:3000"],  # URL of the frontend app (including port if applicable)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

MAX_TOPICS = 30  # Maximum number of topics to fetch

def get_db_connection():
    conn = psycopg2.connect(
        dbname  =os.getenv("DB_NAME"),
        user    =os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host    =os.getenv("DB_HOST"),
        port    =os.getenv("DB_PORT")
    )

    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the table exists
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'trending_topics'
        );
    """)
    exists = cur.fetchone()[0]

    if not exists:
        # If the table doesn't exist, execute the init.sql file
        with open('init.sql', 'r') as f:
            cur.execute(f.read())
        conn.commit()
        print("Table 'trending_topics' created successfully.")
    else:
        print("Table 'trending_topics' already exists.")

    cur.close()
    conn.close()

def fetch_and_store_trending_topics():
    try:
        topics = get_social_media_topics("google", num_topics=MAX_TOPICS)  # Fetch top X topics (s.t. any X > num_topics)
    except Exception as e:
        print(f"Error fetching topics: {e}")
        return

    if not topics:
        print("No topics fetched.")
        return

    conn = get_db_connection()
    cur = conn.cursor()

    # Insert topics into the database
    for topic in topics[::-1]:
        cur.execute(
            "INSERT INTO trending_topics (name, popularity, fetched_at) VALUES (%s, %s, %s)",
            (topic.name, topic.popularity, datetime.now())
        )

    conn.commit()
    cur.close()
    conn.close()

# Schedule the periodic task
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_trending_topics, 'interval', minutes=10)

@app.on_event("startup")
def on_startup():
    init_db()
    scheduler.start()

# Route to get the top n trending topics from the database
@app.get("/topics/{num_topics}")
def get_topics(num_topics: int, db=Depends(get_db_connection)):
    if num_topics > MAX_TOPICS:
        return {"error": f"Number of topics requested exceeds maximum limit of {MAX_TOPICS}."}, 400

    try:
        cur = db.cursor()
        cur.execute(
            "SELECT name, popularity FROM trending_topics ORDER BY fetched_at DESC, popularity DESC LIMIT %s",
            (num_topics,)
        )
        topics = cur.fetchall()
        cur.close()
        db.close()

        if not topics:
            return {"error": "No topics found."}, 500

        return {"topics" : [{"name": topic[0], "popularity": topic[1]} for topic in topics]}, 200
    except Exception as e:
        return {"error": str(e)}, 500

# Route to get the top n trending topics from the database with specific queries in payload, e.g., "reddit, google"
@app.post("/topics/{num_topics}")
def get_topics_with_query(num_topics: int, query: str, db=Depends(get_db_connection)):
    # Not implemented yet
    return {"error": "Not implemented yet."}, 500

# Shut down the scheduler when FastAPI shuts down
@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()