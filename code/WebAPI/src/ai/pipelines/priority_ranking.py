import json
from src.ai.mistral_client import ask_mistral

def priority_ranking_pipeline(topic: str, opinions: list[str]):
    """
    Analyze ranked preferences or prioritization of options.

    Returns
    -------
    tuple
        (options_and_means: dict, top_reasons: dict,
         summary: str, recommendation: str, ai_thought: str)
    """
    # Step 1: extract and compute average rankings
    ranking_prompt = f"""
You are analyzing survey responses where users rank options.
Tasks:
1. Identify all unique options mentioned.
2. Infer the rank or order of preference from each opinion.
3. Compute an average ranking score (1 = highest priority).

Return JSON:
{{
  "options": [list of option names],
  "average_ranking": {{option: average_rank_number}},
  "parsed_opinions": [{{"opinion": "...", "ranking": ["...","...","..."]}}]
}}

Topic: {topic}
Opinions:
{json.dumps(opinions, indent=2)}
"""
    step1 = ask_mistral(ranking_prompt)
    options = step1.get("options", [])
    avg_ranking = step1.get("average_ranking", {})
    parsed = step1.get("parsed_opinions", [])

    # Step 2: reasons per option
    reasons_prompt = f"""
Analyze the following opinions and identify main reasons why each option
is ranked higher or lower.

Return JSON: {{"top_reasons": {{option: [short reasons]}}}}
Options: {json.dumps(options)}
Opinions with ranking info:
{json.dumps(parsed, indent=2)}
"""
    step2 = ask_mistral(reasons_prompt)
    top_reasons = step2.get("top_reasons", {})

    # Step 3: summary and recommendation
    summary_prompt = f"""
Based on the average ranking and reasons, write a neutral summary (2–3 sentences)
explaining the main patterns and priorities.
Average ranking: {json.dumps(avg_ranking)}
Top reasons: {json.dumps(top_reasons, indent=2)}
"""
    summary = ask_mistral(summary_prompt, format_json=False)

    recommendation_prompt = f"Provide a concise recommendation on which option(s) to prioritize first for '{topic}'."
    recommendation = ask_mistral(recommendation_prompt, format_json=False)

    thought_prompt = "In one sentence, summarize the key criterion that drives the prioritization."
    thought = ask_mistral(thought_prompt, format_json=False)

    return {"options": options, "average_ranking": avg_ranking}, top_reasons, summary, recommendation, thought
