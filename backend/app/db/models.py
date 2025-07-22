from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)  # Ensure fullname is required
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, server_default=text("now()"))
    last_convo = Column(TIMESTAMP, server_default=text("now()"))
    summary_file = Column(JSON, nullable=True, default=lambda: [{"conversation_time": "", "summary": ""}])
    chat_history = Column(JSON, nullable=True)
