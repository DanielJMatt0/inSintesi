"""
Unified analysis dispatcher for all consensus AI workflows.

This module acts as a single entry point to run an analysis of any type,
store the generated results in the database, and return a structured summary.

Supported types:
- stance_analysis
- option_comparison
- idea_generation
- priority_ranking
- feedback_analysis
"""

from sqlalchemy.orm import Session
from src.db.session import init_db, SessionLocal
from src.db import models

# Import all AI pipelines
from src.ai.pipelines.stance_analysis import stance_pipeline
from src.ai.pipelines.option_comparison import option_comparison_pipeline
from src.ai.pipelines.idea_generation import idea_generation_pipeline
from src.ai.pipelines.priority_ranking import priority_ranking_pipeline
from src.ai.pipelines.feedback_analysis import feedback_analysis_pipeline


# ---------------------------------------------------------------------
# Utility function
# ---------------------------------------------------------------------
def _unwrap(value, key: str):
    """If a dict wraps the real value under a single key, extract it."""
    return value[key] if isinstance(value, dict) and key in value else value


# ---------------------------------------------------------------------
# Main dispatcher
# ---------------------------------------------------------------------
def analyze_topic(
    question_type: str,
    topic: str,
    opinions: list[str],
    session: Session | None = None,
    question_id: int | None = None,
) -> dict:
    """
    Perform an analysis and persist its results in the database.

    Parameters
    ----------
    question_type : str
        One of:
        'stance_analysis', 'option_comparison', 'idea_generation',
        'priority_ranking', or 'feedback_analysis'.
    topic : str
        The question or subject being analyzed.
    opinions : list[str]
        The list of textual inputs to analyze.
    session : Session | None
        Optional SQLAlchemy session; if not provided, a temporary session is created.
    question_id : int | None
        Optional existing Question ID to link this analysis to.

    Returns
    -------
    dict
        A structured summary of the stored record.
    """
    init_db()

    close_session = False
    if session is None:
        session = SessionLocal()
        close_session = True

    try:
        # -----------------------------------------------------------------
        # Create temporary question if missing (for testing or debugging)
        # -----------------------------------------------------------------
        if question_id is None:
            from db.models.question import Question

            temp_question = Question(content=topic, team_lead_id=1, question_type_id=1)
            session.add(temp_question)
            session.commit()
            question_id = temp_question.id

        # -----------------------------------------------------------------
        # Dispatch by question type
        # -----------------------------------------------------------------
        if question_type == "stance_analysis":
            distribution, total, summary, recommendation, thought = stance_pipeline(topic, opinions)
            record = models.StanceAnalysis(
                question_id=question_id,
                topic=topic,
                raw_inputs={"opinions": opinions},
                distribution=distribution,
                total_responses=total,
                summary=summary,
                recommendation=recommendation,
                ai_thought=thought,
            )

        elif question_type == "option_comparison":
            dist_opts, reasons, summary, recommendation, thought = option_comparison_pipeline(topic, opinions)
            record = models.OptionComparison(
                question_id=question_id,
                topic=topic,
                raw_inputs={"opinions": opinions},
                distribution_and_options=dist_opts,
                reasons=reasons,
                summary=summary,
                recommendation=recommendation,
                ai_thought=thought,
            )

        elif question_type == "idea_generation":
            themes, summary, recommendation, thought = idea_generation_pipeline(topic, opinions)
            themes = _unwrap(themes, "themes")

            record = models.IdeaGeneration(
                question_id=question_id,
                topic=topic,
                raw_inputs={"ideas": opinions},
                themes=themes,
                summary=summary,
                recommendation=recommendation,
                ai_thought=thought,
            )

        elif question_type == "priority_ranking":
            opts_means, top_reasons, summary, recommendation, thought = priority_ranking_pipeline(topic, opinions)
            record = models.PriorityRanking(
                question_id=question_id,
                topic=topic,
                raw_inputs={"opinions": opinions},
                options_and_means=opts_means,
                top_reasons=top_reasons,
                summary=summary,
                recommendation=recommendation,
                ai_thought=thought,
            )

        elif question_type == "feedback_analysis":
            sentiment, pos_themes, neg_themes, summary, recommendation, thought = feedback_analysis_pipeline(
                topic, opinions
            )

            pos_themes = _unwrap(pos_themes, "themes")
            neg_themes = _unwrap(neg_themes, "themes")

            record = models.FeedbackAnalysis(
                question_id=question_id,
                topic=topic,
                raw_inputs={"feedback": opinions},
                sentiment=sentiment,
                positive_themes=pos_themes,
                negative_themes=neg_themes,
                summary=summary,
                recommendation=recommendation,
                ai_thought=thought,
            )

        else:
            raise ValueError(f"Unsupported question_type: {question_type}")

        # -----------------------------------------------------------------
        # Persist record
        # -----------------------------------------------------------------
        session.add(record)
        session.commit()
        session.refresh(record)

        # -----------------------------------------------------------------
        # Prepare structured result for API or CLI use
        # -----------------------------------------------------------------
        result = {
            "id": record.id,
            "question_type": question_type,
            "topic": record.topic,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None,
            "summary": getattr(record, "summary", None),
            "recommendation": getattr(record, "recommendation", None),
            "ai_thought": getattr(record, "ai_thought", None),
        }

        # Attach additional fields based on record type
        if isinstance(record, models.StanceAnalysis):
            result.update(
                {
                    "distribution": record.distribution,
                    "total_responses": record.total_responses,
                    "themes": record.themes,
                }
            )
        elif isinstance(record, models.OptionComparison):
            result.update(
                {
                    "distribution_and_options": record.distribution_and_options,
                    "reasons": record.reasons,
                }
            )
        elif isinstance(record, models.IdeaGeneration):
            result.update({"themes": record.themes})
        elif isinstance(record, models.PriorityRanking):
            result.update(
                {
                    "options_and_means": record.options_and_means,
                    "top_reasons": record.top_reasons,
                }
            )
        elif isinstance(record, models.FeedbackAnalysis):
            result.update(
                {
                    "sentiment": record.sentiment,
                    "positive_themes": record.positive_themes,
                    "negative_themes": record.negative_themes,
                }
            )

        return result

    finally:
        if close_session:
            session.close()


# ---------------------------------------------------------------------
# Local testing utility
# ---------------------------------------------------------------------
if __name__ == "__main__":
    examples = [
        (
            "stance_analysis",
            "Should we adopt a 4-day work week?",
            [
                "Yes, it would increase productivity.",
                "No, clients expect availability five days a week.",
                "Possibly, if teams can coordinate coverage.",
            ],
        ),
        (
            "option_comparison",
            "React vs Vue for the frontend framework.",
            [
                "React has a larger ecosystem.",
                "Vue is simpler and faster to learn.",
                "React is better for scalability.",
            ],
        ),
        (
            "idea_generation",
            "How can we make our workplace more innovative?",
            [
                "Host regular internal hackathons.",
                "Introduce a mentorship program.",
                "Create open channels for idea sharing.",
            ],
        ),
        (
            "priority_ranking",
            "Prioritize features A, B, and C.",
            [
                "A first for impact, then B, then C.",
                "B should come first for customer satisfaction.",
                "C last because it’s purely aesthetic.",
            ],
        ),
        (
            "feedback_analysis",
            "How was your onboarding experience?",
            [
                "The process was smooth and clear.",
                "Too many tools to set up on day one.",
                "My mentor was very helpful.",
                "Some systems didn’t work initially.",
            ],
        ),
    ]

    for qtype, topic, data in examples:
        print(f"\nRunning analysis for: {qtype} | {topic}")
        result = analyze_topic(qtype, topic, data)
        print(result)
