from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    func,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from .base import Base, BaseMixin

# -------------------------------------------------------------------------
# CORE MODELS
# -------------------------------------------------------------------------

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


class QuestionType(Base):
    __tablename__ = "question_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    questions = relationship("Question", back_populates="question_type")


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    team_lead_id = Column(Integer, ForeignKey("team_lead.id"), nullable=False)
    question_type_id = Column(Integer, ForeignKey("question_type.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    team_lead = relationship("TeamLead", back_populates="questions")
    question_type = relationship("QuestionType", back_populates="questions")
    answers = relationship("Answer", back_populates="question")
    tokens = relationship("Token", back_populates="question")
    team_links = relationship("TeamQuestion", back_populates="question")

    # Back-references for AI results
    stance_analysis = relationship("StanceAnalysis", back_populates="question", cascade="all, delete-orphan")
    option_comparison = relationship("OptionComparison", back_populates="question", cascade="all, delete-orphan")
    idea_generation = relationship("IdeaGeneration", back_populates="question", cascade="all, delete-orphan")
    priority_ranking = relationship("PriorityRanking", back_populates="question", cascade="all, delete-orphan")
    feedback_analysis = relationship("FeedbackAnalysis", back_populates="question", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    question = relationship("Question", back_populates="answers")


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token_value = Column(String(255), nullable=False, unique=True)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    expires_at = Column(DateTime, server_default=func.now(), nullable=False)
    used = Column(Boolean, default=False)

    question = relationship("Question", back_populates="tokens")
    user = relationship("User", back_populates="tokens")


class UserTeam(Base):
    __tablename__ = "user_team"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    team_id = Column(Integer, ForeignKey("team.id"), primary_key=True)

    user = relationship("User", back_populates="teams")
    team = relationship("Team", back_populates="members")


class TeamQuestion(Base):
    __tablename__ = "team_question"

    team_id = Column(Integer, ForeignKey("team.id"), primary_key=True)
    question_id = Column(Integer, ForeignKey("question.id"), primary_key=True)

    team = relationship("Team", back_populates="questions")
    question = relationship("Question", back_populates="team_links")

# -------------------------------------------------------------------------
# AI ANALYSIS MODELS (linked to question)
# -------------------------------------------------------------------------

class StanceAnalysis(Base, BaseMixin):
    __tablename__ = "stance_analysis"
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False)
    topic: Mapped[str] = mapped_column(Text)
    distribution: Mapped[dict] = mapped_column(JSON)
    total_responses: Mapped[int] = mapped_column(Integer)
    themes: Mapped[dict | None] = mapped_column(JSON)
    summary: Mapped[str | None] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text)
    ai_thought: Mapped[str | None] = mapped_column(Text)
    question = relationship("Question", back_populates="stance_analysis")


class OptionComparison(Base, BaseMixin):
    __tablename__ = "option_comparison"
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False)
    topic: Mapped[str] = mapped_column(Text)
    distribution_and_options: Mapped[dict] = mapped_column(JSON)
    reasons: Mapped[dict | None] = mapped_column(JSON)
    summary: Mapped[str | None] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text)
    ai_thought: Mapped[str | None] = mapped_column(Text)
    question = relationship("Question", back_populates="option_comparison")


class IdeaGeneration(Base, BaseMixin):
    __tablename__ = "idea_generation"
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False)
    topic: Mapped[str] = mapped_column(Text)
    themes: Mapped[dict | None] = mapped_column(JSON)
    summary: Mapped[str | None] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text)
    ai_thought: Mapped[str | None] = mapped_column(Text)
    question = relationship("Question", back_populates="idea_generation")


class PriorityRanking(Base, BaseMixin):
    __tablename__ = "priority_ranking"
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False)
    topic: Mapped[str] = mapped_column(Text)
    options_and_means: Mapped[dict] = mapped_column(JSON)
    top_reasons: Mapped[dict | None] = mapped_column(JSON)
    summary: Mapped[str | None] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text)
    ai_thought: Mapped[str | None] = mapped_column(Text)
    question = relationship("Question", back_populates="priority_ranking")


class FeedbackAnalysis(Base, BaseMixin):
    __tablename__ = "feedback_analysis"
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False)
    topic: Mapped[str] = mapped_column(Text)
    sentiment: Mapped[int] = mapped_column(Integer)
    positive_themes: Mapped[dict | None] = mapped_column(JSON)
    negative_themes: Mapped[dict | None] = mapped_column(JSON)
    summary: Mapped[str | None] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text)
    ai_thought: Mapped[str | None] = mapped_column(Text)
    question = relationship("Question", back_populates="feedback_analysis")
