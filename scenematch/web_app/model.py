from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

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
    timestamp = Column(DateTime, default=datetime)

# Setup
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
