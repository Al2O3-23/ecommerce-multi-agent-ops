from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class BusinessReport(Base):
    __tablename__ = "business_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(String(20))
    end_date = Column(String(20))
    report_content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
