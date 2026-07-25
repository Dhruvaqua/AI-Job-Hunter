from app.database.database import Base, engine

import app.models.job

def init_db():
    Base.metadata.create_all(bind=engine)