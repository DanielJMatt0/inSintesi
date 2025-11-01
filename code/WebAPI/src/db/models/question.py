from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Boolean, func
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from src.db.base import Base


# ---------------------------------------------------------------------
# Question Type
# ---------------------------------------------------------------------
class QuestionType(Base):
    """Represents a specific type of question (analysis category)."""
    __tablename__ = "question_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    questions = relationship("Question", back_populates="question_type", lazy="joined")


# ---------------------------------------------------------------------
# Question
# ---------------------------------------------------------------------
class Question(Base):
    """Core question model used across AI analyses."""
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    team_lead_id = Column(Integer, ForeignKey("team_lead.id"), nullable=False)
    question_type_id = Column(Integer, ForeignKey("question_type.id"), nullable=False)
    report_id = Column(String(36), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # --- Relationships ---
    team_lead = relationship("TeamLead", back_populates="questions")
    question_type = relationship("QuestionType", back_populates="questions", lazy="joined")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    tokens = relationship("Token", back_populates="question", cascade="all, delete-orphan")


    team_links = relationship("TeamQuestion", back_populates="question", cascade="all, delete-orphan")


    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from src.db.models.core import Team
    teams = association_proxy(
        "team_links", "team",
        creator=lambda t: TeamQuestion(team=t)
    )

    # --- AI analysis ---
    stance_analysis = relationship("StanceAnalysis", back_populates="question", cascade="all, delete-orphan")
    option_comparison = relationship("OptionComparison", back_populates="question", cascade="all, delete-orphan")
    idea_generation = relationship("IdeaGeneration", back_populates="question", cascade="all, delete-orphan")
    priority_ranking = relationship("PriorityRanking", back_populates="question", cascade="all, delete-orphan")
    feedback_analysis = relationship("FeedbackAnalysis", back_populates="question", cascade="all, delete-orphan")


# ---------------------------------------------------------------------
# Answer
# ---------------------------------------------------------------------
class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    question = relationship("Question", back_populates="answers")


# ---------------------------------------------------------------------
# Token
# ---------------------------------------------------------------------
class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token_value = Column(String(255), nullable=False, unique=True)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=True)
    used = Column(Boolean, nullable=True, default=False)

    question = relationship("Question", back_populates="tokens")
    user = relationship("User", back_populates="tokens")


# ---------------------------------------------------------------------
# TeamQuestion
# ---------------------------------------------------------------------
class TeamQuestion(Base):
    __tablename__ = "team_question"

    team_id = Column(Integer, ForeignKey("team.id"), primary_key=True)
    question_id = Column(Integer, ForeignKey("question.id"), primary_key=True)

    team = relationship("Team", back_populates="team_links")
    question = relationship("Question", back_populates="team_links")

    def __init__(self, team=None, question=None):
        if team:
            self.team = team
        if question:
            self.question = question
