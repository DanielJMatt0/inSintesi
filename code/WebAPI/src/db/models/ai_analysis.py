from sqlalchemy import JSON, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base, BaseMixin

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
