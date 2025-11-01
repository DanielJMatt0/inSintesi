from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from db.base import Base

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


class TeamQuestion(Base):
    __tablename__ = "team_question"

    team_id = Column(Integer, ForeignKey("team.id"), primary_key=True)
    question_id = Column(Integer, ForeignKey("question.id"), primary_key=True)

    team = relationship("Team", back_populates="questions")
    question = relationship("Question", back_populates="team_links")
