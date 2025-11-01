import json
from src.ai.mistral_client import ask_mistral

def option_comparison_pipeline(topic: str, opinions: list[str]):
    """
    Analyze comparative opinions about multiple options.

    Returns
    -------
    tuple
        (distribution_and_options: dict, reasons: dict, summary: str,
         recommendation: str, ai_thought: str)
    """
    # Step 1: detect options and votes
    detection_prompt = f"""
You are analyzing comparative opinions.
1. Identify all distinct options mentioned (e.g., React, Vue).
2. Determine which option each opinion prefers.
3. Count how many opinions favor each option.

Return JSON:
{{
  "options": [list of options],
  "votes": {{option: count}},
  "mapping": [{{"opinion": "...", "preferred_option": "..."}}]
}}

Topic: {topic}
Opinions:
{json.dumps(opinions, indent=2)}
"""
    step1 = ask_mistral(detection_prompt)
    options = step1.get("options", [])
    votes = step1.get("votes", {})
    mapping = step1.get("mapping", [])

    # Step 2: extract reasons
    reasons_prompt = f"""
Analyze the opinions and group the main reasons for each option.
Return JSON: {{"reasons": {{option: [short reasons]}}}}

Options: {json.dumps(options)}
Opinions with preferences:
{json.dumps(mapping, indent=2)}
"""
    step2 = ask_mistral(reasons_prompt)
    reasons = step2.get("reasons", {})

    # Step 3: generate summary and recommendation
    summary_prompt = f"""
Write a short neutral summary (2–3 sentences) highlighting the trade-offs among the options below:
Votes: {json.dumps(votes)}
Reasons: {json.dumps(reasons, indent=2)}
"""
    summary = ask_mistral(summary_prompt, format_json=False)

    recommendation_prompt = f"Provide a concise recommendation based on this comparison for '{topic}'."
    recommendation = ask_mistral(recommendation_prompt, format_json=False)

    thought_prompt = "In one sentence, summarize the decisive factor in this recommendation."
    thought = ask_mistral(thought_prompt, format_json=False)

    return {"options": options, "votes": votes}, reasons, summary, recommendation, thought
