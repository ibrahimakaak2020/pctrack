from flask.cli import FlaskGroup
from app import create_app
from app.db.database import db

cli = FlaskGroup(create_app=create_app)

if __name__ == '__main__':
    cli() 