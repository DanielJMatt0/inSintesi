import json
from src.ai.mistral_client import ask_mistral

def feedback_analysis_pipeline(topic: str, feedback: list[str]):
    """
    Analyze qualitative feedback to extract sentiment and themes.

    Returns
    -------
    tuple
        (sentiment: int, positive_themes: dict, negative_themes: dict,
         summary: str, recommendation: str, ai_thought: str)
    """
    # Step 1: identify sentiment and themes
    sentiment_prompt = f"""
You are analyzing employee feedback.
1. Separate into positive and negative themes.
2. Include representative examples for each.
3. Compute an overall sentiment score between 0 and 1 (1 = fully positive).

Return JSON:
{{
  "positive_themes": [{{"name": "...", "examples": ["..."]}}],
  "negative_themes": [{{"name": "...", "examples": ["..."]}}],
  "sentiment_score": number
}}

Topic: {topic}
Feedback:
{json.dumps(feedback, indent=2)}
"""
    step1 = ask_mistral(sentiment_prompt)
    pos = step1.get("positive_themes", [])
    neg = step1.get("negative_themes", [])
    score = float(step1.get("sentiment_score", 0.0))
    sentiment_int = max(0, min(100, int(round(score * 100))))

    # Step 2: summary
    summary_prompt = f"""
Write a short neutral summary (2–3 sentences) describing the key positive and negative aspects
identified from the following feedback.

Positive themes: {json.dumps(pos, indent=2)}
Negative themes: {json.dumps(neg, indent=2)}
Sentiment score: {score}
"""
    summary = ask_mistral(summary_prompt, format_json=False)

    # Step 3: recommendation
    recommendation_prompt = f"""
Based on the analysis above, write a concise recommendation (2–3 sentences)
suggesting practical improvements for '{topic}'.
"""
    recommendation = ask_mistral(recommendation_prompt, format_json=False)

# Step 4: AI Thought — flagging inconsistent opinions
    thought_prompt = f"""
Review all provided feedback opinions and evaluate whether any appear inconsistent,
irrelevant, contradictory or out of alignment with the main themes, summary or sentiment score.
Return a short commentary (2-4 sentences) that:
- Lists any specific opinions by index (or content) that you believe may not make sense or are contradictory.
- Explains why they may be problematic.
- Concludes with whether they meaningfully impact the overall result.

Topic: {topic}
Feedback list:
{json.dumps(feedback, indent=2)}
Identified themes (positive): {json.dumps(pos, indent=2)}
Identified themes (negative): {json.dumps(neg, indent=2)}
Sentiment score: {sentiment_int}
Summary: {summary}
Recommendation: {recommendation}
"""
    ai_thought = ask_mistral(thought_prompt, format_json=False, temperature=0.4)

    return sentiment_int, {"themes": pos}, {"themes": neg}, summary, recommendation, ai_thought