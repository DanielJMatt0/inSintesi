from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.db import models
from src.ai.mistral_client import ask_mistral


def get_question_type_by_content(db: Session, content: str) -> int:
    """
    Determines the question type using the Mistral API based on the question content.
    Returns the numeric ID of the corresponding QuestionType record in the database.
    """

    # These are the allowed types present in your DB
    allowed_types = [
        "stance_analysis",
        "option_comparison",
        "idea_generation",
        "priority_ranking",
        "feedback_analysis",
    ]

    # Build the prompt for Mistral
    prompt = f"""
    You are an assistant that classifies questions into analytical categories.
    Analyze the question below and return its most appropriate type.

    Available types:
    - stance_analysis: analyzes opinions or attitudes
    - option_comparison: compares options or choices
    - idea_generation: generates new ideas or suggestions
    - priority_ranking: ranks or prioritizes items
    - feedback_analysis: analyzes feedback or reviews

    Question: "{content}"

    Respond ONLY in this JSON format:
    {{
        "type": "<one_of: stance_analysis | option_comparison | idea_generation | priority_ranking | feedback_analysis>"
    }}
    """

    # Ask Mistral for classification
    response = ask_mistral(prompt, format_json=True)
    detected_type = response.get("type") if isinstance(response, dict) else None

    # Validate the detected type
    if detected_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid or missing question type '{detected_type}'."
        )

    # Find the corresponding record in the DB
    question_type = (
        db.query(models.QuestionType)
        .filter(models.QuestionType.type == detected_type)
        .first()
    )

    if not question_type:
        raise HTTPException(
            status_code=400,
            detail=f"Question type '{detected_type}' not found in database.",
        )

    # Return the numeric ID (not the object)
    return question_type.id
