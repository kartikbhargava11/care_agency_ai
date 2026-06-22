# this file defines the SQL database tables

from sqlalchemy import Column, Integer, String, Boolean, DateTime # importing data types that relational systems use
from datetime import datetime, timezone
from app.database import Base

class IncidentLogTable(Base): # inherits Base class
    __tablename__ = 'call_logs'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    caller = Column(String, index=True, nullable=False)
    patient_name = Column(String, index=True, nullable=False)
    severity = Column(String, nullable=False)
    requires_immediate_human_action = Column(Boolean, default=False)
    incident_summary = Column(String, nullable=False)
    raw_transcript = Column(String, nullable=False)
    logged_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

