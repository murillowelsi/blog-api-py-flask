import psycopg2
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="blog",
        user="admin",
        password="root"
    )
    return conn


def create_tables(app):
    with app.app_context():
        db.create_all()
