from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP, Table, text
from sqlalchemy.orm import relationship
from .database import Base


user_team = Table(
    "user_team",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("team_id", Integer, ForeignKey("team.id", ondelete="CASCADE"), primary_key=True)
)

team_question = Table(
    "team_question",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("team.id", ondelete="CASCADE"), primary_key=True),
    Column("question_id", Integer, ForeignKey("question.id", ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20))
    lastname = Column(String(30))
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    teams = relationship("Team", secondary=user_team, back_populates="users")
    tokens = relationship("Token", back_populates="user")


class TeamLead(Base):
    __tablename__ = "team_lead"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    teams = relationship("Team", back_populates="team_lead")
    questions = relationship("Question", back_populates="team_lead")


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True)
    team_lead_id = Column(Integer, ForeignKey("team_lead.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    team_lead = relationship("TeamLead", back_populates="teams")
    users = relationship("User", secondary=user_team, back_populates="teams")
    questions = relationship("Question", secondary=team_question, back_populates="teams")


class QuestionType(Base):
    __tablename__ = "question_type"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(100), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    questions = relationship("Question", back_populates="question_type")


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    team_lead_id = Column(Integer, ForeignKey("team_lead.id", ondelete="CASCADE"), nullable=False)
    question_type_id = Column(Integer, ForeignKey("question_type.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    team_lead = relationship("TeamLead", back_populates="questions")
    question_type = relationship("QuestionType", back_populates="questions")
    answers = relationship("Answer", back_populates="question")
    teams = relationship("Team", secondary=team_question, back_populates="questions")
    tokens = relationship("Token", back_populates="question")


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    question = relationship("Question", back_populates="answers")


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, index=True)
    token_value = Column(String(255), unique=True, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    expires_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    used = Column(Boolean, default=False)

    question = relationship("Question", back_populates="tokens")
    user = relationship("User", back_populates="tokens")
