from app.database.database import Base, engine
from app.models.candidate import Candidate

import app.models.job

def init_db():
    Base.metadata.create_all(bind=engine)