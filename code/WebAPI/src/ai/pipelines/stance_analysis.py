import json
from src.ai.mistral_client import ask_mistral

def stance_pipeline(topic: str, opinions: list[str]):
    """
    Analyze pro, contra, and neutral stances for a given topic.
    Returns a distribution dictionary, total count, summary, recommendation, and AI rationale.
    """
    # Step 1: classification
    classification_prompt = f"""
Classify each opinion about "{topic}" as "pro", "contra", or "neutral".
Return JSON array with: opinion, classification, reason.
Opinions:
{json.dumps(opinions, indent=2)}
"""
    classified = ask_mistral(classification_prompt)
    dist = {"pro": 0, "contra": 0, "neutral": 0}
    for c in classified:
        if c.get("classification") in dist:
            dist[c["classification"]] += 1

    # Step 2: summary and recommendation
    summary_prompt = f"Write a short neutral summary (2–3 sentences) describing the main arguments about '{topic}'."
    summary = ask_mistral(summary_prompt, format_json=False)

    rec_prompt = f"Provide a concise recommendation (2–3 sentences) based on the opinions above for '{topic}'."
    recommendation = ask_mistral(rec_prompt, format_json=False)

    thought_prompt = "In one sentence, summarize the key reasoning behind this recommendation."
    thought = ask_mistral(thought_prompt, format_json=False)

    return dist, len(opinions), summary, recommendation, thought
