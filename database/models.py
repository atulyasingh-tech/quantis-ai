from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Text, JSON, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PublishedPost(Base):
    __tablename__ = "published_posts"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    rationale = Column(Text, nullable=False)
    sources = Column(JSON, nullable=False)
    confidence_score = Column(Float, nullable=False)
    future_impact = Column(Text, nullable=False)
    content_hash = Column(String, unique=True, index=True)

class RejectedTopic(Base):
    __tablename__ = "rejected_topics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    topic_title = Column(String, nullable=False)
    source_url = Column(String, nullable=True)
    rejection_reason = Column(Text, nullable=False)
    score = Column(Float, nullable=False)
