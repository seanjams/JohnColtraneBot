from flask import Flask
import os


class NoRedditCredentials(Exception):
    pass

# DB url
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")

# Should run scheduler on startup
RUN_SCHEDULER = os.getenv("RUN_SCHEDULER")

# Logs for development
LOGGING_VERBOSE = os.getenv("LOGGING_VERBOSE")
LOGGING_VERBOSE = False if LOGGING_VERBOSE == "False" else True

# Reddit Config
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
if not all((
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    REDDIT_USERNAME,
    REDDIT_PASSWORD,
)):
    raise NoRedditCredentials(
        "No Reddit Credentials found in environment. Aborting."
    )


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_DATABASE_URI = DATABASE_URL

# create app
app = Flask(__name__)
app.config.from_object(Config())
