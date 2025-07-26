from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

# load .env file variables
load_dotenv()

Base = declarative_base()

# Feedback model
class UserFeedback(Base):
    __tablename__ = 'user_feedback'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255))
    session_id = Column(String(255))
    message_id = Column(String(255))
    feedback_type = Column(String(50))
    rating = Column(Integer)
    comment = Column(Text)
    user_message = Column(Text)
    model_response = Column(Text)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/feedback_db")

engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
