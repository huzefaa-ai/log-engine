import os
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/log_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LogModel(Base):
    __tablename__ = "logs"

    id = Column(String, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    level = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

Base.metadata.create_all(bind=engine)