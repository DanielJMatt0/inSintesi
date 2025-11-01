from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON, Text, Integer
from .base import Base, BaseMixin


class StanceAnalysis(Base, BaseMixin):
    """Model for pro/contra/undecided stance analysis results."""
    __tablename__ = "stance_analysis"
    topic: Mapped[str] = mapped_column(Text)
    distribution: Mapped[dict] = mapped_column(JSON)
    total_responses: Mapped[int] = mapped_column(Integer)
    themes: Mapped[dict | None] = mapped_column(JSON)
    summary: Mapped[str | None] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text)
    ai_thought: Mapped[str | None] = mapped_column(Text)


class OptionComparison(Base, BaseMixin):
    """Model for comparative analysis results between options."""
    __tablename__ = "option_comparison"
    topic: Mapped[str] = mapped_column(Text)
    distribution_and_options: Mapped[dict] = mapped_column(JSON)
    reasons: Mapped[dict | None] = mapped_column(JSON)
    summary: Mapped[str | None] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text)
    ai_thought: Mapped[str | None] = mapped_column(Text)


class IdeaGeneration(Base, BaseMixin):
    """Model for open idea or proposal synthesis."""
    __tablename__ = "idea_generation"
    topic: Mapped[str] = mapped_column(Text)
    themes: Mapped[dict | None] = mapped_column(JSON)
    summary: Mapped[str | None] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text)
    ai_thought: Mapped[str | None] = mapped_column(Text)


class PriorityRanking(Base, BaseMixin):
    """Model for ranking and prioritization results."""
    __tablename__ = "priority_ranking"
    topic: Mapped[str] = mapped_column(Text)
    options_and_means: Mapped[dict] = mapped_column(JSON)
    top_reasons: Mapped[dict | None] = mapped_column(JSON)
    summary: Mapped[str | None] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text)
    ai_thought: Mapped[str | None] = mapped_column(Text)


class FeedbackAnalysis(Base, BaseMixin):
    """Model for sentiment and qualitative feedback analysis."""
    __tablename__ = "feedback_analysis"
    topic: Mapped[str] = mapped_column(Text)
    sentiment: Mapped[int] = mapped_column(Integer)
    positive_themes: Mapped[dict | None] = mapped_column(JSON)
    negative_themes: Mapped[dict | None] = mapped_column(JSON)
    summary: Mapped[str | None] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text)
    ai_thought: Mapped[str | None] = mapped_column(Text)
