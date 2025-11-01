from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from src.db.base import Base


# ---------------------------------------------------------------------
# User
# ---------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    lastname = Column(String(30))
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Many-to-many relationship with Team through UserTeam
    team_links = relationship("UserTeam", back_populates="user", cascade="all, delete-orphan")

    # Association proxy for direct access: user.teams
    teams = association_proxy(
        "team_links", "team",
        creator=lambda t: UserTeam(team=t)
    )

    # One-to-many relationship with Token
    tokens = relationship("Token", back_populates="user")


# ---------------------------------------------------------------------
# TeamLead
# ---------------------------------------------------------------------
class TeamLead(Base):
    __tablename__ = "team_lead"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # One-to-many relationships
    teams = relationship("Team", back_populates="lead")
    questions = relationship("Question", back_populates="team_lead")


# ---------------------------------------------------------------------
# Team
# ---------------------------------------------------------------------
class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_lead_id = Column(Integer, ForeignKey("team_lead.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Reference to the team lead
    lead = relationship("TeamLead", back_populates="teams")

    # Many-to-many relationships
    user_links = relationship("UserTeam", back_populates="team", cascade="all, delete-orphan")
    team_links = relationship("TeamQuestion", back_populates="team", cascade="all, delete-orphan")

    # Association proxy for direct access: team.users
    users = association_proxy(
        "user_links", "user",
        creator=lambda u: UserTeam(user=u)
    )

    # Association proxy for direct access: team.questions
    questions = association_proxy(
        "team_links", "question",
        creator=lambda q: __import__("src.db.models.question", fromlist=["TeamQuestion"]).TeamQuestion(question=q)
    )


# ---------------------------------------------------------------------
# UserTeam (association table between User and Team)
# ---------------------------------------------------------------------
class UserTeam(Base):
    __tablename__ = "user_team"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    team_id = Column(Integer, ForeignKey("team.id"), primary_key=True)

    # Relationships to both sides
    user = relationship("User", back_populates="team_links")
    team = relationship("Team", back_populates="user_links")

    # Constructor compatible with association_proxy
    def __init__(self, user=None, team=None, **kwargs):
        super().__init__(**kwargs)
        if user:
            self.user = user
        if team:
            self.team = team
