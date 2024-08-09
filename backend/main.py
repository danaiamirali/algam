from fastapi import FastAPI
from algam import get_topics as get_social_media_topics
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL of the frontend app (including port if applicable)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/topics/{num_topics}")
def get_topics(num_topics: int):
    try:
        topics = get_social_media_topics("google", "reddit", weights=[0.8, 0.2], num_topics=num_topics)
    except Exception as e:
        return {"error": str(e)}, 500

    if not topics:
        return {"error": "No topics found."}, 500

    return topics, 200

