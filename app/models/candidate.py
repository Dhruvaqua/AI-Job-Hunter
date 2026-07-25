from sqlalchemy import Column, Integer, String

from app.database.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    location = Column(String, nullable=False)

    skills = Column(String, nullable=False)