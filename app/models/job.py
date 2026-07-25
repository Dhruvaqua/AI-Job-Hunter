from sqlalchemy import Column, Integer, String, Text

from app.database.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    company = Column(String(255), nullable=False)

    location = Column(String(255), nullable=True)

    salary = Column(String(255), nullable=True)

    url = Column(String(500), unique=True, nullable=False)

    description = Column(Text, nullable=True)