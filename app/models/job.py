from sqlalchemy import Column, Integer, String, Text

from app.database.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String)
    salary = Column(String)

    url = Column(String, unique=True, nullable=False)

    description = Column(Text, nullable=True)

    required_skills = Column(Text, nullable=True)