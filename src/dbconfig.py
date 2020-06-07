import os
from flask_sqlalchemy import SQLAlchemy
from src.app import app

# PostgreSQL configuration
POSTGRES_USER = os.getenv("PG_USER")
POSTGRES_URL = os.getenv("PG_URL")
POSTGRES_PW = os.getenv("PG_PW")
POSTGRES_DB = os.getenv("PG_DB_EV")

DATABASE_URL = os.getenv("DATABASE_URL")

# DB URL
if not DATABASE_URL:
    DATABASE_URL = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB
    )

# SQLAlchemy configuration
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # silence deprecation warning

db = SQLAlchemy(app)
