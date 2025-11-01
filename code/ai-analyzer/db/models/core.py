from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    lastname = Column(String(30))
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    teams = relationship("UserTeam", back_populates="user")
    tokens = relationship("Token", back_populates="user")


class TeamLead(Base):
    __tablename__ = "team_lead"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    teams = relationship("Team", back_populates="lead")
    questions = relationship("Question", back_populates="team_lead")


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_lead_id = Column(Integer, ForeignKey("team_lead.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    lead = relationship("TeamLead", back_populates="teams")
    members = relationship("UserTeam", back_populates="team")
    questions = relationship("TeamQuestion", back_populates="team")


class UserTeam(Base):
    __tablename__ = "user_team"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    team_id = Column(Integer, ForeignKey("team.id"), primary_key=True)

    user = relationship("User", back_populates="teams")
    team = relationship("Team", back_populates="members")
