# database/schema.py

from backend.database.connection import engine


def create_schema() -> None:
    """Create the database schema using the configured engine."""
    # Import models here to register metadata
    # from backend.models import table_model
    # table_model.Base.metadata.create_all(bind=engine)
    pass
