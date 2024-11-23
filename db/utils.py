from typing import Any, Type, TypeVar
from sqlalchemy.orm import Session
from db.base import Base

ModelType = TypeVar("ModelType", bound=Base)

def create_tables(engine: Any) -> None:
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)

def get_by_id(db: Session, model: Type[ModelType], id: Any) -> ModelType | None:
    """Get a record by its ID."""
    return db.query(model).filter(model.id == id).first()

def create(db: Session, model: Type[ModelType], **kwargs: Any) -> ModelType:
    """Create a new record."""
    db_obj = model(**kwargs)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj 