from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Create the base model class
class BaseModel(db.Model):
    __abstract__ = True
    
    def dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }