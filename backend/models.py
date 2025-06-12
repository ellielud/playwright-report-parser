from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TestRun(Base):
    __tablename__ = "test_runs"

    id = Column(Integer, primary_key=True, index=True)
    test_name = Column(String)
    status = Column(String)
    error_message = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)