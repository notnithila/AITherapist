from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class JournalEntry(Base):
    __tablename__ = 'journal_entries'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.now())

    analysis = relationship("AnalysisResult", back_populates="entry", uselist=False)

class AnalysisResult(Base):
    __tablename__ = 'analysis_results'

    id = Column(Integer, primary_key=True)
    journal_id = Column(Integer, ForeignKey('journal_entries.id'))
    recommendation = Column(Text)

    entry = relationship("JournalEntry", back_populates="analysis")
