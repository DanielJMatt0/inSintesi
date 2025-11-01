import json
from ai.mistral_client import ask_mistral

def idea_generation_pipeline(topic: str, ideas: list[str]):
    """
    Analyze open-ended proposals or creative ideas.

    Returns
    -------
    tuple
        (themes: dict, summary: str, recommendation: str, ai_thought: str)
    """
    # Step 1: cluster ideas into themes
    cluster_prompt = f"""
You analyze employee ideas and group similar ones into 3–6 high-level themes.
For each theme, include representative ideas and a brief summary.

Return JSON:
{{
  "themes": [
    {{"name": "...", "ideas": ["..."], "summary": "..."}}
  ]
}}

Ideas:
{json.dumps(ideas, indent=2)}
"""
    themes = ask_mistral(cluster_prompt)

    # Step 2: write a summary
    summary_prompt = f"""
Write a short neutral summary (2–3 sentences) describing the main directions and motivations behind the following themes:
{json.dumps(themes, indent=2)}
"""
    summary = ask_mistral(summary_prompt, format_json=False)

    # Step 3: recommendation
    recommendation_prompt = f"""
Topic: {topic}
Themes: {json.dumps(themes, indent=2)}
Summary: {summary}

Write a practical recommendation (2–3 sentences) suggesting clear next steps.
"""
    recommendation = ask_mistral(recommendation_prompt, format_json=False)

    # Step 4: AI thought
    thought_prompt = "In one sentence, describe the main opportunity reflected in this recommendation."
    thought = ask_mistral(thought_prompt, format_json=False)

    return themes, summary, recommendation, thought
